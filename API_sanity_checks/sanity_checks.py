#!/usr/bin/env python3
"""
Unified sanity checker.

Project layout (example):
API_sanity_checks/
  smart_home/
    interface_1/
    ...
    interface_5/
    get_set_APIs.yaml
  sanity_checks.py
  (autowrites) tools_info.json
  (autowrites) sanity_report.json

What this does:
- Reads GET/SET classification ONLY from get_set_APIs.yaml
- Computes per-interface counts & percentages for GET/SET (no UNKNOWN)
- Detects duplicate API names across different interfaces (from YAML)
- Compares folder files vs YAML:
    * missing_in_yaml: files present in interface folder but not listed in YAML
    * extra_in_yaml: YAML-listed APIs that have no corresponding .py file
- Collects get_info() parameter specs for every API (path-based imports; no package side-effects)
- Parses invoke(...) signature (AST) to get params and compares with get_info():
    * api_records[].params            -> AST params
    * api_records[].param_match       -> True/False
    * api_records[].param_mismatch    -> detail dict
- Writes tools_info.json AND sanity_report.json next to smart_home/
"""

import os
import sys
import json
import re
import ast
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
import importlib.util
import types
import traceback
import yaml
import http.server
import socketserver
import webbrowser


# -------------------- Config --------------------

IGNORED_FILES = {"__init__.py", "policy.md"}
INTERFACE_DIR_NAMES = [f"interface_{i}" for i in range(1, 6)]
YAML_FILENAME = "get_set_APIs.yaml"
TOOLS_INFO_FILENAME = "tools_info.json"  # written next to base_dir
SERVER_PORT = 8000

TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "object": "dict",
    "array": "list",
}

# -------------------- FS helpers --------------------

def discover_interface_dirs(base_dir):
    return [os.path.join(base_dir, name)
            for name in INTERFACE_DIR_NAMES
            if os.path.isdir(os.path.join(base_dir, name))]

def list_api_files(interface_dir):
    """
    Return:
      names: set of api names (lowercased stems)
      paths: dict { api_name_lower: full_path }
    """
    names = set()
    paths = {}
    for entry in os.listdir(interface_dir):
        full = os.path.join(interface_dir, entry)
        if not os.path.isfile(full):
            continue
        if entry in IGNORED_FILES:
            continue
        stem, ext = os.path.splitext(entry)
        if ext.lower() != ".py":
            continue
        api = stem.strip().lower()
        if api:
            names.add(api)
            paths[api] = full
    return names, paths

def percent(part, total):
    if total == 0:
        return 0.0
    return round((part / total) * 100.0, 2)

def load_yaml(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    norm = {}
    for iface, buckets in data.items():
        if not isinstance(buckets, dict):
            continue
        get_list = buckets.get("get") or []
        set_list = buckets.get("set") or []
        norm[iface] = {
            "get": [x.strip().lower() for x in get_list if isinstance(x, str) and x.strip()],
            "set": [x.strip().lower() for x in set_list if isinstance(x, str) and x.strip()],
        }
    return norm

# -------------------- AST param parser (for invoke signature) --------------------

def _unparse(node):
    try:
        return ast.unparse(node)  # py>=3.9
    except Exception:
        return None

def _normalize_type(ann: str | None) -> str:
    if not ann:
        return ""
    s = ann.strip()
    # normalize typing forms to simple ones (best-effort)
    # Optional[T] -> T ; Union[T, None] -> T
    s = re.sub(r"\btyping\.", "", s)
    s = re.sub(r"\bOptional\s*\[\s*([^]\s]+)\s*\]", r"\1", s)
    s = re.sub(r"\bUnion\s*\[\s*([^,\]]+)\s*,\s*NoneType?\s*\]", r"\1", s)
    s = re.sub(r"\bNoneType\b", "None", s)
    # List[T] -> list ; Dict[K,V] -> dict ; Set[T] -> set ; Tuple[...] -> tuple
    s = re.sub(r"\bList\s*\[.*\]", "list", s)
    s = re.sub(r"\bDict\s*\[.*\]", "dict", s)
    s = re.sub(r"\bSet\s*\[.*\]", "set", s)
    s = re.sub(r"\bTuple\s*\[.*\]", "tuple", s)
    # Basic aliases
    s = s.replace("str", "str").replace("int", "int").replace("float", "float").replace("bool", "bool")
    return s

def _is_optional_annotation(ann_str: str | None) -> bool:
    if not ann_str:
        return False
    s = ann_str.replace(" ", "")
    return s.startswith("Optional[") or ("Union[" in s and "None" in s)

def _collect_invoke_signature(py_path):
    """
    Returns {"params": [ {name, type, optional}, ... ]}
    Skips 'self', 'cls', and 'data' params.
    """
    try:
        with open(py_path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src)
    except Exception:
        return {"params": []}

    invoke_func = None

    # find @staticmethod def invoke inside classes
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for fn in node.body:
                if isinstance(fn, ast.FunctionDef) and fn.name == "invoke":
                    is_static = any(
                        (isinstance(dec, ast.Name) and dec.id == "staticmethod") or
                        (isinstance(dec, ast.Attribute) and dec.attr == "staticmethod")
                        for dec in getattr(fn, "decorator_list", [])
                    )
                    if is_static:
                        invoke_func = fn
                        break
        if invoke_func:
            break

    # fallback: module-level def invoke
    if not invoke_func:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "invoke":
                invoke_func = node
                break

    if not invoke_func:
        return {"params": []}

    args = invoke_func.args
    all_args = list(args.args)  # ignore kwonly for simplicity; can be added if you need
    defaults = list(args.defaults or [])
    defaults_pad = [None] * (len(all_args) - len(defaults))
    defaults_aligned = defaults_pad + defaults

    out = []
    for i, a in enumerate(all_args):
        name = a.arg
        if name in ("self", "cls", "data"):
            continue
        ann = _unparse(a.annotation) if getattr(a, "annotation", None) else None
        ann = _normalize_type(ann)
        has_default = defaults_aligned[i] is not None
        is_opt = has_default or _is_optional_annotation(ann)
        out.append({"name": name, "type": ann or "", "optional": bool(is_opt)})
    return {"params": out}

# -------------------- get_info() param collector (path-based; from getting_info.py) --------------------

def snake_to_camel(s: str) -> str:
    return "".join(part.capitalize() for part in s.split("_"))

def mock_tau_bench():
    sys.modules['tau_bench'] = types.ModuleType('tau_bench')
    sys.modules['tau_bench.envs'] = types.ModuleType('tau_bench.envs')
    sys.modules['tau_bench.envs.tool'] = types.ModuleType('tau_bench.envs.tool')
    sys.modules['tau_bench.envs.tool'].Tool = object

def json_schema_type_to_str(t):
    if isinstance(t, list):
        t = next((x for x in t if x != "null"), t[0] if t else None)
    return TYPE_MAP.get(t, "str" if t in (None, "null") else str(t))

def build_params_from_get_info(info: dict):
    fn = (info or {}).get("function", {})
    params_schema = fn.get("parameters", {}) or {}
    props = params_schema.get("properties", {}) or {}
    required = set(params_schema.get("required", []) or [])
    out = []
    for pname, pdef in props.items():
        ptype = pdef.get("type")
        out.append({
            "name": pname,
            "type": json_schema_type_to_str(ptype),
            "optional": (pname not in required)
        })
    return out

def load_module_from_path(module_name: str, file_path: Path):
    try:
        spec = importlib.util.spec_from_file_location(module_name, str(file_path))
        if spec is None or spec.loader is None:
            return None
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = module_name.rpartition('.')[0]
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        # Leave a breadcrumb; keep going
        traceback.print_exc()
        return None

def collect_all_tools_info(base_dir: str):
    """
    Mirrors getting_info.py behavior but returns:
      { "params": [ {interface, api_name, params, name_mismatch}, ... ] }
    """
    mock_tau_bench()
    base = Path(base_dir).resolve()
    results = []

    for iface in INTERFACE_DIR_NAMES:
        iface_dir = base / iface
        if not iface_dir.is_dir():
            continue
        for entry in sorted(os.listdir(iface_dir)):
            full = iface_dir / entry
            if not full.is_file() or entry in IGNORED_FILES:
                continue
            stem, ext = os.path.splitext(entry)
            if ext.lower() != ".py":
                continue

            class_name = snake_to_camel(stem)
            module_name = f"_toolload.{iface}.{stem}"
            mod = load_module_from_path(module_name, full)
            if mod is None:
                continue

            ToolClass = getattr(mod, class_name, None)
            if ToolClass is None:
                continue
            get_info = getattr(ToolClass, "get_info", None)
            if not callable(get_info):
                continue

            try:
                info = get_info()
            except Exception:
                traceback.print_exc()
                continue

            fn_name = ((info or {}).get("function", {}) or {}).get("name")
            mismatch_flag = True
            if isinstance(fn_name, str) and fn_name.strip():
                mismatch_flag = (stem.lower() != fn_name.strip().lower())

            params = build_params_from_get_info(info)
            results.append({
                "interface": iface,
                "api_name": stem,
                "params": params,
                "name_mismatch": mismatch_flag
            })

    payload = {"params": results}
    return payload

def write_tools_info(base_dir: str, payload: dict):
    out_path = Path(base_dir).parent / TOOLS_INFO_FILENAME
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return str(out_path)

def load_tools_info_dict(payload: dict):
    """
    Build lookup: { (interface, api): [params ...] }
    and the set of keys.
    """
    lookup = {}
    keys = set()
    for item in payload.get("params", []):
        iface = item.get("interface")
        api = item.get("api_name")
        params = item.get("params", [])
        if iface and api:
            lookup[(iface, api)] = params
            keys.add((iface, api))
    return lookup, keys

# -------------------- Comparison helpers --------------------

def _norm_type_for_compare(t: str) -> str:
    if not t:
        return ""
    s = t.strip().lower()
    # normalize common typing to base names
    s = s.replace("typing.", "")
    s = s.replace("optional[", "").replace("]", "") if s.startswith("optional[") else s
    for pat, repl in (("list[", "list"), ("dict[", "dict"), ("set[", "set"), ("tuple[", "tuple")):
        if s.startswith(pat):
            s = repl
    return s

def compare_params(parsed_params, tools_params):
    """
    Returns (match_bool, detail_dict) where detail_dict has keys the UI expects:
      - missing_in_tools: [names only in AST/parsed]
      - extra_in_tools:   [names only in tools/get_info]
      - type_or_optional_diff: [
            { "name": str,
              "parsed": {"type": str, "optional": bool},
              "tools":  {"type": str, "optional": bool} },
            ...
        ]
    """
    pp = {p["name"]: {"type": _norm_type_for_compare(p.get("type", "")),
                      "optional": bool(p.get("optional", False))}
          for p in parsed_params}
    tp = {p["name"]: {"type": _norm_type_for_compare(p.get("type", "")),
                      "optional": bool(p.get("optional", False))}
          for p in tools_params}

    names_parsed = set(pp.keys())
    names_tools  = set(tp.keys())

    missing_in_tools = sorted(names_parsed - names_tools)   # only in parsed (AST)
    extra_in_tools   = sorted(names_tools - names_parsed)   # only in tools (get_info)

    type_or_optional_diff = []
    for name in sorted(names_parsed & names_tools):
        a, b = pp[name], tp[name]
        if a["type"] != b["type"] or a["optional"] != b["optional"]:
            type_or_optional_diff.append({
                "name": name,
                "parsed": {"type": a["type"], "optional": a["optional"]},
                "tools":  {"type": b["type"], "optional": b["optional"]},
            })

    match = not (missing_in_tools or extra_in_tools or type_or_optional_diff)
    detail = {
        "missing_in_tools": missing_in_tools,
        "extra_in_tools": extra_in_tools,
        "type_or_optional_diff": type_or_optional_diff
    }
    return match, detail



# -------------------- main --------------------

def main():

    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sanity_report.json")

    if len(sys.argv) != 2:
        print("Usage: python sanity_checks.py <base_folder>")
        sys.exit(1)

    base_dir = os.path.abspath(sys.argv[1])
    if not os.path.isdir(base_dir):
        print(f"❌ Base folder does not exist: {base_dir}", file=sys.stderr)
        sys.exit(2)

    yaml_path = os.path.join(base_dir, YAML_FILENAME)
    if not os.path.isfile(yaml_path):
        print(f"❌ YAML not found: {yaml_path}", file=sys.stderr)
        sys.exit(2)

    # Load YAML (source of truth for GET/SET)
    yaml_map = load_yaml(yaml_path)

    # Locate interface folders
    interface_dirs = discover_interface_dirs(base_dir)
    if not interface_dirs:
        print(f"❌ No interface_* folders found in: {base_dir}", file=sys.stderr)
        sys.exit(2)

    # Per-interface files on disk + map to paths
    files_per_iface = {}
    files_map = {}  # (iface_name, api_name) -> full_path
    for iface_path in interface_dirs:
        iface_name = os.path.basename(iface_path)
        names, paths = list_api_files(iface_path)
        files_per_iface[iface_name] = names
        for api_name, full_path in paths.items():
            files_map[(iface_name, api_name)] = full_path

    # Build counts purely from YAML
    per_interface_counts = {}
    overall = Counter()
    occurrences = defaultdict(list)  # for duplicates

    for iface_name, buckets in yaml_map.items():
        get_list = buckets.get("get", [])
        set_list = buckets.get("set", [])
        total = len(get_list) + len(set_list)
        g, s = len(get_list), len(set_list)

        per_interface_counts[iface_name] = {
            "total_apis": total,
            "get": {"count": g, "percent": percent(g, total)},
            "set": {"count": s, "percent": percent(s, total)},
        }
        overall["total"] += total; overall["get"] += g; overall["set"] += s
        for api in set(get_list + set_list):
            occurrences[api].append(iface_name)

    duplicates = [
        {"api_name": api, "interfaces_involved": sorted(list(set(ifaces)))}
        for api, ifaces in sorted(occurrences.items())
        if len(set(ifaces)) > 1
    ]

    # Compare folder contents vs YAML
    interface_comparisons = {}
    for iface_name in sorted(set(list(files_per_iface.keys()) + list(yaml_map.keys()))):
        files = files_per_iface.get(iface_name, set())
        ym = yaml_map.get(iface_name, {"get": [], "set": []})
        yaml_apis = set(ym.get("get", []) + ym.get("set", []))

        missing_in_yaml = sorted(list(files - yaml_apis))
        extra_in_yaml = sorted(list(yaml_apis - files))

        interface_comparisons[iface_name] = {
            "files_count": len(files),
            "yaml_count": len(yaml_apis),
            "missing_in_yaml": missing_in_yaml,
            "extra_in_yaml": extra_in_yaml,
        }

    overall_summary = {
        "total_apis": overall.get("total", 0),
        "get": {"count": overall.get("get", 0), "percent": percent(overall.get("get", 0), overall.get("total", 0))},
        "set": {"count": overall.get("set", 0), "percent": percent(overall.get("set", 0), overall.get("total", 0))},
    }

    # -------- Collect fresh tools_info (path-based) and write it
    tools_payload = collect_all_tools_info(base_dir)
    tools_info_path = write_tools_info(base_dir, tools_payload)
    tools_lookup, tools_all_keys = load_tools_info_dict(tools_payload)

    # -------- Build api_records (with AST-parsed params + comparison vs tools_info)
# -------- Build api_records (with AST-parsed params + comparison vs tools_info)
    api_records = []
    seen_keys = set()

    for iface_name, buckets in yaml_map.items():
        for cls_name, apis in (("get", buckets.get("get", [])), ("set", buckets.get("set", []))):
            for api in apis:
                parsed_params = []
                fp = files_map.get((iface_name, api))
                if fp:
                    sig = _collect_invoke_signature(fp)
                    parsed_params = sig.get("params", [])
                tools_params = tools_lookup.get((iface_name, api), None)
                if tools_params is None:
                    param_match = False
                    mismatch = {
                        "not_in_tools_info": True,
                        "missing_in_tools": [],
                        "extra_in_tools": [],
                        "type_or_optional_diff": []
                    }
                else:
                    param_match, mismatch = compare_params(parsed_params, tools_params)

                api_records.append({
                    "interface": iface_name,
                    "api_name": api,
                    "classification": cls_name,
                    "params": parsed_params,            # AST parsed
                    "param_match": param_match,         # matches get_info()?
                    "param_mismatch": mismatch,
                    "param_diff_summary": mismatch.get("summary", [])   # <-- add this
                })
                seen_keys.add((iface_name, api))


    # tools_info entries not in YAML
    extra_apis_in_tools_info = sorted(
        [{"interface": i, "api_name": a} for (i, a) in tools_all_keys if (i, a) not in seen_keys],
        key=lambda x: (x["interface"], x["api_name"])
    )

    report = {
        "base_folder": base_dir,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "interfaces": sorted(list(set(list(yaml_map.keys()) + [os.path.basename(p) for p in interface_dirs]))),
        "ignored_files": sorted(list(IGNORED_FILES)),
        "yaml_path": yaml_path,
        "tools_info_path": tools_info_path,
        "summary": {
            "interfaces": per_interface_counts,
            "overall": overall_summary
        },
        "duplicates": duplicates,
        "interface_file_yaml_comparison": interface_comparisons,
        "extra_apis_in_tools_info": extra_apis_in_tools_info,
        "apis": api_records
    }

    # Write the report OUTSIDE the base folder (next to it)
    out_path = os.path.join(os.path.dirname(base_dir), "sanity_report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # ------- Console output -------
    print("\n=== Per-Interface Summary (from YAML) ===")
    for iface in sorted(per_interface_counts.keys()):
        s = per_interface_counts[iface]
        print(f"- {iface}: total={s['total_apis']} | "
              f"GET {s['get']['count']} ({s['get']['percent']}%), "
              f"SET {s['set']['count']} ({s['set']['percent']}%)")

    if duplicates:
        print("\n=== Duplicate API Names Across Interfaces (YAML) ===")
        for d in duplicates:
            print(f"- {d['api_name']}: {', '.join(d['interfaces_involved'])}")
    else:
        print("\n=== Duplicate API Names Across Interfaces (YAML) ===\n- None")

    print("\n=== Folder vs YAML Checks ===")
    for iface in sorted(interface_comparisons.keys()):
        comp = interface_comparisons[iface]
        print(f"\n  {iface}: files={comp['files_count']} | yaml={comp['yaml_count']}")
        print("    Files not in YAML:", ", ".join(comp["missing_in_yaml"]) or "None")
        print("    YAML entries missing files:", ", ".join(comp["extra_in_yaml"]) or "None")

    print(f"\n📝 Wrote tools_info.json to: {tools_info_path}")
    print(f"📝 Wrote sanity report to: {out_path}")
    print(f"📊 Overall — total: {overall_summary['total_apis']}, "
          f"get: {overall_summary['get']['count']} ({overall_summary['get']['percent']}%), "
          f"set: {overall_summary['set']['count']} ({overall_summary['set']['percent']}%)")

    # Serve the dashboard and open in browser
    web_dir = os.path.dirname(OUTPUT_FILE)
    os.chdir(web_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", SERVER_PORT), handler) as httpd:
        url = f"http://localhost:{SERVER_PORT}/"
        print(f"[INFO] Serving at {url}")
        webbrowser.open(url)
        httpd.serve_forever()

if __name__ == "__main__":
    main()

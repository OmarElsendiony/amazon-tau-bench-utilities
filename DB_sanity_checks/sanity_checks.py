import os
import json
import pandas as pd
import yaml
import http.server
import socketserver
import argparse
import webbrowser
from datetime import datetime

SERVER_PORT = 1000

def load_json_as_df(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame.from_dict(data, orient="index")
    return df, data

def load_enum_defs(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("enums", {})
    except Exception as e:
        print(f"[ERROR] Failed to load enums file '{file_path}': {e}")
        return {}

# After loading your YAML enum_defs, add this fix:
def fix_yaml_boolean_conversion(enum_defs):
    for table_name, table_enums in enum_defs.items():
        for col_name, allowed_values in table_enums.items():
            # Convert any boolean values back to their string equivalents
            fixed_values = []
            for val in allowed_values:
                if val is True:
                    fixed_values.append("on")
                elif val is False:
                    fixed_values.append("off")
                else:
                    fixed_values.append(val)
            enum_defs[table_name][col_name] = fixed_values
    
    return enum_defs

def sanity_check_keys_are_strings(table_name, data, report):
    all_str = all(isinstance(k, str) for k in data.keys())
    report["checks"].append({"check": "Keys are strings", "result": all_str})
    print(f"[{'PASS' if all_str else 'FAIL'}] {table_name}: Keys are strings")
    return all_str

def sanity_check_id_matches_key(table_name, data, report):
    first_record = next(iter(data.values()), None)
    if not first_record:
        report["checks"].append({"check": "File not empty", "result": False})
        print(f"[WARN] {table_name}: File is empty")
        return False

    id_field = [col for col in first_record.keys() if col.endswith("_id")]
    if not id_field:
        report["checks"].append({"check": "Has *_id field", "result": False})
        print(f"[FAIL] {table_name}: No *_id field")
        return False

    id_field = id_field[0]
    all_match = all(str(v.get(id_field, "")) == str(k) for k, v in data.items())
    report["checks"].append({"check": f"{id_field} matches key", "result": all_match})
    print(f"[{'PASS' if all_match else 'FAIL'}] {table_name}: {id_field} matches key")
    return all_match

# New check: primary keys directly from JSON keys

def sanity_check_pk_from_json(table_name, data, report):

    keys = list(data.keys())

    # Ensure no empty or null keys

    non_null = all(k not in (None, "") for k in keys)

    report["checks"].append({"check": "Primary keys non-null", "result": non_null})

    print(f"[{'PASS' if non_null else 'FAIL'}] {table_name}: Primary keys non-null")



    # Ensure uniqueness of keys

    unique = len(keys) == len(set(keys))

    report["checks"].append({"check": "Primary keys unique", "result": unique})

    print(f"[{'PASS' if unique else 'FAIL'}] {table_name}: Primary keys unique")



    return non_null and unique

def sanity_check_enums(table_name, df, enum_defs, report):
    if table_name not in enum_defs:
        return True

    table_enums = enum_defs[table_name]
    all_valid   = True

    for col, allowed in table_enums.items():
        if col not in df.columns:
            continue

        # find invalid values
        actual_values = df[col].dropna().unique()
        print(f"DEBUG: {col} - actual values: {actual_values}")
        print(f"DEBUG: {col} - actual values types: {[type(v) for v in actual_values]}")
        print(f"DEBUG: {col} - allowed values: {allowed}")
        print(f"DEBUG: {col} - allowed values types: {[type(v) for v in allowed]}")
        print(f"DEBUG: {col} - actual repr: {[repr(v) for v in actual_values]}")
        print(f"DEBUG: {col} - allowed repr: {[repr(v) for v in allowed]}")
        
        invalid_vals = set(actual_values) - set(allowed)
        print(f"DEBUG: {col} - invalid values: {invalid_vals}")
        
        valid = len(invalid_vals) == 0
        all_valid &= valid

        # sample up to 5 record-keys where invalids occur
        sample_keys = []
        if not valid:
            mask = df[col].isin(invalid_vals)
            sample_keys = df.index[mask].tolist()[:5]

        report["checks"].append({
            "check":   f"{col} in enum",
            "result":  valid,
            "details": {
                "invalid_values": list(invalid_vals)[:5],
                "sample_keys":    sample_keys
            }
        })

        status = "PASS" if valid else "FAIL"
        print(f"[{status}] {table_name}.{col}: invalid values = {invalid_vals}; sample keys = {sample_keys}")

    return all_valid


def normalize_type(t):
    s = str(t).strip().upper()
    if s == "61":   # YAML 1.1 sexagesimal for 1:1
        s = "1:1"
    if s not in {"1:1", "1:N", "M:N"}:
        raise ValueError(f"Unsupported relationship type: {t!r}")
    return s

def check_foreign_keys(relationships, dfs, report):
    """
    relationships: list of dicts like:
      {
        "parent_table": "funds",
        "parent_column": "fund_id",
        "child_table": "portfolio_holdings",
        "child_column": "fund_id",
        "type": "1:1" | "1:N" | "M:N",
        # optional:
        "mandatory": False,           # if True, enforce full coverage (1:1 exactly once; 1:N at least once)
        "min_children": None,         # only for 1:N
        "max_children": None,         # only for 1:N
        # for M:N only (when child_table is a link table):
        "link_parent_column": None,   # e.g., "fund_id"
        "link_child_column": None     # e.g., "portfolio_id"
      }

    dfs: dict[str, pandas.DataFrame]
    report: dict with a "relationships": list to append records to
    """
    for rel in relationships:
        p_table = rel["parent_table"]
        p_col   = rel["parent_column"]
        c_table = rel["child_table"]
        c_col   = rel["child_column"]
        rtype_raw   = rel["type"]
        rtype = normalize_type(rtype_raw)
        mandatory    = rel.get("mandatory", False)
        min_children = rel.get("min_children")
        max_children = rel.get("max_children")

        check_name = f"{p_table}.{p_col} → {c_table}.{c_col}"

        # Skip if missing tables
        if p_table not in dfs or c_table not in dfs:
            report["relationships"].append({
                "relationship": check_name,
                "check": "Tables present",
                "result": False,
                "details": {"reason": "Missing table(s)"}
            })
            continue

        parent_df = dfs[p_table]
        child_df  = dfs[c_table]

        # Basic column existence check (useful in evolving seeds)
        for tname, df, col, role in ((p_table, parent_df, p_col, "parent"),
                                     (c_table, child_df, c_col, "child")):
            exists = col in df.columns
            report["relationships"].append({
                "relationship": check_name,
                "check": f"{role.capitalize()} column exists",
                "result": exists,
                "details": {"table": tname, "column": col}
            })
            if not exists:
                # If a critical column is missing, no further checks can run
                # (but still continue to next relationship rather than raising)
                parent_missing = (role == "parent")
                # Only break once we’ve appended both existence checks
                break
        if p_col not in parent_df.columns or c_col not in child_df.columns:
            continue

        # Normalize types where possible to reduce false negatives on isin
        p_series = parent_df[p_col]
        c_series = child_df[c_col]
        # If dtypes mismatch in int/str, try best-effort cast of child to parent dtype
        try:
            c_cast = c_series.astype(p_series.dtype, copy=False)
        except Exception:
            c_cast = c_series  # fall back silently

        # Null handling
        null_count = c_cast.isna().sum()
        non_null = c_cast.dropna()

        report["relationships"].append({
            "relationship": check_name,
            "check": "Child column nulls",
            "result": True,  # informative metric
            "details": {"column": c_col, "null_count": int(null_count), "non_null_count": int(non_null.shape[0])}
        })

        # 1) All children have parents (referential integrity)
        missing_mask  = ~non_null.isin(p_series)
        missing_ids   = non_null[missing_mask].unique().tolist()
        total_missing = len(missing_ids)
        exists_ok     = total_missing == 0
        report["relationships"].append({
            "relationship": check_name,
            "check": "All children have parents",
            "result": exists_ok,
            "details": {"column": c_col, "missing_ids_sample": missing_ids[:5], "count": total_missing}
        })
        print(f"[{'PASS' if exists_ok else 'FAIL'}] {check_name} – {total_missing} missing IDs in `{c_col}`")

        # 2) Parent column unique (PK-like)
        dup_parents   = p_series[p_series.duplicated(keep=False)].unique().tolist()
        total_dups    = len(dup_parents)
        parent_unique = total_dups == 0
        report["relationships"].append({
            "relationship": check_name,
            "check": "Parent column unique",
            "result": parent_unique,
            "details": {"column": p_col, "duplicate_parent_ids_sample": dup_parents[:5], "count": total_dups}
        })
        print(f"[{'PASS' if parent_unique else 'FAIL'}] {p_table}.{p_col} – {total_dups} duplicates")

        # Cardinality-specific checks
        if rtype == "1:1":
            # 3a) Child column unique (no parent referenced more than once)
            dup_children = non_null[non_null.duplicated(keep=False)].unique().tolist()
            total_child_dups = len(dup_children)
            child_unique = total_child_dups == 0
            report["relationships"].append({
                "relationship": check_name,
                "check": "Child column unique (1:1)",
                "result": child_unique,
                "details": {"column": c_col, "duplicate_child_ids_sample": dup_children[:5], "count": total_child_dups}
            })
            print(f"[{'PASS' if child_unique else 'FAIL'}] {c_table}.{c_col} – {total_child_dups} duplicates")

            # 3b) Coverage: if mandatory 1:1, every parent must appear exactly once in child
            if mandatory:
                # parents that appear in child
                used_parents = set(non_null.unique().tolist())
                all_parents  = set(p_series.unique().tolist())
                missing_parents = list(all_parents - used_parents)
                extra_refs      = list(used_parents - all_parents)  # should be empty if check #1 passed

                # check exact multiplicity == 1
                vc = non_null.value_counts(dropna=False)
                not_exact_one = vc[vc != 1].index.tolist()  # parents referenced 0 or >1 times are already covered by missing/dup
                ok = (len(missing_parents) == 0) and (len(not_exact_one) == 0)

                report["relationships"].append({
                    "relationship": check_name,
                    "check": "Mandatory 1:1 coverage (each parent exactly once)",
                    "result": ok,
                    "details": {
                        "missing_parent_ids_sample": missing_parents[:5],
                        "over_or_under_referenced_ids_sample": not_exact_one[:5],
                        "missing_count": len(missing_parents),
                        "over_or_under_count": len(not_exact_one)
                    }
                })
                status = 'PASS' if ok else 'FAIL'
                print(f"[{status}] {check_name} – mandatory 1:1 coverage")

        elif rtype == "1:N":
            # 3c) Distribution stats
            vc = non_null.value_counts()
            avg_count = round(float(vc.mean()), 2) if not vc.empty else 0.0
            min_count = int(vc.min()) if not vc.empty else 0
            max_count = int(vc.max()) if not vc.empty else 0
            # Top parents by load
            top5 = vc.sort_values(ascending=False).head(5).to_dict()

            report["relationships"].append({
                "relationship": check_name,
                "check": "Children per parent (distribution)",
                "result": True,  # informative
                "details": {
                    "avg": avg_count, "min": min_count, "max": max_count,
                    "top5_parents_by_children": top5
                }
            })
            print(f"[INFO] {check_name}: avg={avg_count:.2f}, min={min_count}, max={max_count}")

            # 3d) Optional policy bounds
            if min_children is not None:
                below = vc[vc < min_children]
                ok = below.empty
                report["relationships"].append({
                    "relationship": check_name,
                    "check": f"Min children per parent ≥ {min_children}",
                    "result": ok,
                    "details": {
                        "violating_parent_ids_sample": below.index.tolist()[:5],
                        "violations": int((vc < min_children).sum())
                    }
                })
            if max_children is not None:
                above = vc[vc > max_children]
                ok = above.empty
                report["relationships"].append({
                    "relationship": check_name,
                    "check": f"Max children per parent ≤ {max_children}",
                    "result": ok,
                    "details": {
                        "violating_parent_ids_sample": above.index.tolist()[:5],
                        "violations": int((vc > max_children).sum())
                    }
                })

            # 3e) Mandatory coverage: each parent appears at least once
            if mandatory:
                used_parents = set(non_null.unique().tolist())
                all_parents  = set(parent_df[p_col].unique().tolist())
                missing_parents = list(all_parents - used_parents)
                ok = (len(missing_parents) == 0)
                report["relationships"].append({
                    "relationship": check_name,
                    "check": "Mandatory 1:N coverage (each parent at least once)",
                    "result": ok,
                    "details": {
                        "missing_parent_ids_sample": missing_parents[:5],
                        "missing_count": len(missing_parents)
                    }
                })

        elif rtype == "M:N":
            # Here, c_table is assumed to be a link table with two FK columns
            lp = rel.get("link_parent_column")
            lc = rel.get("link_child_column")
            ok_meta = bool(lp and lc and lp in child_df.columns and lc in child_df.columns)
            report["relationships"].append({
                "relationship": f"{c_table} ({lp},{lc})",
                "check": "Link columns present (M:N)",
                "result": ok_meta,
                "details": {"table": c_table, "parent_link_col": lp, "child_link_col": lc}
            })
            if ok_meta:
                # Uniqueness of pairs (no duplicate relationships)
                pair_dups = (
                    child_df[[lp, lc]]
                    .assign(_pair=lambda d: d[lp].astype(str) + "§" + d[lc].astype(str))
                )
                dup_pairs = pair_dups["_pair"][pair_dups["_pair"].duplicated(keep=False)].unique().tolist()
                ok_pairs = len(dup_pairs) == 0
                report["relationships"].append({
                    "relationship": f"{c_table} ({lp},{lc})",
                    "check": "Composite uniqueness (parent, child)",
                    "result": ok_pairs,
                    "details": {
                        "duplicate_pairs_sample": dup_pairs[:5],
                        "count": len(dup_pairs)
                    }
                })
                # Existence for both sides
                # Parent side
                parent_exists = child_df[lp].dropna().isin(parent_df[p_col]).all()
                report["relationships"].append({
                    "relationship": f"{p_table}.{p_col} → {c_table}.{lp}",
                    "check": "All link parent IDs have parents",
                    "result": parent_exists,
                    "details": {}
                })
                # Child side existence requires child entity DF; you can pass another rel for that side
            else:
                # Nothing else can be done for this M:N without proper link columns
                pass

        else:
            # Unknown type (record it but don't fail the whole run)
            report["relationships"].append({
                "relationship": check_name,
                "check": "Unknown relationship type",
                "result": False,
                "details": {"type": rtype}
            })

import json
import pandas as pd

def check_generic_foreign_keys(gfk_configs, dfs, report):
    """
    gfk_configs: list of dicts, each like:
      {
        "child_table": "page_version_components",
        "type_column": "component_type",
        "id_column": "component_data",
        "json_column": "component_data",      # Optional: the JSON column
        "mapping": {
          "whiteboard": {
            "parent_table": "whiteboards",
            "parent_column": "whiteboard_id",
            "json_id_key": "whiteboard_id"    # Optional: key to extract from JSON
          },
          "smart_link": {
            "parent_table": "smart_links",
            "parent_column": "smart_link_id",
            "json_id_key": "smart_link_id"
          }
        }
      }
    """
    if "relationships" not in report:
        report["relationships"] = []

    def add_result(relationship, check, result, details=None, kind="generic"):
        report["relationships"].append({
            "relationship": relationship,
            "check": check,
            "result": result,
            "details": details or {},
            "kind": kind
        })

    table_columns = {t: set(df.columns) for t, df in dfs.items()}

    for cfg in (gfk_configs or []):
        child_table = cfg.get("child_table")
        type_col    = cfg.get("type_column")
        id_col      = cfg.get("id_column")
        mapping     = cfg.get("mapping", {})
        json_col    = cfg.get("json_column")

        rel_label = f"{child_table}.{id_col} (type via {type_col})"
        if not child_table or child_table not in dfs:
            add_result(rel_label, "Child table present", False, {"child_table": child_table})
            print(f"[FAIL] {rel_label} – child table missing: {child_table}")
            continue

        child_df = dfs[child_table]

        # Basic column existence check
        for col_name, label in [(type_col, "type column"), (id_col, "id column")]:
            if not col_name or col_name not in child_df.columns:
                add_result(rel_label, f"Child {label} present", False, {"column": col_name})
                print(f"[FAIL] {rel_label} – missing child {label}: {col_name}")
                continue

        # 0) Type coverage sanity
        type_values = child_df[type_col].dropna().astype(str).unique().tolist()
        mapped_types = set(mapping.keys())
        data_types   = set(type_values)

        unmapped_types = sorted(list(data_types - mapped_types))
        stale_mapping  = sorted(list(mapped_types - data_types))

        add_result(rel_label, "All type values are mapped", len(unmapped_types) == 0,
                   {"unmapped_types": unmapped_types[:10], "count": len(unmapped_types)})
        print(f"[{'PASS' if len(unmapped_types)==0 else 'FAIL'}] {rel_label} – {len(unmapped_types)} unmapped type(s)")

        if stale_mapping:
            add_result(rel_label, "Stale mapping entries (info)", True,
                       {"stale_types": stale_mapping[:10], "count": len(stale_mapping)})
            print(f"[INFO] {rel_label} – {len(stale_mapping)} stale mapping type(s) in config")

        # 1) Per-type parent existence check (+ metrics)
        for tval in sorted(data_types):
            if tval not in mapping:
                continue

            m = mapping[tval] or {}
            p_table = m.get("parent_table")
            p_col   = m.get("parent_column")
            json_id_key_for_type = m.get("json_id_key")  # FIX: Get from TYPE mapping, not config
            relationship_name = f"{child_table}.{id_col} (type='{tval}') → {p_table}.{p_col}"

            # Validate parent table/column presence
            if p_table not in dfs or not p_col or p_col not in dfs.get(p_table, pd.DataFrame()).columns:
                add_result(relationship_name, "Parent table/column present", False,
                           {"parent_table": p_table, "parent_column": p_col})
                print(f"[FAIL] {relationship_name} – missing parent table/column")
                continue

            parent_df = dfs[p_table]
            parent_ids = set(parent_df[p_col].dropna().astype(str).tolist())

            # Type mask
            type_mask = child_df[type_col] == tval
            
            # FIXED: Extract IDs from JSON using the TYPE-SPECIFIC key
            if json_col and json_id_key_for_type and json_col in child_df.columns:
                ids_list = []
                for json_str in child_df.loc[type_mask, json_col].dropna():
                    try:
                        data = json.loads(json_str)
                        if isinstance(data, dict) and json_id_key_for_type in data:
                            extracted_id = data[json_id_key_for_type]
                            if extracted_id is not None:
                                ids_list.append(str(extracted_id))
                    except (json.JSONDecodeError, TypeError):
                        pass
                ids = pd.Series(ids_list)
            else:
                # Normal case: ID is directly in the column
                ids = child_df.loc[type_mask, id_col].dropna().astype(str)

            # 1a) Existence (referential integrity)
            missing_mask = ~ids.isin(parent_ids)
            missing_ids = ids[missing_mask].unique().tolist()
            total_missing = len(missing_ids)

            add_result(relationship_name, "All children have parents (polymorphic)", total_missing == 0,
                       {"type": tval, "child_column": id_col, "missing_ids": missing_ids[:5], "count": total_missing})
            print(f"[{'PASS' if total_missing==0 else 'FAIL'}] {relationship_name} – missing {total_missing} ID(s)")

            # 1b) Metrics: average & max children per parent
            vc = ids.value_counts()
            avg_children = round(float(vc.mean()), 2) if not vc.empty else 0.0
            max_children = int(vc.max()) if not vc.empty else 0
            add_result(relationship_name, "Average children per parent (info)", avg_children,
                       {"type": tval, "max_children_for_single_parent": max_children})
            print(f"[INFO] {relationship_name}: Avg children/parent = {avg_children:.2f}, Max = {max_children}")

            # 1c) Action policy (optional)
            allowed_actions = set((m.get("allowed_actions") or []))
            if allowed_actions and "action" in child_df.columns:
                actions = child_df.loc[type_mask, "action"].dropna().astype(str)
                invalid = actions[~actions.isin(allowed_actions)]
                invalid_count = int(invalid.shape[0])
                sample = invalid.head(5).tolist()
                add_result(relationship_name, "Action allowed for type", invalid_count == 0,
                           {"type": tval, "invalid_actions": sample, "count": invalid_count,
                            "allowed_actions": sorted(list(allowed_actions))})
                print(f"[{'PASS' if invalid_count==0 else 'FAIL'}] {relationship_name} – {invalid_count} invalid action(s)")

            # 1d) field_name validity (optional)
            if "field_name" in child_df.columns:
                field_series = child_df.loc[type_mask, "field_name"].dropna().astype(str)
                if not field_series.empty:
                    valid_cols = table_columns.get(p_table, set())
                    invalid_fields = field_series[~field_series.isin(valid_cols)]
                    inv_count = int(invalid_fields.shape[0])
                    sample_inv = invalid_fields.head(5).tolist()
                    add_result(relationship_name, "field_name valid for parent type", inv_count == 0,
                               {"type": tval, "invalid_field_names": sample_inv, "count": inv_count,
                                "parent_table_columns_sample": list(sorted(list(valid_cols)))[:10]})
                    print(f"[{'PASS' if inv_count==0 else 'FAIL'}] {relationship_name} – {inv_count} invalid field_name value(s)")

            # 1e) Temporal sanity (optional)
            child_has_ts  = "created_at" in child_df.columns
            parent_has_ts = "created_at" in parent_df.columns
            if child_has_ts and parent_has_ts and not ids.empty:
                # Build alignment: ids -> child timestamps
                c_rows = child_df.loc[type_mask, ["created_at"]].reset_index(drop=True)
                if len(c_rows) == len(ids):
                    c_rows["_pid"] = ids.reset_index(drop=True).values
                    p_rows = parent_df[[p_col, "created_at"]].rename(columns={p_col: "_pid"})
                    merged = pd.merge(c_rows, p_rows, how="left", on="_pid")
                    cts = pd.to_datetime(merged["created_at_x"], errors="coerce", utc=True)
                    pts = pd.to_datetime(merged["created_at_y"], errors="coerce", utc=True)
                    bad_order = (cts < pts) & pts.notna() & cts.notna()
                    viol_count = int(bad_order.sum())
                    add_result(relationship_name, "created_at sequence valid (child ≥ parent)", viol_count == 0,
                               {"type": tval, "violations": int(viol_count)})
                    print(f"[{'PASS' if viol_count==0 else 'FAIL'}] {relationship_name} – {viol_count} temporal violation(s)")

        # 2) User link validity (if applicable)
        if "user_id" in child_df.columns:
            if "users" in dfs and "user_id" in dfs["users"].columns:
                user_ids = set(dfs["users"]["user_id"].dropna().tolist())
                non_null_u = child_df["user_id"].dropna()
                missing_users = non_null_u[~non_null_u.isin(user_ids)].unique().tolist()
                miss_count = len(missing_users)
                add_result(f"{child_table}.user_id → users.user_id", "All children have valid users", miss_count == 0,
                           {"missing_user_ids": missing_users[:5], "count": miss_count})
                print(f"[{'PASS' if miss_count==0 else 'FAIL'}] {child_table}.user_id → users.user_id – missing {miss_count} user(s)")
            else:
                add_result(f"{child_table}.user_id → users.user_id", "Users table present", False,
                           {"reason": "users table or user_id column not found"})
                print(f"[FAIL] {child_table}.user_id → users.user_id – users table/column missing")
                
def main(folder):

    DATA_DIR    = os.path.join(folder, "data")
    REL_FILE    = os.path.join(folder, "relationships.yaml")
    ENUM_FILE   = os.path.join(folder, "enums.yaml")
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sanity_report.json")

    # Ensure data and relationship files exist
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Data directory '{DATA_DIR}' not found.")
        return
    if not os.path.exists(REL_FILE):
        print(f"[ERROR] Relationships file '{REL_FILE}' not found.")
        return

    # Load enum definitions
    enum_defs = load_enum_defs(ENUM_FILE)
    enum_defs = fix_yaml_boolean_conversion(enum_defs)

    # Initialize report (added generic containers)
    sanity_report = {
        "timestamp": datetime.now().isoformat(),
        "tables": {},
        "enum_tables": {},
        "relationships": [],
        "generic_relationships": [],   # ← for index.html separate section
        "generic_fk_summary": {}       # ← quick summary numbers for header/widgets
    }

    # Load dataframes
    dfs = {}
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue

        table_name = filename.replace(".json", "")
        file_path = os.path.join(DATA_DIR, filename)

        try:
            df, data = load_json_as_df(file_path)
        except Exception as e:
            print(f"[ERROR] Failed to read {filename}: {e}")
            continue

        dfs[table_name] = df
        sanity_report["tables"][table_name] = {
            "row_count": len(df),
            "checks": []
        }
        sanity_report["enum_tables"][table_name] = []

        # Run existing per-table checks
        report_entry = sanity_report["tables"][table_name]
        sanity_check_keys_are_strings(table_name, data, report_entry)
        sanity_check_id_matches_key(table_name, data, report_entry)
        sanity_check_pk_from_json(table_name, data, report_entry)

        # Enum validity checks into enum_tables section
        enum_report = {"checks": sanity_report["enum_tables"][table_name]}
        sanity_check_enums(table_name, df, enum_defs, enum_report)

    # Load relationships YAML (support both normal and generic FKs)
    with open(REL_FILE, "r", encoding="utf-8") as f:
        rel_yaml = yaml.safe_load(f) or {}

    relationships = rel_yaml.get("foreign_keys", []) or []
    gfk_configs   = rel_yaml.get("generic_foreign_keys", []) or []

    # 1) Normal FK checks
    if relationships:
        check_foreign_keys(relationships, dfs, sanity_report)
    else:
        print("[INFO] No 'foreign_keys' entries found in relationships.yaml")

    # 2) Generic (polymorphic) FK checks
    if gfk_configs:
        # This function appends entries into sanity_report["relationships"] with kind="generic"
        check_generic_foreign_keys(gfk_configs, dfs, sanity_report)
    else:
        print("[INFO] No 'generic_foreign_keys' entries found in relationships.yaml")

    # 3) Build a dedicated section for generic checks for index.html rendering
    generic_entries = [r for r in sanity_report["relationships"] if r.get("kind") == "generic"]
    sanity_report["generic_relationships"] = generic_entries

    # 4) Compute a compact summary for quick display (counts)
    #    - total checks
    #    - passes / fails
    #    - info metrics (numeric results)
    total = len(generic_entries)
    passes = sum(1 for r in generic_entries if isinstance(r.get("result"), bool) and r["result"] is True)
    fails  = sum(1 for r in generic_entries if isinstance(r.get("result"), bool) and r["result"] is False)

    # numeric/info-style results: capture averages etc. for possible small charts
    info_numeric = []
    for r in generic_entries:
        if not isinstance(r.get("result"), bool):
            info_numeric.append({
                "relationship": r.get("relationship"),
                "check": r.get("check"),
                "value": r.get("result")
            })

    sanity_report["generic_fk_summary"] = {
        "total_checks": total,
        "passes": passes,
        "fails": fails,
        "info_metrics_count": len(info_numeric)
    }

    # Write out the complete report
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sanity_report, f, indent=2)

    print(f"[INFO] Sanity report saved to {OUTPUT_FILE}")

    # Serve the dashboard and open in browser
    web_dir = os.path.dirname(OUTPUT_FILE)
    os.chdir(web_dir)
    handler = http.server.SimpleHTTPRequestHandler
    SERVER_PORT = 8002
    with socketserver.TCPServer(("", SERVER_PORT), handler) as httpd:
        url = f"http://localhost:{SERVER_PORT}/"
        print(f"[INFO] Serving at {url}")
        webbrowser.open(url)
        httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run sanity checks for a data folder.")
    parser.add_argument("folder", help="Target folder (e.g., smart_home)")
    parser.add_argument("--port", type=int, default=8001, help="Port for HTTP server")

    args = parser.parse_args()

    # If your run_checks already defaults to: copy index, serve, and port 8000:
    main(args.folder)

    # If your run_checks requires those args, call with explicit defaults:
    # run_checks(
    #     folder=args.folder,
    #     index_template_path=os.path.join(os.path.dirname(__file__), "index.html"),
    #     copy_index=True,
    #     serve=True,
    #     port=8000
    # )


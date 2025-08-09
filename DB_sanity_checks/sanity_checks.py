import os
import json
import pandas as pd
import yaml
import http.server
import socketserver
import argparse
import webbrowser
from datetime import datetime

SERVER_PORT = 8000

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


def check_foreign_keys(relationships, dfs, report):
    for rel in relationships:
        p_table, p_col = rel["parent_table"], rel["parent_column"]
        c_table, c_col = rel["child_table"],  rel["child_column"]
        rel_type      = rel["type"]
        check_name    = f"{p_table}.{p_col} → {c_table}.{c_col}"
        if p_table not in dfs or c_table not in dfs:
            continue

        parent_df = dfs[p_table]
        child_df  = dfs[c_table]
        non_null  = child_df[c_col].dropna()

        # 1) All children have parents
        missing_mask   = ~non_null.isin(parent_df[p_col])
        missing_ids    = non_null[missing_mask].unique().tolist()
        total_missing  = len(missing_ids)
        top5_missing   = missing_ids[:5]
        exists_ok      = total_missing == 0
        report["relationships"].append({
            "relationship": check_name,
            "check":        "All children have parents",
            "result":       exists_ok,
            "details": {
                "column":      c_col,
                "missing_ids": top5_missing,
                "count":       total_missing
            }
        })
        print(f"[{'PASS' if exists_ok else 'FAIL'}] {check_name} – missing {total_missing} IDs in `{c_col}`")

        # 2) Parent column must be unique
        dup_parents   = parent_df[p_col][parent_df[p_col].duplicated(keep=False)].unique().tolist()
        total_dups    = len(dup_parents)
        top5_parents  = dup_parents[:5]
        parent_unique = total_dups == 0
        report["relationships"].append({
            "relationship": check_name,
            "check":        "Parent column unique",
            "result":       parent_unique,
            "details": {
                "column":                p_col,
                "duplicate_parent_ids":  top5_parents,
                "count":                 total_dups
            }
        })
        print(f"[{'PASS' if parent_unique else 'FAIL'}] {p_table}.{p_col} – {total_dups} duplicates")

        # 3) Depending on relationship type…
        if rel_type == "1:1":
            dup_children     = child_df[c_col][child_df[c_col].duplicated(keep=False)].unique().tolist()
            total_child_dups = len(dup_children)
            top5_children    = dup_children[:5]
            child_unique     = total_child_dups == 0
            report["relationships"].append({
                "relationship": check_name,
                "check":        "Child column unique",
                "result":       child_unique,
                "details": {
                    "column":               c_col,
                    "duplicate_child_ids":  top5_children,
                    "count":               total_child_dups
                }
            })
            print(f"[{'PASS' if child_unique else 'FAIL'}] {c_table}.{c_col} – {total_child_dups} duplicates")

        elif rel_type == "1:N":
            avg_count = non_null.value_counts().mean()
            report["relationships"].append({
                "relationship": check_name,
                "check":        "Average children per parent",
                "result":       avg_count,
                "details":      {}
            })
            print(f"[INFO] {check_name}: Avg children per parent = {avg_count:.2f}")



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

    # Initialize report, now including an enum_tables section
    sanity_report = {
        "timestamp": datetime.now().isoformat(),
        "tables": {},
        "enum_tables": {},
        "relationships": []
    }

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
        # Prepare an empty list for enum checks
        sanity_report["enum_tables"][table_name] = []

        # Run existing checks
        report_entry = sanity_report["tables"][table_name]
        sanity_check_keys_are_strings(table_name, data, report_entry)
        sanity_check_id_matches_key(table_name, data, report_entry)
        sanity_check_pk_from_json(table_name, data, report_entry)

        # Run enum validity checks into the separate enum_tables section
        enum_report = {"checks": sanity_report["enum_tables"][table_name]}
        sanity_check_enums(table_name, df, enum_defs, enum_report)

    # Load and validate foreign key relationships
    with open(REL_FILE, "r", encoding="utf-8") as f:
        relationships = yaml.safe_load(f).get("foreign_keys", [])
    check_foreign_keys(relationships, dfs, sanity_report)

    # Write out the complete report
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sanity_report, f, indent=2)

    print(f"[INFO] Sanity report saved to {OUTPUT_FILE}")

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
    parser = argparse.ArgumentParser(description="Run sanity checks for a data folder.")
    parser.add_argument("folder", help="Target folder (e.g., smart_home)")
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


# amazon-tau-bench-utilities


# Database Sanity Checks

This utility runs a set of **generic sanity checks** on JSON-based database dumps and displays the results in an interactive HTML dashboard.

## 📂 Project Structure

```
DB_sanity_checks
├── sanity_checks.py      # Main script to run checks and serve dashboard
├── index.html            # Dashboard UI (fetches sanity_report.json)
└── <DB_FOLDER>/          # Target database folder (e.g., smart_home)
    ├── data/             # JSON files (tables)
    ├── relationships.yaml
    └── enums.yaml
```

## 🚀 How to Run

1. Prepare your target folder (e.g., `smart_home`) with:

   ```
   smart_home/data/*.json
   smart_home/relationships.yaml
   smart_home/enums.yaml
   ```
2. Run the script:

   ```bash
   python sanity_checks.py smart_home
   ```
3. The script will:

   * Generate `sanity_report.json`
   * Serve the dashboard at **[http://localhost:8000/](http://localhost:8000/)**
   * Open your default browser to view the results

Here is a video **[demo](https://drive.google.com/file/d/19apuwtwPeDZ6_lm7f5tQXyaU-Nmio3In/view?usp=drive_link)** on how to use this utility. 

## 🧪 Checks Performed

* **Table checks**

  * Keys are strings
  * Primary key matches JSON key
  * PK presence check
* **Relationship checks**

  * All children have valid parents
  * Parent column uniqueness
* **Enum checks**

  * Values match defined allowed values

## 💡 Notes

* You can use this tool for any database folder with the required structure — not tied to a specific schema.


# API Sanity Checker

## Overview

A tool to validate API implementations against `get_set_APIs.yaml`.
Checks classification, duplicates, file/YAML mismatches, parameter alignment, and generates JSON reports with a local dashboard.

## Features

* Reads **GET/SET** classification from `get_set_APIs.yaml`.
* Detects duplicate API names across interfaces.
* Flags missing/extra APIs between folders and YAML.
* Compares `invoke()` parameters with `get_info()` specs.
* Outputs `tools_info.json` & `sanity_report.json`.
* Serves a simple dashboard at `http://localhost:8000`.

## Notes

* Works for any `<database_name>` folder (e.g., `smart_home`, `finance_db`) with `interface_1`–`interface_5`.
* `get_set_APIs.yaml` can be generated from API docs using `helper_prompts/get_set_yaml_prompt.txt`.

## Usage

```bash
python sanity_checks.py <database_name>
```

Video Demo [link](https://drive.google.com/file/d/1o7eIhLcQYOdEArjkPROw2RUccUOqSHNq/view?usp=drive_link)

## Requirements

* Python 3.9+
* PyYAML


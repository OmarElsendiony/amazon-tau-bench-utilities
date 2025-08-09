
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



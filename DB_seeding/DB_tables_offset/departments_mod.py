import json
import os

# Read the original departments JSON file
with open('../Test/database_json/departments.json', 'r') as f:
    departments = json.load(f)

# Create new dictionary with offset department IDs
offset_departments = {}
for key, department in departments.items():
    # Convert current ID to int, add 25, then back to string
    old_id = int(key)
    new_id = old_id + 25
    new_key = str(new_id)
    
    # Create new department with updated department_id
    new_department = department.copy()
    new_department['department_id'] = str(new_id)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_department and new_department[field]:
            new_department[field] = new_department[field].rstrip('Z')
    
    # Add to new dictionary
    offset_departments[new_key] = new_department

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/departments.json', 'w') as f:
    json.dump(offset_departments, f, indent=2)

print(f"Departments with offset IDs saved to {new_dir}/departments.json")
print(f"Transformed {len(departments)} departments")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(departments.keys())[:3], list(offset_departments.keys())[:3])):
    old_department = departments[old_key]
    new_department = offset_departments[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    department_id: {old_department['department_id']} -> {new_department['department_id']}")
    print(f"    name: {new_department.get('name', 'N/A')}")
    print(f"    manager_id: {new_department.get('manager_id', 'N/A')}")
    print(f"    company_id: {new_department.get('company_id', 'N/A')}")
    print(f"    created_at: {old_department.get('created_at', 'N/A')} -> {new_department.get('created_at', 'N/A')}")
    if i < 2:
        print()

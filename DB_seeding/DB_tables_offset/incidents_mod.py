import json
import os

# Read the original incidents JSON file
with open('../Test/database_json/incidents.json', 'r') as f:
    incidents = json.load(f)

# Create new dictionary with offset IDs
offset_incidents = {}
for key, incident in incidents.items():
    # Convert current incident_id to int, add 200, then back to string
    old_id = int(key)
    new_id = old_id + 200
    new_key = str(new_id)
    
    # Create new incident with updated IDs
    new_incident = incident.copy()
    new_incident['incident_id'] = str(new_id)
    
    # Update category_id by adding 10
    if 'category_id' in new_incident and new_incident['category_id']:
        new_incident['category_id'] = str(int(new_incident['category_id']) + 10)
    
    # Update subcategory_id by adding 34
    if 'subcategory_id' in new_incident and new_incident['subcategory_id']:
        new_incident['subcategory_id'] = str(int(new_incident['subcategory_id']) + 34)
    
    # Update reported_by by adding 100
    if 'reported_by' in new_incident and new_incident['reported_by']:
        new_incident['reported_by'] = str(int(new_incident['reported_by']) + 100)
    
    # Update assigned_to by adding 100
    if 'assigned_to' in new_incident and new_incident['assigned_to']:
        new_incident['assigned_to'] = str(int(new_incident['assigned_to']) + 100)
    
    # Update department_id by adding 25
    if 'department_id' in new_incident and new_incident['department_id']:
        new_incident['department_id'] = str(int(new_incident['department_id']) + 25)
    
    # Update company_id by adding 15
    if 'company_id' in new_incident and new_incident['company_id']:
        new_incident['company_id'] = str(int(new_incident['company_id']) + 15)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_incident and new_incident[field]:
            new_incident[field] = new_incident[field].rstrip('Z')
    
    # Add to new dictionary
    offset_incidents[new_key] = new_incident

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/incidents.json', 'w') as f:
    json.dump(offset_incidents, f, indent=2)

print(f"Incidents with offset IDs saved to {new_dir}/incidents.json")
print(f"Transformed {len(incidents)} incidents")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(incidents.keys())[:3], list(offset_incidents.keys())[:3])):
    old_incident = incidents[old_key]
    new_incident = offset_incidents[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    incident_id: {old_incident['incident_id']} -> {new_incident['incident_id']}")
    print(f"    category_id: {old_incident.get('category_id', 'N/A')} -> {new_incident.get('category_id', 'N/A')}")
    print(f"    subcategory_id: {old_incident.get('subcategory_id', 'N/A')} -> {new_incident.get('subcategory_id', 'N/A')}")
    print(f"    reported_by: {old_incident.get('reported_by', 'N/A')} -> {new_incident.get('reported_by', 'N/A')}")
    print(f"    assigned_to: {old_incident.get('assigned_to', 'N/A')} -> {new_incident.get('assigned_to', 'N/A')}")
    print(f"    department_id: {old_incident.get('department_id', 'N/A')} -> {new_incident.get('department_id', 'N/A')}")
    print(f"    company_id: {old_incident.get('company_id', 'N/A')} -> {new_incident.get('company_id', 'N/A')}")
    print(f"    title: {new_incident.get('title', 'N/A')[:50]}...")
    if i < 2:
        print()

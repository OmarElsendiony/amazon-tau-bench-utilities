import json
import os

# Read the original incident_sla JSON file
with open('../Test/database_json/incident_sla.json', 'r') as f:
    incident_sla = json.load(f)

# Create new dictionary with offset IDs
offset_incident_sla = {}
for key, sla_entry in incident_sla.items():
    # Convert current incident_sla_id to int, add 200, then back to string
    old_id = int(key)
    new_id = old_id + 200
    new_key = str(new_id)
    
    # Create new sla_entry with updated IDs
    new_sla_entry = sla_entry.copy()
    new_sla_entry['incident_sla_id'] = str(new_id)
    
    # Update incident_id by adding 200
    if 'incident_id' in new_sla_entry and new_sla_entry['incident_id']:
        new_sla_entry['incident_id'] = str(int(new_sla_entry['incident_id']) + 200)
    
    # Update sla_id by adding 15
    if 'sla_id' in new_sla_entry and new_sla_entry['sla_id']:
        new_sla_entry['sla_id'] = str(int(new_sla_entry['sla_id']) + 15)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['response_due', 'resolve_due', 'created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_sla_entry and new_sla_entry[field]:
            new_sla_entry[field] = new_sla_entry[field].rstrip('Z')
    
    # Add to new dictionary
    offset_incident_sla[new_key] = new_sla_entry

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/incident_sla.json', 'w') as f:
    json.dump(offset_incident_sla, f, indent=2)

print(f"Incident SLA with offset IDs saved to {new_dir}/incident_sla.json")
print(f"Transformed {len(incident_sla)} incident SLA entries")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(incident_sla.keys())[:3], list(offset_incident_sla.keys())[:3])):
    old_sla = incident_sla[old_key]
    new_sla = offset_incident_sla[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    incident_sla_id: {old_sla['incident_sla_id']} -> {new_sla['incident_sla_id']}")
    print(f"    incident_id: {old_sla.get('incident_id', 'N/A')} -> {new_sla.get('incident_id', 'N/A')}")
    print(f"    sla_id: {old_sla.get('sla_id', 'N/A')} -> {new_sla.get('sla_id', 'N/A')}")
    print(f"    status: {new_sla.get('status', 'N/A')}")
    print(f"    created_at: {old_sla.get('created_at', 'N/A')} -> {new_sla.get('created_at', 'N/A')}")
    if i < 2:
        print()

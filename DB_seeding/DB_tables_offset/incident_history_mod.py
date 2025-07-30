import json
import os

# Read the original incident_history JSON file
with open('../Test/database_json/incident_history.json', 'r') as f:
    incident_history = json.load(f)

# Create new dictionary with offset IDs
offset_incident_history = {}
for key, history_entry in incident_history.items():
    # Convert current incident_history_id to int, add 315, then back to string
    old_id = int(key)
    new_id = old_id + 315
    new_key = str(new_id)
    
    # Create new history_entry with updated IDs
    new_history_entry = history_entry.copy()
    new_history_entry['incident_history_id'] = str(new_id)
    
    # Update incident_id by adding 200
    if 'incident_id' in new_history_entry and new_history_entry['incident_id']:
        new_history_entry['incident_id'] = str(int(new_history_entry['incident_id']) + 200)
    
    # Update changed_by by adding 100
    if 'changed_by' in new_history_entry and new_history_entry['changed_by']:
        new_history_entry['changed_by'] = str(int(new_history_entry['changed_by']) + 100)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['changed_at']
    for field in timestamp_fields:
        if field in new_history_entry and new_history_entry[field]:
            new_history_entry[field] = new_history_entry[field].rstrip('Z')
    
    # Add to new dictionary
    offset_incident_history[new_key] = new_history_entry

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/incident_history.json', 'w') as f:
    json.dump(offset_incident_history, f, indent=2)

print(f"Incident history with offset IDs saved to {new_dir}/incident_history.json")
print(f"Transformed {len(incident_history)} incident history entries")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(incident_history.keys())[:3], list(offset_incident_history.keys())[:3])):
    old_ih = incident_history[old_key]
    new_ih = offset_incident_history[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    incident_history_id: {old_ih['incident_history_id']} -> {new_ih['incident_history_id']}")
    print(f"    incident_id: {old_ih.get('incident_id', 'N/A')} -> {new_ih.get('incident_id', 'N/A')}")
    print(f"    changed_by: {old_ih.get('changed_by', 'N/A')} -> {new_ih.get('changed_by', 'N/A')}")
    print(f"    changed_at: {old_ih.get('changed_at', 'N/A')} -> {new_ih.get('changed_at', 'N/A')}")
    if 'incident_values' in new_ih and new_ih['incident_values']:
        print(f"    incident_values: {new_ih['incident_values']}")
    if i < 2:
        print()

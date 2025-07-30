import json
import os

# Read the original sla JSON file
with open('../Test/database_json/sla_policies.json', 'r') as f:
    sla = json.load(f)

# Create new dictionary with offset IDs
offset_sla = {}
for key, sla_entry in sla.items():
    # Convert current sla_id to int, add 15, then back to string
    old_id = int(key)
    new_id = old_id + 15
    new_key = str(new_id)
    
    # Create new sla_entry with updated IDs
    new_sla_entry = sla_entry.copy()
    new_sla_entry['sla_id'] = str(new_id)
    
    # Update category_id by adding 10
    if 'category_id' in new_sla_entry and new_sla_entry['category_id']:
        new_sla_entry['category_id'] = str(int(new_sla_entry['category_id']) + 10)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_sla_entry and new_sla_entry[field]:
            new_sla_entry[field] = new_sla_entry[field].rstrip('Z')
    
    # Add to new dictionary
    offset_sla[new_key] = new_sla_entry

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/sla.json', 'w') as f:
    json.dump(offset_sla, f, indent=2)

print(f"SLA with offset IDs saved to {new_dir}/sla_policies.json")
print(f"Transformed {len(sla)} SLA entries")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(sla.keys())[:3], list(offset_sla.keys())[:3])):
    old_sla = sla[old_key]
    new_sla = offset_sla[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    sla_id: {old_sla['sla_id']} -> {new_sla['sla_id']}")
    print(f"    category_id: {old_sla.get('category_id', 'N/A')} -> {new_sla.get('category_id', 'N/A')}")
    print(f"    name: {new_sla.get('name', 'N/A')}")
    print(f"    priority: {new_sla.get('priority', 'N/A')}")
    print(f"    response_time: {new_sla.get('response_time', 'N/A')}")
    print(f"    resolve_time: {new_sla.get('resolve_time', 'N/A')}")
    if i < 2:
        print()

import json
import os

# Read the original change_requests JSON file
with open('../Test/database_json/change_requests.json', 'r') as f:
    change_requests = json.load(f)

# Create new dictionary with offset IDs
offset_change_requests = {}
for key, change_request in change_requests.items():
    # Convert current change_request_id to int, add 40, then back to string
    old_id = int(key)
    new_id = old_id + 40
    new_key = str(new_id)
    
    # Create new change_request with updated IDs
    new_change_request = change_request.copy()
    new_change_request['change_request_id'] = str(new_id)
    
    # Update incident_id by adding 200
    if 'incident_id' in new_change_request and new_change_request['incident_id']:
        new_change_request['incident_id'] = str(int(new_change_request['incident_id']) + 200)
    
    # Update assigned_to by adding 100
    if 'assigned_to' in new_change_request and new_change_request['assigned_to']:
        new_change_request['assigned_to'] = str(int(new_change_request['assigned_to']) + 100)
    
    # Update approved_by by adding 100
    if 'approved_by' in new_change_request and new_change_request['approved_by']:
        new_change_request['approved_by'] = str(int(new_change_request['approved_by']) + 100)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at', 'scheduled_start', 'scheduled_end']
    for field in timestamp_fields:
        if field in new_change_request and new_change_request[field]:
            new_change_request[field] = new_change_request[field].rstrip('Z')
    
    # Add to new dictionary
    offset_change_requests[new_key] = new_change_request

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/change_requests.json', 'w') as f:
    json.dump(offset_change_requests, f, indent=2)

print(f"Change requests with offset IDs saved to {new_dir}/change_requests.json")
print(f"Transformed {len(change_requests)} change requests")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(change_requests.keys())[:3], list(offset_change_requests.keys())[:3])):
    old_cr = change_requests[old_key]
    new_cr = offset_change_requests[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    change_request_id: {old_cr['change_request_id']} -> {new_cr['change_request_id']}")
    print(f"    incident_id: {old_cr.get('incident_id', 'N/A')} -> {new_cr.get('incident_id', 'N/A')}")
    print(f"    assigned_to: {old_cr.get('assigned_to', 'N/A')} -> {new_cr.get('assigned_to', 'N/A')}")
    print(f"    approved_by: {old_cr.get('approved_by', 'N/A')} -> {new_cr.get('approved_by', 'N/A')}")
    print(f"    description: {new_cr.get('description', 'N/A')[:50]}...")
    if i < 2:
        print()

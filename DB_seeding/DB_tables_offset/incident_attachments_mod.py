import json
import os

# Read the original incident_attachments JSON file
with open('../Test/database_json/incident_attachments.json', 'r') as f:
    incident_attachments = json.load(f)

# Create new dictionary with offset IDs
offset_incident_attachments = {}
for key, incident_attachment in incident_attachments.items():
    # Convert current incident_attachment_id to int, add 201, then back to string
    old_id = int(key)
    new_id = old_id + 201
    new_key = str(new_id)
    
    # Create new incident_attachment with updated IDs
    new_incident_attachment = incident_attachment.copy()
    new_incident_attachment['incident_attachment_id'] = str(new_id)
    
    # Update incident_id by adding 200
    if 'incident_id' in new_incident_attachment and new_incident_attachment['incident_id']:
        new_incident_attachment['incident_id'] = str(int(new_incident_attachment['incident_id']) + 200)
    
    # Update uploaded_by by adding 100
    if 'uploaded_by' in new_incident_attachment and new_incident_attachment['uploaded_by']:
        new_incident_attachment['uploaded_by'] = str(int(new_incident_attachment['uploaded_by']) + 100)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_incident_attachment and new_incident_attachment[field]:
            new_incident_attachment[field] = new_incident_attachment[field].rstrip('Z')
    
    # Add to new dictionary
    offset_incident_attachments[new_key] = new_incident_attachment

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/incident_attachments.json', 'w') as f:
    json.dump(offset_incident_attachments, f, indent=2)

print(f"Incident attachments with offset IDs saved to {new_dir}/incident_attachments.json")
print(f"Transformed {len(incident_attachments)} incident attachments")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(incident_attachments.keys())[:3], list(offset_incident_attachments.keys())[:3])):
    old_ia = incident_attachments[old_key]
    new_ia = offset_incident_attachments[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    incident_attachment_id: {old_ia['incident_attachment_id']} -> {new_ia['incident_attachment_id']}")
    print(f"    incident_id: {old_ia.get('incident_id', 'N/A')} -> {new_ia.get('incident_id', 'N/A')}")
    print(f"    uploaded_by: {old_ia.get('uploaded_by', 'N/A')} -> {new_ia.get('uploaded_by', 'N/A')}")
    print(f"    comment_text: {new_ia.get('comment_text', 'N/A')[:50]}...")
    print(f"    created_at: {old_ia.get('created_at', 'N/A')} -> {new_ia.get('created_at', 'N/A')}")
    if i < 2:
        print()

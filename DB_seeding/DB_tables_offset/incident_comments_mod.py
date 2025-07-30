import json
import os

# Read the original incident_comments JSON file
with open('../Test/database_json/incident_comments.json', 'r') as f:
    incident_comments = json.load(f)

# Create new dictionary with offset IDs
offset_incident_comments = {}
for key, incident_comment in incident_comments.items():
    # Convert current incident_comment_id to int, add 786, then back to string
    old_id = int(key)
    new_id = old_id + 786
    new_key = str(new_id)
    
    # Create new incident_comment with updated IDs
    new_incident_comment = incident_comment.copy()
    new_incident_comment['incident_comment_id'] = str(new_id)
    
    # Update incident_id by adding 200
    if 'incident_id' in new_incident_comment and new_incident_comment['incident_id']:
        new_incident_comment['incident_id'] = str(int(new_incident_comment['incident_id']) + 200)
    
    # Update user_id by adding 100
    if 'user_id' in new_incident_comment and new_incident_comment['user_id']:
        new_incident_comment['user_id'] = str(int(new_incident_comment['user_id']) + 100)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_incident_comment and new_incident_comment[field]:
            new_incident_comment[field] = new_incident_comment[field].rstrip('Z')
    
    # Add to new dictionary
    offset_incident_comments[new_key] = new_incident_comment

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/incident_comments.json', 'w') as f:
    json.dump(offset_incident_comments, f, indent=2)

print(f"Incident comments with offset IDs saved to {new_dir}/incident_comments.json")
print(f"Transformed {len(incident_comments)} incident comments")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(incident_comments.keys())[:3], list(offset_incident_comments.keys())[:3])):
    old_ic = incident_comments[old_key]
    new_ic = offset_incident_comments[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    incident_comment_id: {old_ic['incident_comment_id']} -> {new_ic['incident_comment_id']}")
    print(f"    incident_id: {old_ic.get('incident_id', 'N/A')} -> {new_ic.get('incident_id', 'N/A')}")
    print(f"    user_id: {old_ic.get('user_id', 'N/A')} -> {new_ic.get('user_id', 'N/A')}")
    print(f"    comment_text: {new_ic.get('comment_text', 'N/A')[:50]}...")
    print(f"    created_at: {old_ic.get('created_at', 'N/A')} -> {new_ic.get('created_at', 'N/A')}")
    if i < 2:
        print()

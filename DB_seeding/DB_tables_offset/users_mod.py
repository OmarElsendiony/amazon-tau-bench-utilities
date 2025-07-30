import json
import os

# Read the original users JSON file
with open('../Test/database_json/users.json', 'r') as f:
    users = json.load(f)

# Create new dictionary with offset IDs
offset_users = {}
for key, user in users.items():
    # Convert current user_id to int, add 100, then back to string
    old_id = int(key)
    new_id = old_id + 100
    new_key = str(new_id)
    
    # Create new user with updated IDs
    new_user = user.copy()
    new_user['user_id'] = str(new_id)
    
    # Update company_id by adding 15
    if 'company_id' in new_user and new_user['company_id']:
        new_user['company_id'] = str(int(new_user['company_id']) + 15)
    
    # Update department_id by adding 25 if not null
    if 'department_id' in new_user and new_user['department_id'] is not None:
        new_user['department_id'] = str(int(new_user['department_id']) + 25)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_user and new_user[field]:
            new_user[field] = new_user[field].rstrip('Z')
    
    # Add to new dictionary
    offset_users[new_key] = new_user

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/users.json', 'w') as f:
    json.dump(offset_users, f, indent=2)

print(f"Users with offset IDs saved to {new_dir}/users.json")
print(f"Transformed {len(users)} users")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(users.keys())[:3], list(offset_users.keys())[:3])):
    old_user = users[old_key]
    new_user = offset_users[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    user_id: {old_user['user_id']} -> {new_user['user_id']}")
    print(f"    name: {new_user.get('first_name', '')} {new_user.get('last_name', '')}")
    print(f"    email: {new_user.get('email', 'N/A')}")
    print(f"    company_id: {old_user.get('company_id', 'N/A')} -> {new_user.get('company_id', 'N/A')}")
    print(f"    department_id: {old_user.get('department_id', 'N/A')} -> {new_user.get('department_id', 'N/A')}")
    print(f"    role: {new_user.get('role', 'N/A')}")
    if i < 2:
        print()

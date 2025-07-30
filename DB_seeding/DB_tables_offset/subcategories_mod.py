import json
import os

# Read the original subcategories JSON file
with open('../Test/database_json/subcategories.json', 'r') as f:
    subcategories = json.load(f)

# Create new dictionary with offset IDs
offset_subcategories = {}
for key, subcategory in subcategories.items():
    # Convert current subcategory_id to int, add 34, then back to string
    old_id = int(key)
    new_id = old_id + 34
    new_key = str(new_id)
    
    # Create new subcategory with updated IDs
    new_subcategory = subcategory.copy()
    new_subcategory['subcategory_id'] = str(new_id)
    
    # Update category_id by adding 10
    if 'category_id' in new_subcategory and new_subcategory['category_id']:
        new_subcategory['category_id'] = str(int(new_subcategory['category_id']) + 10)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_subcategory and new_subcategory[field]:
            new_subcategory[field] = new_subcategory[field].rstrip('Z')
    
    # Add to new dictionary
    offset_subcategories[new_key] = new_subcategory

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/subcategories.json', 'w') as f:
    json.dump(offset_subcategories, f, indent=2)

print(f"Subcategories with offset IDs saved to {new_dir}/subcategories.json")
print(f"Transformed {len(subcategories)} subcategories")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(subcategories.keys())[:3], list(offset_subcategories.keys())[:3])):
    old_subcategory = subcategories[old_key]
    new_subcategory = offset_subcategories[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    subcategory_id: {old_subcategory['subcategory_id']} -> {new_subcategory['subcategory_id']}")
    print(f"    category_id: {old_subcategory.get('category_id', 'N/A')} -> {new_subcategory.get('category_id', 'N/A')}")
    print(f"    name: {new_subcategory.get('name', 'N/A')}")
    print(f"    created_at: {old_subcategory.get('created_at', 'N/A')} -> {new_subcategory.get('created_at', 'N/A')}")
    if i < 2:
        print()

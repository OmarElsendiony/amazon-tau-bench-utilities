import json
import os

# Read the original categories JSON file
with open('../Test/database_json/categories.json', 'r') as f:
    categories = json.load(f)

# Create new dictionary with offset category IDs
offset_categories = {}
for key, category in categories.items():
    # Convert current ID to int, add 10, then back to string
    old_id = int(key)
    new_id = old_id + 10
    new_key = str(new_id)
    
    # Create new category with updated category_id
    new_category = category.copy()
    new_category['category_id'] = str(new_id)
    
    # Add to new dictionary
    offset_categories[new_key] = new_category

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/categories.json', 'w') as f:
    json.dump(offset_categories, f, indent=2)

print(f"Categories with offset IDs saved to {new_dir}/categories.json")
print(f"Transformed {len(categories)} categories")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(categories.keys())[:3], list(offset_categories.keys())[:3])):
    print(f"  {old_key} -> {new_key}")
    print(f"    category_id: {categories[old_key]['category_id']} -> {offset_categories[new_key]['category_id']}")
    print(f"    name: {offset_categories[new_key]['name']}")
    if i < 2:
        print()

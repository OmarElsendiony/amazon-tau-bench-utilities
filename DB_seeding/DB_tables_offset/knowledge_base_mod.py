import json
import os

# Read the original knowledge_base JSON file
with open('../Test/database_json/knowledge_base.json', 'r') as f:
    knowledge_base = json.load(f)

# Create new dictionary with offset IDs
offset_knowledge_base = {}
for key, kb_entry in knowledge_base.items():
    # Convert current knowledge_base_id to int, add 50, then back to string
    old_id = int(key)
    new_id = old_id + 50
    new_key = str(new_id)
    
    # Create new kb_entry with updated IDs
    new_kb_entry = kb_entry.copy()
    new_kb_entry['knowledge_base_id'] = str(new_id)
    
    # Update created_by by adding 100
    if 'created_by' in new_kb_entry and new_kb_entry['created_by']:
        new_kb_entry['created_by'] = str(int(new_kb_entry['created_by']) + 100)
    
    # Update category_id by adding 10
    if 'category_id' in new_kb_entry and new_kb_entry['category_id']:
        new_kb_entry['category_id'] = str(int(new_kb_entry['category_id']) + 10)
    
    # Update subcategory_id by adding 34
    if 'subcategory_id' in new_kb_entry and new_kb_entry['subcategory_id']:
        new_kb_entry['subcategory_id'] = str(int(new_kb_entry['subcategory_id']) + 34)
    
    # Update company_id by adding 15
    if 'company_id' in new_kb_entry and new_kb_entry['company_id']:
        new_kb_entry['company_id'] = str(int(new_kb_entry['company_id']) + 15)
    
    # Update department_id by adding 25 if not null
    if 'department_id' in new_kb_entry and new_kb_entry['department_id'] is not None:
        new_kb_entry['department_id'] = str(int(new_kb_entry['department_id']) + 25)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_kb_entry and new_kb_entry[field]:
            new_kb_entry[field] = new_kb_entry[field].rstrip('Z')
    
    # Add to new dictionary
    offset_knowledge_base[new_key] = new_kb_entry

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/knowledge_base.json', 'w') as f:
    json.dump(offset_knowledge_base, f, indent=2)

print(f"Knowledge base with offset IDs saved to {new_dir}/knowledge_base.json")
print(f"Transformed {len(knowledge_base)} knowledge base entries")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(knowledge_base.keys())[:3], list(offset_knowledge_base.keys())[:3])):
    old_kb = knowledge_base[old_key]
    new_kb = offset_knowledge_base[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    knowledge_base_id: {old_kb['knowledge_base_id']} -> {new_kb['knowledge_base_id']}")
    print(f"    created_by: {old_kb.get('created_by', 'N/A')} -> {new_kb.get('created_by', 'N/A')}")
    print(f"    category_id: {old_kb.get('category_id', 'N/A')} -> {new_kb.get('category_id', 'N/A')}")
    print(f"    subcategory_id: {old_kb.get('subcategory_id', 'N/A')} -> {new_kb.get('subcategory_id', 'N/A')}")
    print(f"    company_id: {old_kb.get('company_id', 'N/A')} -> {new_kb.get('company_id', 'N/A')}")
    print(f"    department_id: {old_kb.get('department_id', 'N/A')} -> {new_kb.get('department_id', 'N/A')}")
    print(f"    description: {new_kb.get('description', 'N/A')[:50]}...")
    if i < 2:
        print()

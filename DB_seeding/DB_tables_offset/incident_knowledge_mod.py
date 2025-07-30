import json
import os

# Read the original incident_knowledge JSON file
with open('../Test/database_json/incident_knowledge.json', 'r') as f:
    incident_knowledge = json.load(f)

# Create new dictionary with added incident_knowledge_id field
updated_incident_knowledge = {}
for key, knowledge_entry in incident_knowledge.items():
    # Create new knowledge_entry with added incident_knowledge_id field
    new_knowledge_entry = knowledge_entry.copy()
    new_knowledge_entry['incident_knowledge_id'] = key
    
    # Add to new dictionary
    updated_incident_knowledge[key] = new_knowledge_entry

# Create backup directory if it doesn't exist
backup_dir = '../Test/database_json_backup'
os.makedirs(backup_dir, exist_ok=True)

# Backup the original file
with open(f'{backup_dir}/incident_knowledge_original.json', 'w') as f:
    json.dump(incident_knowledge, f, indent=2)

# Save the updated data back to the original file
with open('../Test/database_json/incident_knowledge.json', 'w') as f:
    json.dump(updated_incident_knowledge, f, indent=2)

print(f"Added incident_knowledge_id field to {len(incident_knowledge)} entries")
print(f"Original file backed up to {backup_dir}/incident_knowledge_original.json")
print(f"Updated file saved to ../Test/database_json/incident_knowledge.json")

# Display a sample of the transformation
print("\nSample transformation:")
for i, key in enumerate(list(updated_incident_knowledge.keys())[:3]):
    old_entry = incident_knowledge[key]
    new_entry = updated_incident_knowledge[key]
    
    print(f"  Entry {key}:")
    print(f"    Before: {old_entry}")
    print(f"    After:  {new_entry}")
    if i < 2:
        print()

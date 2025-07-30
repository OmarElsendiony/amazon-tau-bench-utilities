import json
import os

# Read the original tasks JSON file
with open('../Test/database_json/tasks.json', 'r') as f:
    tasks = json.load(f)

# Create new dictionary with offset IDs
offset_tasks = {}
for key, task in tasks.items():
    # Convert current task_id to int, add 142, then back to string
    old_id = int(key)
    new_id = old_id + 142
    new_key = str(new_id)
    
    # Create new task with updated IDs
    new_task = task.copy()
    new_task['task_id'] = str(new_id)
    
    # Update incident_id by adding 200
    if 'incident_id' in new_task and new_task['incident_id']:
        new_task['incident_id'] = str(int(new_task['incident_id']) + 200)
    
    # Update assigned_to by adding 100
    if 'assigned_to' in new_task and new_task['assigned_to']:
        new_task['assigned_to'] = str(int(new_task['assigned_to']) + 100)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['due_date', 'created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_task and new_task[field]:
            new_task[field] = new_task[field].rstrip('Z')
    
    # Add to new dictionary
    offset_tasks[new_key] = new_task

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/tasks.json', 'w') as f:
    json.dump(offset_tasks, f, indent=2)

print(f"Tasks with offset IDs saved to {new_dir}/tasks.json")
print(f"Transformed {len(tasks)} tasks")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(tasks.keys())[:3], list(offset_tasks.keys())[:3])):
    old_task = tasks[old_key]
    new_task = offset_tasks[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    task_id: {old_task['task_id']} -> {new_task['task_id']}")
    print(f"    incident_id: {old_task.get('incident_id', 'N/A')} -> {new_task.get('incident_id', 'N/A')}")
    print(f"    assigned_to: {old_task.get('assigned_to', 'N/A')} -> {new_task.get('assigned_to', 'N/A')}")
    print(f"    status: {new_task.get('status', 'N/A')}")
    print(f"    priority: {new_task.get('priority', 'N/A')}")
    print(f"    description: {new_task.get('description', 'N/A')[:50]}...")
    if i < 2:
        print()

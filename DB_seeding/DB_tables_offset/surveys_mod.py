import json
import os

# Read the original surveys JSON file
with open('../Test/database_json/surveys.json', 'r') as f:
    surveys = json.load(f)

# Create new dictionary with offset IDs
offset_surveys = {}
for key, survey in surveys.items():
    # Convert current survey_id to int, add 90, then back to string
    old_id = int(key)
    new_id = old_id + 90
    new_key = str(new_id)
    
    # Create new survey with updated IDs
    new_survey = survey.copy()
    new_survey['survey_id'] = str(new_id)
    
    # Update incident_id by adding 200
    if 'incident_id' in new_survey and new_survey['incident_id']:
        new_survey['incident_id'] = str(int(new_survey['incident_id']) + 200)
    
    # Update user_id by adding 100
    if 'user_id' in new_survey and new_survey['user_id']:
        new_survey['user_id'] = str(int(new_survey['user_id']) + 100)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['submitted_at', 'created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_survey and new_survey[field]:
            new_survey[field] = new_survey[field].rstrip('Z')
    
    # Add to new dictionary
    offset_surveys[new_key] = new_survey

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/surveys.json', 'w') as f:
    json.dump(offset_surveys, f, indent=2)

print(f"Surveys with offset IDs saved to {new_dir}/surveys.json")
print(f"Transformed {len(surveys)} surveys")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(surveys.keys())[:3], list(offset_surveys.keys())[:3])):
    old_survey = surveys[old_key]
    new_survey = offset_surveys[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    survey_id: {old_survey['survey_id']} -> {new_survey['survey_id']}")
    print(f"    incident_id: {old_survey.get('incident_id', 'N/A')} -> {new_survey.get('incident_id', 'N/A')}")
    print(f"    user_id: {old_survey.get('user_id', 'N/A')} -> {new_survey.get('user_id', 'N/A')}")
    print(f"    rating: {new_survey.get('rating', 'N/A')}")
    print(f"    submitted_at: {old_survey.get('submitted_at', 'N/A')} -> {new_survey.get('submitted_at', 'N/A')}")
    if i < 2:
        print()

import json
import os

# Read the original companies JSON file
with open('../Test/database_json/companies.json', 'r') as f:
    companies = json.load(f)

# Create new dictionary with offset company IDs
offset_companies = {}
for key, company in companies.items():
    # Convert current ID to int, add 15, then back to string
    old_id = int(key)
    new_id = old_id + 15
    new_key = str(new_id)
    
    # Create new company with updated company_id
    new_company = company.copy()
    new_company['company_id'] = str(new_id)
    
    # Remove 'Z' from timestamp fields if present
    timestamp_fields = ['created_at', 'updated_at']
    for field in timestamp_fields:
        if field in new_company and new_company[field]:
            new_company[field] = new_company[field].rstrip('Z')
    
    # Add to new dictionary
    offset_companies[new_key] = new_company

# Create new directory if it doesn't exist
new_dir = '../Test/database_json_offset'
os.makedirs(new_dir, exist_ok=True)

# Save the transformed data to new file
with open(f'{new_dir}/companies.json', 'w') as f:
    json.dump(offset_companies, f, indent=2)

print(f"Companies with offset IDs saved to {new_dir}/companies.json")
print(f"Transformed {len(companies)} companies")

# Display a sample of the transformation
print("\nSample transformation:")
for i, (old_key, new_key) in enumerate(zip(list(companies.keys())[:3], list(offset_companies.keys())[:3])):
    old_company = companies[old_key]
    new_company = offset_companies[new_key]
    
    print(f"  {old_key} -> {new_key}")
    print(f"    company_id: {old_company['company_id']} -> {new_company['company_id']}")
    print(f"    name: {new_company.get('name', 'N/A')}")
    print(f"    industry: {new_company.get('industry', 'N/A')}")
    print(f"    created_at: {old_company.get('created_at', 'N/A')} -> {new_company.get('created_at', 'N/A')}")
    if i < 2:
        print()

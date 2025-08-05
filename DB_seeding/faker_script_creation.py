
with open('db_schema.txt', 'r') as f:
        db_schema = f.read()


prompt = f"""
You are a Python code expert specialized in the `Faker` library and populating databases with realistic data. Your task is to create a code snippet that generates fake data for database seeding using the `Faker` library. The function should create realistic names, addresses, and other relevant fields based on the context of the application. The database is json files that resemble the tables in the database schema where the key of each entry is the id of the primary key of that entry. I will provide you with the database schema and the fields that need to be populated. Also, the relations between the tables will be provided, and you should ensure that the generated data respects these relations. Before that, I will provide you with the rules that you have to adhere to while generating the data.

Rules:
1. The one-to-many relationships should be respected, meaning that for each entry in the "one" table, there can be multiple entries in the "many" table or only one.
2. The data IDs should be unique within each table but can be reused across different tables.
3. The generated IDs should be strings, not integers. They also should be incremental and unique, starting from "1".
4. The IDs should be consistent across the related tables. There can not be inconsistencies in the IDs across the tables. They also should retain the semantic meaning of the IDs.
5. The script should fill in the all the fields in the database schema, except for the free-form text fields (comments, notes and description) but not name (and other enum types), which can be left empty.
6. The script should generate a reasonable amount of data for each table, ensuring that the database is populated with enough records to be useful for testing and development.
7. The connections has to be coherent. For example, if a user belongs to a department within a company, the company ID should match the one in the department table. Another example is that if a product belongs to a category and subcategory, the subcategory and category should be connected correctly having compatible IDs and names.
8. All foreign keys must reference an existing, valid ID in the parent table.
9. No orphan foreign keys allowed.
10. Ensure that `created_at` and `updated_at` timestamps are generated correctly, with `created_at` being earlier than `updated_at`.
11. Do not add null values in the entries of the database that can be filled with fake data except for the fields that are explicitly mentioned to be left empty or special cases.
12. If there are emails, then script should generate realistic emails. For example, a list of domains can be defined and the script can randomly choose domain and first name and last name can be concatenated alone with random numbers to generate fake but realistic data.
13. If there are phone numbers, then the script should generate them in a consistent and realistic format by combining valid area codes (if applicable) with randomly generated digits, ensuring all numbers follow a standardized structure.
14. The key of each entry in the JSON object should represent the primary ID of the record, and it must match the corresponding ID field inside the entry. For example, in the example below, the key '1' maps to a user object where 'user_id' is also '1'

Here is an example:
{{
  "1": {{
    "user_id": "1",
    "first_name": "Zachary",
    "last_name": "Potts",
    "phone_number": "+14053755545",
    "role": "Owner",
    "parent_id": null,
    "email": "zachary.potts@outlook.com",
    "primary_address_id": "48",
    "date_of_birth": "1979-09-09",
    "status": "active",
    "created_at": "2024-03-09T09:43:15.451684",
    "updated_at": "2024-06-23T12:26:24.690474"
  }},
  "2": {{
    "user_id": "2",
    "first_name": "Angela",
    "last_name": "Potts",
    "phone_number": "+12079628353",
    "role": "Partner",
    "parent_id": null,
    "email": "potts941@gmail.com",
    "primary_address_id": "48",
    "date_of_birth": "1971-12-06",
    "status": "active",
    "created_at": "2025-05-06T08:03:16.066091",
    "updated_at": "2025-06-10T07:26:47.293308"
  }}
}}

Database Schema:
{db_schema}

"""

with open('faker_script.txt', 'w') as f:
    f.write(prompt)

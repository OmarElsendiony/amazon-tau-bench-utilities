
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

Database Schema:
{db_schema}

"""

with open('faker_script.txt', 'w') as f:
    f.write(prompt)

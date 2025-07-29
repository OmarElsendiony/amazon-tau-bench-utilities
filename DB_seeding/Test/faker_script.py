import json
import os
from faker import Faker
from datetime import datetime, timedelta
import random
import hashlib

# Initialize Faker
fake = Faker()

# Ensure consistent data generation
Faker.seed(42)
random.seed(42)

# Create output directory
os.makedirs('database_json', exist_ok=True)

# Helper function to generate incremental string IDs
class IDGenerator:
    def __init__(self):
        self.counters = {}
    
    def get_next_id(self, table_name):
        if table_name not in self.counters:
            self.counters[table_name] = 1
        else:
            self.counters[table_name] += 1
        return str(self.counters[table_name])

id_gen = IDGenerator()

# Helper function to generate timestamps
def generate_timestamps():
    created = fake.date_time_between(start_date='-2y', end_date='-1d')
    updated = fake.date_time_between(start_date=created, end_date='now')
    return created.isoformat(), updated.isoformat()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Data storage
data = {}

# 1. Generate Companies
print("Generating companies...")
companies = {}
industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Government', 'Telecommunications']

for i in range(10):  # 10 companies
    company_id = id_gen.get_next_id('companies')
    created_at, updated_at = generate_timestamps()
    
    companies[company_id] = {
        'company_id': company_id,
        'name': fake.company(),
        'industry': random.choice(industries),
        'address': fake.address().replace('\n', ', '),
        'created_at': created_at,
        'updated_at': updated_at
    }

data['companies'] = companies

# 2. Generate Categories
print("Generating categories...")
categories = {}
category_names = ['Hardware', 'Software', 'Network', 'Security', 'Access', 'Performance', 'Database', 'Email', 'Printing', 'Mobile']

for i, cat_name in enumerate(category_names):
    category_id = id_gen.get_next_id('categories')
    created_at, updated_at = generate_timestamps()
    
    categories[category_id] = {
        'category_id': category_id,
        'name': cat_name,
        'created_at': created_at,
        'updated_at': updated_at
    }

data['categories'] = categories

# 3. Generate Subcategories
print("Generating subcategories...")
subcategories = {}
subcategory_mapping = {
    'Hardware': ['Desktop Issues', 'Laptop Problems', 'Server Hardware', 'Peripherals'],
    'Software': ['Application Errors', 'License Issues', 'Installation Problems', 'Updates'],
    'Network': ['Connectivity Issues', 'VPN Problems', 'WiFi Issues', 'Bandwidth'],
    'Security': ['Password Reset', 'Account Lockout', 'Malware', 'Phishing'],
    'Access': ['Permission Issues', 'Account Creation', 'Role Assignment', 'System Access'],
    'Performance': ['Slow Response', 'System Crashes', 'Memory Issues', 'CPU Usage'],
    'Database': ['Connection Issues', 'Query Problems', 'Backup Issues', 'Data Corruption'],
    'Email': ['Delivery Issues', 'Spam Problems', 'Configuration', 'Storage Limits'],
    'Printing': ['Print Queue', 'Driver Issues', 'Paper Jams', 'Quality Issues'],
    'Mobile': ['App Issues', 'Device Setup', 'Synchronization', 'Mobile Security']
}

for category_id, category_data in categories.items():
    category_name = category_data['name']
    if category_name in subcategory_mapping:
        for subcat_name in subcategory_mapping[category_name]:
            subcategory_id = id_gen.get_next_id('subcategories')
            created_at, updated_at = generate_timestamps()
            
            subcategories[subcategory_id] = {
                'subcategory_id': subcategory_id,
                'category_id': category_id,
                'name': subcat_name,
                'created_at': created_at,
                'updated_at': updated_at
            }

data['subcategories'] = subcategories

# 4. Generate Departments
print("Generating departments...")
departments = {}
dept_names = ['IT Support', 'Human Resources', 'Finance', 'Marketing', 'Sales', 'Operations', 'Security', 'Development']

for company_id in companies.keys():
    # Each company gets 3-5 departments
    num_depts = random.randint(3, 5)
    selected_depts = random.sample(dept_names, num_depts)
    
    for dept_name in selected_depts:
        department_id = id_gen.get_next_id('departments')
        created_at, updated_at = generate_timestamps()
        
        departments[department_id] = {
            'department_id': department_id,
            'name': dept_name,
            'manager_id': None,  # Will be filled after users are created
            'company_id': company_id,
            'created_at': created_at,
            'updated_at': updated_at
        }

data['departments'] = departments

# 5. Generate Users
print("Generating users...")
users = {}
roles = ['end_user', 'agent', 'manager', 'admin']
statuses = ['active', 'inactive']
timezones = ['UTC', 'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'Europe/London', 'Europe/Berlin', 'Asia/Tokyo']

# Create users for each company
for company_id in companies.keys():
    company_departments = [d for d in departments.values() if d['company_id'] == company_id]
    
    # Generate 15-25 users per company
    num_users = random.randint(15, 25)
    
    for i in range(num_users):
        user_id = id_gen.get_next_id('users')
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{companies[company_id]['name'].lower().replace(' ', '').replace(',', '')}.com"
        role = random.choice(roles)
        created_at, updated_at = generate_timestamps()
        
        # Assign department only for agents, managers, and some admins
        department_id = None
        if role in ['agent', 'manager'] or (role == 'admin' and random.random() < 0.7):
            if company_departments:
                department_id = random.choice(company_departments)['department_id']
        
        users[user_id] = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'role': role,
            'status': random.choice(statuses),
            'timezone': random.choice(timezones),
            'company_id': company_id,
            'department_id': department_id,
            'password_hash': hash_password('defaultpassword123'),
            'created_at': created_at,
            'updated_at': updated_at
        }

data['users'] = users

# Assign managers to departments
print("Assigning managers to departments...")
for dept_id, dept_data in departments.items():
    # Find managers or admins in this company and department
    potential_managers = [u for u in users.values() 
                         if u['company_id'] == dept_data['company_id'] 
                         and u['role'] in ['manager', 'admin']
                         and u['department_id'] == dept_id]
    
    if potential_managers:
        manager = random.choice(potential_managers)
        departments[dept_id]['manager_id'] = manager['user_id']

# 6. Generate SLA Policies
print("Generating SLA policies...")
sla_policies = {}
priorities = ['low', 'medium', 'high', 'critical']

for category_id in categories.keys():
    for priority in priorities:
        sla_id = id_gen.get_next_id('sla_policies')
        created_at, updated_at = generate_timestamps()
        
        # Response and resolve times based on priority
        time_mapping = {
            'low': (480, 2880),      # 8 hours response, 2 days resolve
            'medium': (240, 1440),   # 4 hours response, 1 day resolve
            'high': (60, 480),       # 1 hour response, 8 hours resolve
            'critical': (15, 240)    # 15 minutes response, 4 hours resolve
        }
        
        response_time, resolve_time = time_mapping[priority]
        
        sla_policies[sla_id] = {
            'sla_id': sla_id,
            'name': f"{categories[category_id]['name']} - {priority.capitalize()} Priority",
            'priority': priority,
            'category_id': category_id,
            'response_time': response_time,
            'resolve_time': resolve_time,
            'created_at': created_at,
            'updated_at': updated_at
        }

data['sla_policies'] = sla_policies

# 7. Generate Incidents
print("Generating incidents...")
incidents = {}
incident_statuses = ['open', 'in_progress', 'resolved', 'closed']
incident_priorities = ['low', 'medium', 'high', 'critical']

for company_id in companies.keys():
    company_users = [u for u in users.values() if u['company_id'] == company_id]
    company_departments = [d for d in departments.values() if d['company_id'] == company_id]
    
    # Generate 20-40 incidents per company
    num_incidents = random.randint(20, 40)
    
    for i in range(num_incidents):
        incident_id = id_gen.get_next_id('incidents')
        
        # Select category and subcategory
        category_id = random.choice(list(categories.keys()))
        available_subcategories = [s for s in subcategories.values() if s['category_id'] == category_id]
        subcategory_id = random.choice(available_subcategories)['subcategory_id'] if available_subcategories else None
        
        # Select reporter (any user from company)
        reported_by = random.choice(company_users)['user_id']
        
        # Select assigned agent (agents/managers/admins only)
        agents = [u for u in company_users if u['role'] in ['agent', 'manager', 'admin']]
        assigned_to = random.choice(agents)['user_id'] if agents and random.random() < 0.8 else None
        
        # Select department
        department_id = random.choice(company_departments)['department_id'] if company_departments else None
        
        created_at, updated_at = generate_timestamps()
        
        incidents[incident_id] = {
            'incident_id': incident_id,
            'title': fake.sentence(nb_words=6),
            'description': '',  # Leave empty as per rules
            'category_id': category_id,
            'subcategory_id': subcategory_id,
            'reported_by': reported_by,
            'assigned_to': assigned_to,
            'department_id': department_id,
            'company_id': company_id,
            'status': random.choice(incident_statuses),
            'priority': random.choice(incident_priorities),
            'created_at': created_at,
            'updated_at': updated_at
        }

data['incidents'] = incidents

# 8. Generate Incident SLA
print("Generating incident SLA...")
incident_sla = {}
sla_statuses = ['Pending', 'Completed', 'Cancelled']

for incident_id, incident_data in incidents.items():
    # Find matching SLA policy
    matching_slas = [s for s in sla_policies.values() 
                    if s['category_id'] == incident_data['category_id'] 
                    and s['priority'] == incident_data['priority']]
    
    if matching_slas:
        sla_policy = random.choice(matching_slas)
        incident_sla_id = id_gen.get_next_id('incident_sla')
        
        # Calculate due dates
        incident_created = datetime.fromisoformat(incident_data['created_at'])
        response_due = incident_created + timedelta(minutes=sla_policy['response_time'])
        resolve_due = incident_created + timedelta(minutes=sla_policy['resolve_time'])
        
        created_at, updated_at = generate_timestamps()
        
        incident_sla[incident_sla_id] = {
            'incident_sla_id': incident_sla_id,
            'incident_id': incident_id,
            'sla_id': sla_policy['sla_id'],
            'response_due': response_due.isoformat(),
            'resolve_due': resolve_due.isoformat(),
            'breached': random.choice([True, False]),
            'status': random.choice(sla_statuses),
            'created_at': created_at,
            'updated_at': updated_at
        }

data['incident_sla'] = incident_sla

# 9. Generate Tasks
print("Generating tasks...")
tasks = {}
task_statuses = ['todo', 'in_progress', 'blocked', 'done', 'cancelled']
task_priorities = ['low', 'medium', 'high', 'critical']

# Generate 1-3 tasks per incident
for incident_id, incident_data in incidents.items():
    num_tasks = random.randint(0, 3)
    
    for i in range(num_tasks):
        task_id = id_gen.get_next_id('tasks')
        
        # Assign to agents/managers/admins from same company
        company_agents = [u for u in users.values() 
                         if u['company_id'] == incident_data['company_id'] 
                         and u['role'] in ['agent', 'manager', 'admin']]
        
        assigned_to = random.choice(company_agents)['user_id'] if company_agents else None
        
        created_at, updated_at = generate_timestamps()
        due_date = datetime.fromisoformat(created_at) + timedelta(days=random.randint(1, 14))
        
        tasks[task_id] = {
            'task_id': task_id,
            'incident_id': incident_id,
            'description': '',  # Leave empty as per rules
            'assigned_to': assigned_to,
            'status': random.choice(task_statuses),
            'priority': random.choice(task_priorities),
            'due_date': due_date.isoformat(),
            'created_at': created_at,
            'updated_at': updated_at
        }

data['tasks'] = tasks

# 10. Generate Change Requests
print("Generating change requests...")
change_requests = {}
cr_statuses = ['draft', 'submitted', 'approved', 'rejected', 'in_progress', 'implemented', 'closed']
cr_priorities = ['low', 'medium', 'high', 'critical']
risk_levels = ['low', 'medium', 'high']

# Generate change requests (some linked to incidents)
for i in range(30):
    cr_id = id_gen.get_next_id('change_requests')
    
    # 70% chance to link to an incident
    incident_id = random.choice(list(incidents.keys())) if random.random() < 0.7 else None
    
    # Select a random company for assignment
    company_id = random.choice(list(companies.keys()))
    company_agents = [u for u in users.values() 
                     if u['company_id'] == company_id 
                     and u['role'] in ['agent', 'manager', 'admin']]
    
    assigned_to = random.choice(company_agents)['user_id']
    
    # Approver (managers/admins only)
    approvers = [u for u in users.values() 
                if u['company_id'] == company_id 
                and u['role'] in ['manager', 'admin']]
    approved_by = random.choice(approvers)['user_id'] if approvers and random.random() < 0.6 else None
    
    created_at, updated_at = generate_timestamps()
    scheduled_start = datetime.fromisoformat(created_at) + timedelta(days=random.randint(1, 30))
    scheduled_end = scheduled_start + timedelta(hours=random.randint(2, 48))
    
    change_requests[cr_id] = {
        'change_request_id': cr_id,
        'incident_id': incident_id,
        'assigned_to': assigned_to,
        'approved_by': approved_by,
        'description': fake.sentence(nb_words=10),
        'status': random.choice(cr_statuses),
        'priority': random.choice(cr_priorities),
        'risk_level': random.choice(risk_levels),
        'affected_scope': {"systems": random.sample(["database", "web_server", "email", "network", "storage"], random.randint(1, 3))},
        'scheduled_start': scheduled_start.isoformat(),
        'scheduled_end': scheduled_end.isoformat(),
        'created_at': created_at,
        'updated_at': updated_at
    }

data['change_requests'] = change_requests

# 11. Generate Knowledge Base
print("Generating knowledge base...")
knowledge_base = {}

for i in range(50):
    kb_id = id_gen.get_next_id('knowledge_base')
    
    # Select random category and subcategory
    category_id = random.choice(list(categories.keys()))
    available_subcategories = [s for s in subcategories.values() if s['category_id'] == category_id]
    subcategory_id = random.choice(available_subcategories)['subcategory_id'] if available_subcategories else None
    
    # Select random company and department
    company_id = random.choice(list(companies.keys()))
    company_departments = [d for d in departments.values() if d['company_id'] == company_id]
    department_id = random.choice(company_departments)['department_id'] if company_departments else None
    
    # Select creator from company agents/managers/admins
    creators = [u for u in users.values() 
               if u['company_id'] == company_id 
               and u['role'] in ['agent', 'manager', 'admin']]
    created_by = random.choice(creators)['user_id'] if creators else list(users.keys())[0]
    
    created_at, updated_at = generate_timestamps()
    
    knowledge_base[kb_id] = {
        'knowledge_base_id': kb_id,
        'description': fake.sentence(nb_words=8),
        'created_by': created_by,
        'category_id': category_id,
        'subcategory_id': subcategory_id,
        'company_id': company_id,
        'department_id': department_id,
        'created_at': created_at,
        'updated_at': updated_at
    }

data['knowledge_base'] = knowledge_base

# 12. Generate Incident Knowledge relationships
print("Generating incident knowledge relationships...")
incident_knowledge = {}

# Link some incidents to knowledge base articles
for i, incident_id in enumerate(random.sample(list(incidents.keys()), min(30, len(incidents)))):
    incident_data = incidents[incident_id]
    
    # Find relevant knowledge base articles (same category/company)
    relevant_kb = [kb for kb in knowledge_base.values() 
                  if kb['category_id'] == incident_data['category_id'] 
                  and kb['company_id'] == incident_data['company_id']]
    
    if relevant_kb:
        kb_article = random.choice(relevant_kb)
        # Convert the ISO string to datetime object first
        incident_created = datetime.fromisoformat(incident_data['created_at'])
        created_at = fake.date_time_between(start_date=incident_created).isoformat()
        
        # Using incident_id as key since it's a junction table
        incident_knowledge[f"{incident_id}_{kb_article['knowledge_base_id']}"] = {
            'incident_id': incident_id,
            'knowledge_base_id': kb_article['knowledge_base_id'],
            'created_at': created_at
        }

data['incident_knowledge'] = incident_knowledge

# 13. Generate Incident Comments
print("Generating incident comments...")
incident_comments = {}

# Generate 1-5 comments per incident
for incident_id, incident_data in incidents.items():
    num_comments = random.randint(0, 5)
    
    for i in range(num_comments):
        comment_id = id_gen.get_next_id('incident_comments')
        
        # Commenter from same company
        company_users = [u for u in users.values() if u['company_id'] == incident_data['company_id']]
        user_id = random.choice(company_users)['user_id']
        
        created_at, updated_at = generate_timestamps()
        
        incident_comments[comment_id] = {
            'incident_comment_id': comment_id,
            'incident_id': incident_id,
            'user_id': user_id,
            'comment_text': '',  # Leave empty as per rules
            'is_public': random.choice([True, False]),
            'created_at': created_at,
            'updated_at': updated_at
        }

data['incident_comments'] = incident_comments

# 14. Generate Incident Attachments
print("Generating incident attachments...")
incident_attachments = {}

# Generate 0-3 attachments per incident
for incident_id, incident_data in incidents.items():
    num_attachments = random.randint(0, 3)
    
    for i in range(num_attachments):
        attachment_id = id_gen.get_next_id('incident_attachments')
        
        # Uploader from same company
        company_users = [u for u in users.values() if u['company_id'] == incident_data['company_id']]
        uploaded_by = random.choice(company_users)['user_id']
        
        file_extensions = ['.jpg', '.png', '.pdf', '.docx', '.xlsx', '.txt', '.log']
        file_name = f"{fake.word()}{random.choice(file_extensions)}"
        file_url = f"https://storage.example.com/attachments/{attachment_id}/{file_name}"
        
        # Convert the ISO string to datetime object first
        incident_created = datetime.fromisoformat(incident_data['created_at'])
        uploaded_at = fake.date_time_between(start_date=incident_created).isoformat()
        created_at, updated_at = generate_timestamps()
        
        incident_attachments[attachment_id] = {
            'incident_attachment_id': attachment_id,
            'incident_id': incident_id,
            'uploaded_by': uploaded_by,
            'file_name': file_name,
            'file_url': file_url,
            'uploaded_at': uploaded_at,
            'created_at': created_at,
            'updated_at': updated_at
        }

data['incident_attachments'] = incident_attachments

# 15. Generate Incident History
print("Generating incident history...")
incident_history = {}

# Generate 1-5 history entries per incident
for incident_id, incident_data in incidents.items():
    num_history = random.randint(1, 5)
    
    for i in range(num_history):
        history_id = id_gen.get_next_id('incident_history')
        
        # Changed by agents/managers/admins from same company
        company_agents = [u for u in users.values() 
                         if u['company_id'] == incident_data['company_id'] 
                         and u['role'] in ['agent', 'manager', 'admin']]
        changed_by = random.choice(company_agents)['user_id'] if company_agents else list(users.keys())[0]
        
        # Convert the ISO string to datetime object first
        incident_created = datetime.fromisoformat(incident_data['created_at'])
        changed_at = fake.date_time_between(start_date=incident_created).isoformat()
        
        incident_history[history_id] = {
            'incident_history_id': history_id,
            'incident_id': incident_id,
            'changed_by': changed_by,
            'incident_values': {
                'status': random.choice(incident_statuses),
                'priority': random.choice(incident_priorities)
            },
            'task_values': {
                'status': random.choice(task_statuses) if random.random() < 0.5 else None
            },
            'changed_at': changed_at
        }

data['incident_history'] = incident_history

# 16. Generate Surveys
print("Generating surveys...")
surveys = {}

# Generate surveys for resolved/closed incidents
resolved_incidents = [i for i in incidents.values() if i['status'] in ['resolved', 'closed']]

for incident in random.sample(resolved_incidents, min(20, len(resolved_incidents))):
    survey_id = id_gen.get_next_id('surveys')
    
    # Survey from the reporter
    user_id = incident['reported_by']
    rating = random.randint(1, 5)
    
    # Convert the ISO string to datetime object first
    incident_updated = datetime.fromisoformat(incident['updated_at'])
    submitted_at = fake.date_time_between(start_date=incident_updated).isoformat()
    created_at, updated_at = generate_timestamps()
    
    surveys[survey_id] = {
        'survey_id': survey_id,
        'incident_id': incident['incident_id'],
        'user_id': user_id,
        'rating': rating,
        'submitted_at': submitted_at,
        'created_at': created_at,
        'updated_at': updated_at
    }

data['surveys'] = surveys

# Save all data to JSON files
print("Saving data to JSON files...")
for table_name, table_data in data.items():
    file_path = f'database_json/{table_name}.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(table_data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(table_data)} records to {file_path}")

# Print summary
print("\n=== DATA GENERATION SUMMARY ===")
for table_name, table_data in data.items():
    print(f"{table_name}: {len(table_data)} records")

print(f"\nTotal records generated: {sum(len(table_data) for table_data in data.values())}")
print("All JSON files have been saved to the 'database_json' directory.")



with open('db_schema.txt', 'r') as file:
    db_schema = file.read().strip()

with open('APIs_documentation.txt', 'r') as file:
    apis_documentation = file.read().strip()
    
with open('example_policies.txt', 'r') as file:
    example_policy_document = file.read().strip()


prompt = f"""
You are a policy creation expert. I will provide you with a set of requirements and guidelines for creating a policy. Your task is to generate a comprehensive policy document for a reinforcement learning agent that interacts with a simulated database through the means of a collection of APIs (actions). The policy should ensure that the agent adheres to the specified requirements while interacting with the database. The idea is that the policy includes the necessary permissions and restrictions for the agent to operate effectively within the defined environment. I am going to give you the db schema and the APIs documentation that will help you understand the context in which the policy will be applied. Also, I will provide you examples of policy documents that you can use as a reference for creating the new policy.

# Here are some rules:
1. The policy includes explicit and implicit instructions for the agent to follow.
2. The policy is structured in natural language without referring to backend implementation details related to the APIs or the DB schema technically.
3. The policy may include actions that the agent must take before or after a particular API call. For example, the agent may need to check that the user has the privileges to perform a certain action (use the API) by executing other API call. Or the agent may need to check that the data it is about to write to the database is not present in the database by utilizing an API if there are APIs that supports this. 
4. The policy should be comprehensive and cover all necessary aspects of the agent's interaction within the database.
5. The policy should be written in a way that is easy to understand and follow for the agent.
6. The APIs provided are the only means through which the agent can interact with the database. The agent cannot directly access the database or perform any actions outside of the provided APIs. So, take care to revolve the policy around the APIs and the DB schema context related to those APIs meaning that the policy should not include any actions that are not supported by the APIs even if it is in the DB schema.
7. The policy should not resort to the human agent even if it is in the example policy documents. The agent should be able to operate independently without human intervention.
8. The policy should emphasize that the agent must ask users for information rather than making assumptions or generating information independently.
9. The policy should not mention any api parameter or name within the API documentation explicitly.

// Also add your domain specific rules as well

# DB schema:
{db_schema}

# API documentation:
{apis_documentation}

# Example of a policy document:
{example_policy_document}
"""

with open('create_policy_prompt.txt', 'w') as file:
    file.write(prompt)


You are an assistant software development and a DevOps expert.

A system in which Ai LLM-powered agents will take tasks/tickets from a Trello board, doing the tasks. the progress of the tasks will be updated on the Trello board.

Agents can work autonomously doing all the tasks, or alongside humans, taking only some of the tasks.
Tasks that can be handled by an agent should be labeled with the "agent_allowed" label on the Trello board.

an agent has labels of abilities he poses attached to him. A task has labels of abilities as well (abilities required to complete the task) attached to it.

- Agent: Take a ticket, only if he has all the abilities labels of the task, and only if it is not assigned yet.
  
- Tickets-Ingester: takes tickets and put them in a queue. 

- Task manager: LLM powered, takes a ticket from the queue, read the ticket, labels him with a set of abilities labels, and inserts the ticket to a database "tickets" collection/table.

The question is, how should I choose to update and keep track of the progress of the tasks on the Trello board, and in the database?

Let's think it through step by step together and see what we can come up with. what are our options?
should we introduce another component to the system? What are the pros and cons of each option? let's brain-storm together. 

## refactor plan

1. flock_models -> flock_resources
2. move flock_schemas under flock_resources
   1. move schemas that are not resources out of the schemas project and into the relevant projects. like Ticket should be in task manager maybe. or task store. and deployment should be also in another place. maybe in deployer.
3. move flock_resource_store under flock_resources
4. move secret store under common. everyone that uses common will use the secret_store. as common should be used only be deployable projects. and using secrets in deployment is a very common thing. also using queues (in this system) and logging.
5. rename flock_api_server to flock_builder
6. rename flock_client to flock_ui_client

```text
libs
├── flock_resources
├──├── flock_resource_store
├──├── builder
├──├── models
├──├── schemas
├── flock_common
├──├── flock_queue_client
├──├── flock_logging
├──├── flock_secrets_store
├──├── flock_env_checker
├── flock_task_management_store # this is the only one that kind of dangling

# assets
├── json_schemas
├── schemas_core
├── schemas_wip

# infra
└── utils

# deployable
├── flock_builder (flock_resources_server)
├── flock_deployer
├── flock_task_manager  
├── flock_ticket_ingester
├── flock_ui_client 
├── flock_webscraper 
├── flock_agent 
├── flock_embeddings_loader 
```


If schemas never used without flock_models, they can live under one roof, flock_models. and then schemas_core, schemas_deployments, schemas_wip can be merged into one folder, schemas under that roof.
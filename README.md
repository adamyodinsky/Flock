
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
should we introduce another component to the system? What are the pros and cons of each option? let's brain storm together. 

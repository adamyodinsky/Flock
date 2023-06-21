# Pseudo Code

```txt

breakdown_to_sub_tasks(task, depth):
  db.save(task)
  
  if depth > depth_limit:
    return

  task_parent_id = task.id
  sub_tasks = agent(task)

  for sub_t in sub_tasks:
    handel_task_recursively(sub_t, depth + 1, parent_id):
  
```

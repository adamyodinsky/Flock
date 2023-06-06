

```txt
SYSTEM: The date is: Tue Jun  6 16:35:20 IDT 2023. Your knowledge was cut off in September 2021.

Main Task: <main task description>

The task will be given to a highly capable LLM, with a context window of 8000 words.

because of the limitation of 8000 words, we are going to break down the main task to sub tasks of 2 category.


1. pre-requisite sub-tasks list. a sub tasks list that should be done before doing the actual task. like research for example.
2. The main task, break down to smaller sub-tasks so they can be done by an LLM with 8000 words context window limitation.

In both lists, the tasks should be ordered chronologically.

Your answer should be in json format.

example:

{
  "pre-sub-tasks": [
    "do this",
    "do that"
  ],
  "sub-tasks": [
    "do this",
    "do that"
  ]
}
```

Example:

```txt
Main Task: Write an article about the Eurovision contest took place in may 2023.
```

Got this (i add the json syntax highlighting), got a pure json back.

Also, i'm using for this task of breaking tasks to subtasks, temperature of 0, so it will be more obedient, consistent and predictable, wich is better for instructions like that.

```json
{
  "pre-sub-tasks": [
    "Research the history of the Eurovision Song Contest",
    "Find information about the host country and city for the 2023 contest",
    "Collect data on participating countries and their entries",
    "Study the contest's rules and voting system",
    "Review the highlights and controversies of the 2023 contest"
  ],
  "sub-tasks": [
    "Write an introduction to the Eurovision Song Contest and its significance",
    "Describe the host country and city, including their preparations for the event",
    "Present an overview of the participating countries and their entries, focusing on notable acts and fan favorites",
    "Explain the contest's rules and voting system, including any changes made for the 2023 edition",
    "Discuss the highlights of the 2023 contest, such as standout performances and memorable moments",
    "Address any controversies or issues that arose during the event",
    "Summarize the results, including the winner and notable placements",
    "Conclude with the impact of the 2023 contest on the future of Eurovision and the music industry"
  ]
}
```

```pseudo-code
for task in pre-sub-tasks:
    result = do(task)
    result.save()
```


Phase 2 trying to make it recursive, so it will be able to break down sub-tasks to sub-sub-tasks and so on.

```txt
SYSTEM: The date is: Tue Jun  6 16:35:20 IDT 2023. Your knowledge was cut off in September 2021.

Main Task: Write an article about the Eurovision contest took place in may 2023.

The task will be given to a highly capable LLM, with a context window of 8000 words.

Because of the limitation of 8000 words, we are going to break-down the main task to sub tasks of 2 categories.

1. Pre-requisite sub-tasks list. a sub tasks list that should be done before doing the actual task. like research for example.
2. The main task, break down to smaller sub-tasks so they can be done by an LLM with 8000 words context window limitation.

In both lists, the tasks should be ordered chronologically.

your answer should be in json format.
examples:

{
"pre-sub-tasks": [
"do this",
"do that"
],
"sub-tasks": [
"do this",
"do that"
]
}

{
"pre-sub-tasks": [],
"sub-tasks": [
"do this",
"do that"
]
}

{
"pre-sub-tasks": [],
"sub-tasks": []
}

Notice that sometimes the pre-sub-tasks list can be empty because there is no need for something to be done before the task itself.

keep in mind that you will be asked to break-down each sub task to sub tasks recursively. If there is no need to break a task to subtasks any more in order to complete it successfully you can return empty lists like in the example, above.

the answer must be raw pure json object.
```

Answer:

```json
{
  "pre-sub-tasks": [
    "Research the Eurovision 2023 contest details, including host country, city, venue, and dates",
    "Gather information about participating countries, artists, and songs",
    "Collect data on the contest's format, including semi-finals, grand final, and voting system",
    "Find notable moments, controversies, or interesting stories from the event"
  ],
  "sub-tasks": [
    "Introduce the Eurovision 2023 contest, including its history and significance",
    "Describe the host country, city, and venue, including any unique aspects or challenges",
    "Present an overview of the participating countries, artists, and songs, highlighting any favorites or notable entries",
    "Explain the contest's format, including the semi-finals, grand final, and voting system",
    "Discuss the results of the semi-finals and any surprises or upsets",
    "Detail the grand final, including the performances, interval acts, and any notable moments",
    "Analyze the final results, including the winner, top entries, and any controversies or surprises",
    "Conclude with the impact of the Eurovision 2023 contest on the music industry, participating countries, and future contests"
  ]
}
```
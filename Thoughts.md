# Thoughts

## Making docker build faster with caching

- <https://pythonspeed.com/articles/docker-cache-pip-downloads/>

It's not working for now with docker desktop on mac unfortunately.


## The flow of using some knowledge base as an augmented data of an agent.

1. create a vector-store A
   1. choose embedding resource
2. create a webscraper
   1. choose vector-store A
3. create an embeddingloader
   1. choose vector-store A
   2. choose splitter resource
4. create a vector-store-qa tool
   1. choose vector store A
   2. choose llmchat resource
5. deploy the webscraper job with the address source of the knowledge base
6. deploy the embeddingloader job
7. create an agent
   1. choose the vector-store-qa tool in the tools list


Shortcut

1. Choose address source of the knowledge base
2. Choose an existent vector-store resource, or create one
   1. if create
      1. fill in the name of the vector store
      2. fill in description
      3. choose embeddings resource
3. Submit

Automatically in the backend:

the frontend send a request to /shortcut/vectorstore or creating the vector store if needed. returns the vector store id.

then it makes another request for doing the webscraper job, with the vector store id.

then it makes another request for doing the embeddingloader job, with the vector store id.

then it makes another request for creating, or updating the vector-store-qa tool, with the vector store id.


1. create a vector-store A (only if not choose)
2. create a webscraper with the address source of the knowledge base
    1. choose vector-store A
3. create an embeddingloader resource
   1. choose vector-store A
   2. choose a default splitter
4. deploy the webscraper job with the address source of the knowledge base
5. deploy the embeddingloader job
6. create a vector-store-qa tool if the vector store is a new one.
   1. choose vector-store A
   2. choose default llmchat resource


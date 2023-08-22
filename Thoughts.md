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
3. Choosing LLM
   1. if create
      1. fill in the name of the vector store
      2. fill in description
      3. choose embeddings resource
4. Submit

Automatically:

the frontend send a request to /shortcut/vectorstore or creating the vector store if needed. returns the vector store id. - done

then it makes another request for doing the shortcut/webscraper job, with the vector store id.

then it makes another request for doing the shortcut/embeddingloader job, with the vector store details or id as data.

then it makes another requests for deploying the webscraper job, and the embeddingloader job.

then it makes another request for creating, or updating to shortcut/vector-store-qa tool, with the vector store id. need to choose llm. (in th backend i'll search if there is a qa tool with this vector store in the dependencies, i might need to make here a very custom query to mongodb)



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

Create request id ?

## what needs to be done for this to be ready for customers?

1. The code must be in a black box, obfuscated and compiled.
2. There are some essential components in the system that if deployed outside of the client premises. we can make it a Sass based service and we will have more control over the system.
3. A rolling update strategy must be thought of and implemented (if it's a hybrid Sass it may be more complicated). this way we can update the system without downtime. or minimal downtime.
4. Secure Secrets injection within k8s. integration with vault as the secret storage.
https://developer.hashicorp.com/vault/tutorials/kubernetes/vault-secrets-operator
vault secret operator is a k8s operator that can inject secrets into pods. interesting.
5. An alternative for kubernetes can be great, like docker swarm, or even bare metal processes.
6. Fully functional User interface.
7. How to enforce license?

Section 1,2,3 are essential for the system to be ready for customers. How long i estimate this can be done? i think the hardest part in here is the compilation of the code the binary, and obfuscation. technically i tried to do it and it just seemed like an impossible mission.


1. It's a a blocker, i tried pyinstaller and did not succeed. I'll need to try again, and also use some help.
2. It can be done, though need some work. A week of work. 2 days of planning, 3 days of implementation, 2 days of testing.
3. It can be done, 1-2 day of planning.
4. It can be done. 1-3 days of development.
5. It's a lot of work, at least a full month.
6. This is up to Yossi. may take something like a week if we are both focused on it. may takes forever if we are not.


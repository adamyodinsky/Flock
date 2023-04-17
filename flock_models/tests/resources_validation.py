import yaml
from flock_store.resources.fs import ResourceStoreFS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models.openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from flock_models.resources import (
    agent,
    embedding,
    llm,
    splitter,
    vectorstore,
    vectorstore_qa_tool,
)
from flock_models.schemes.base import Kind

path_to_schemas = "tests/schemas/integration"


def main():
    files = {
        "agent": "agent.yaml",
        "vectorstore_qa_tool": "vectorstore_qa_tool.yaml",
        "llm": "llm.yaml",
        "search_tool": "search_tool.yaml",
        "vectorstore": "vectorstore.yaml",
        "embedding": "embedding.yaml",
        "splitter": "splitter.yaml",
    }

    # set a local resource store
    resource_store = ResourceStoreFS(".resource_store")
    secret_store = None

    with open(f"{path_to_schemas}/{files['embedding']}") as manifest_file:
        embedding_resource = embedding.EmbeddingResource(
            manifest=yaml.load(manifest_file, Loader=yaml.FullLoader),
            embedding=OpenAIEmbeddings,
        )

        embedding_resource_key = (
            f"{Kind.embedding.value}/{embedding_resource.manifest.metadata.name}"
        )

        resource_store.put_resource(key=embedding_resource_key, obj=embedding_resource)

    with open(f"{path_to_schemas}/{files['llm']}") as manifest_file:
        llm_resource = llm.LLMResource(
            manifest=yaml.load(manifest_file, Loader=yaml.FullLoader),
            llm_cls=ChatOpenAI,
        )

        llm_resource_key = f"{Kind.llm.value}/{llm_resource.manifest.metadata.name}"
        resource_store.put_resource(key=llm_resource_key, obj=llm_resource)

    with open(f"{path_to_schemas}/{files['vectorstore']}") as manifest_file:
        vectorstore_resource = vectorstore.VectorStoreResource(
            manifest=yaml.load(manifest_file, Loader=yaml.FullLoader),
            vectorstore_cls=Chroma,
            resource_store=resource_store,
        )
        vectorstore_resource_key = (
            f"{Kind.vectorstore.value}/{vectorstore_resource.manifest.metadata.name}"
        )

        resource_store.put_resource(
            key=vectorstore_resource_key, obj=vectorstore_resource
        )

    with open(f"{path_to_schemas}/{files['vectorstore_qa_tool']}") as manifest_file:
        vectorestore_qa_tool_resource = vectorstore_qa_tool.VectorStoreQAToolResource(
            manifest=yaml.load(manifest_file, Loader=yaml.FullLoader),
            chain_cls=RetrievalQAWithSourcesChain,
            resource_store=resource_store,
        )

        vectorestore_qa_tool_resource_key = (
            f"{Kind.tool.value}/{vectorestore_qa_tool_resource.manifest.metadata.name}"
        )
        resource_store.put_resource(
            key=vectorestore_qa_tool_resource_key, obj=vectorestore_qa_tool_resource
        )

    with open(f"{path_to_schemas}/{files['agent']}") as manifest_file:
        agent_resource = agent.SelfAskSearchAgentResource(
            manifest=yaml.load(manifest_file, Loader=yaml.FullLoader),
            resource_store=resource_store,
        )

        agent_resource_key = (
            f"{Kind.agent.value}/{agent_resource.manifest.metadata.name}"
        )
        resource_store.put_resource(key=agent_resource_key, obj=agent_resource)

    print("OK")


main()

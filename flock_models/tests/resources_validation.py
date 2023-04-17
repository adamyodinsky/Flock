import yaml
from flock_models.resources import (
    vectorestore_qa_tool,
    embedding,
    vectorstore,
    splitter,
    )
from flock_store.resources.fs import ResourceStoreFS
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
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
    resource_store = ResourceStoreFS('.resource_store')
    secret_store = None
    
    with open(f"{path_to_schemas}/{files['embedding']}") as manifest_file:
        embedding_resource = embedding.EmbeddingResource(
            manifest = yaml.load(manifest_file, Loader=yaml.FullLoader),
            embedding=OpenAIEmbeddings
            )
        
        embedding_resource_key = f"{Kind.embedding.value}/{embedding_resource.manifest.metadata.name}"

        resource_store.put_resource(
            key=embedding_resource_key,
            obj=embedding_resource
        )

    with open(f"{path_to_schemas}/{files['vectorstore']}") as manifest_file:
        vectorestore_qa_tool.VectorStoreResource(
            manifest = yaml.load(manifest_file, Loader=yaml.FullLoader),
            vectorstore = OpenAIEmbeddings,
            resource_store=resource_store,
            )
    print("OK")

main()
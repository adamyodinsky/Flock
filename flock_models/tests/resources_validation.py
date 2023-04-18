import yaml
from flock_store.resources import ResourceStoreFS
from flock_models.builder import ResourceBuilder
from flock_models.schemes import Kind
from flock_models import resources
from flock_models import schemes

path_to_schemas = "tests/schemas"

def main():
    files = {
        "Agent": "agent.yaml",
        "VectorStoreQATool": "vectorstore_qa_tool.yaml",
        "LLM": "llm.yaml",
        "SearchTool": "search_tool.yaml",
        "VectorStore": "vectorstore.yaml",
        "Embedding": "embedding.yaml",
        "Splitter": "splitter.yaml",
    }

    # Setup
    secret_store = None
    resource_store = ResourceStoreFS(".resource_store")
    resource_builder = ResourceBuilder(resource_store=resource_store, secret_store=secret_store)
                                       

    ### Tests ###

    ### Embedding ###
    
    path = f"{path_to_schemas}/{files[Kind.embedding]}"
    schema = schemes.EmbeddingSchema

    # test load from file
    manifest: schema = resource_store.load_yaml(path, schema)

    # test save and load
    key = (
        f"{Kind.embedding.value}/{manifest.metadata.name}"
    )
    resource_store.put_model(key=key, val=manifest)
    manifest: schema = resource_store.get_model(key=key, schema=schema)

    resource = resource_builder.build_resource(
        manifest=manifest
    )
    print(f"{manifest.kind} - OK")

    # with open(f"{path_to_schemas}/{files['llm']}") as manifest_file:
    # with open(f"{path_to_schemas}/{files['vectorstore']}") as manifest_file:
    # with open(f"{path_to_schemas}/{files['vectorstore_qa_tool']}") as manifest_file:
    # with open(f"{path_to_schemas}/{files['agent']}") as manifest_file:
    


main()

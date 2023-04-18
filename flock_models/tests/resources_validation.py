import yaml
from flock_store.resources import ResourceStoreFS
from flock_models.builder import ResourceBuilder
from flock_models.schemes import Kind
from flock_models import resources
from flock_models import schemes

path_to_schemas = "tests/schemas"
resources_files = {
        "Splitter": "splitter.yaml",
        "Embedding": "embedding.yaml",
        "LLM": "llm.yaml",
        "VectorStore": "vectorstore.yaml",
        "VectorStoreQATool": "vectorstore_qa_tool.yaml",
        "SearchTool": "search_tool.yaml",
    }
agent_file = {"Agent": "agent.yaml"}

# Setup
secret_store = None
resource_store = ResourceStoreFS(".resource_store")
resource_builder = ResourceBuilder(resource_store=resource_store, secret_store=secret_store)


def building_resources_loop(files):
        for kind, file in files.items():
            assert kind in Kind.__members__, f"{kind} is not a valid member of Kind enum"

            path = f"{path_to_schemas}/{file}"
            schema = schemes.Schemas[kind]

            # test loading from yaml file
            manifest: schema = resource_store.load_yaml(path, schema)
            assert manifest.kind == kind, f"kind is not {kind} as expected in the manifest"

            # test save and load from resource store
            key = (f"default/{manifest.kind}/{manifest.metadata.name}")
            resource_store.put_model(key=key, val=manifest)
            manifest: schema = resource_store.get_model(key=key, schema=schema)

            resource_builder.build_resource(
                manifest=manifest
            )
            print(f"{manifest.kind} - OK")

def main():                            
    ########### TEST ###########
    # building_resources_loop(resources_files)
    building_resources_loop(agent_file)

main()

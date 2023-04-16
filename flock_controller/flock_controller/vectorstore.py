from langchain.vectorstores import Chroma
from flock_schemas.vector_store import VectorStore as VectorStoreSchema

# import abc

# class VectorStoreABS(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def get_vector_store(self):
#         pass

#     @staticmethod
#     @abc.abstractmethod
#     def my_abstract_staticmethod():
#         pass


class VectorStore(VectorStoreSchema):
    __vectorstores = {
        "chroma": Chroma,
        "pinecone": "pinecone",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vectorstore = self.__vectorstores[self.spec.vendor](
            persist_directory=self.spec.store.path,
            collection_name=self.metadata.name,
            # TODO: implement get_element_from_objects_db_store
            # Implement an objects store that can be used to store the objects, manifest next to actual python object, i think i'll need to use some kind of serialization
            # embedding_function=get_element_from_objects_store(
            #   name=self.spec.embedding.name,
            #   kind="Embedding",
            #   labels=self.spec.embedding.labels,
            #   )
            collection_metadata={
                "name": self.metadata.name,
                "description": self.metadata.description,
                "source": self.metadata.annotations.get("source"),
            },
        )

    def get_vectorstore(self):
        return self._vectorstore


# apiVersion: flock/v1
# kind: VectorStore
# metadata:
#   name: documentation_vectorstore
#   description: documentation vector store
#   annotations:
#     source: github.com://flockml/flockml
#   labels:
#     app: my_app
# spec:
#   store:
#     vendor: chroma
#     type: local
#     path:  /home/flock/store/
#   embedding:
#     name: my-openai-embedding
#     labels:
#       app: my_app

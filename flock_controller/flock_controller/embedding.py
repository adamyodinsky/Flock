from flock_schemas.embedding import Embedding as EmbeddingSchema
from langchain.embeddings.openai import OpenAIEmbeddings

class Embedding(EmbeddingSchema):
    from langchain.embeddings.openai import OpenAIEmbeddings
    
    __embeddings = {
        "openai": OpenAIEmbeddings,
        "huggingface": "huggingface",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._embedding = self.__embeddings[self.spec.vendor](
          embedding_ctx_length=self.spec.embedding_ctx_length,
          chunk_size=self.spec.chunk_size,
          model_name=self.spec.model,
    )
        
    def get_embedding(self):
        return self._embedding
  
# apiVersion: flock/v1
# kind: Embedding
# metadata:
#   name: my-openai-embedding
#   description: openai embedding
#   labels:
#     app: my_app
# spec:
#   vendor: openai
#   model: text-embedding-ada-002
#   embedding_ctx_length: 4096
#   chunk_size: 1000

from flock_models.schemes.llm import LLM as LLMSchema
from langchain.chat_models import ChatOpenAI

class LLM(LLMSchema):
    
    __llms = {
        "openai": ChatOpenAI,
        "huggingface": "huggingface",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._llm = self.__llms[self.spec.vendor](
          temperature=self.spec.temperature,
          model_name=self.spec.model,
          max_tokens=self.spec.token_limit,
    )
        
    def get_llm(self):
        return self._llm
        

# ---
# apiVersion: flock/v1
# kind: LLM
# # uuid: b70bb61d-6710-48bd-85b0-f32c91f1eed1
# metadata:
#   name: my-openai-llm
#   description: openai language model
#   labels:
#     app: my_app
# spec:
#   vendor: openai
#   model: gpt3.5-turbo
#   token_limit: 1000
#   temperature: 0.5

from google import genai
from google.genai import types
import getpass
import os
class embeddings():
    def __init__(self,model="gemini-embedding-001",tasktype="Question_ANSWERING"):
        self.model = model
        self.tasktype= tasktype
        self.client = genai.Client()

    def create_embeddings(self,text)-> list:
        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(task_type=self.tasktype,output_dimensionality=3072)
        )
        return response.embeddings[0].values
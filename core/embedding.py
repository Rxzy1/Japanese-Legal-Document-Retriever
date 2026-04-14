from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import time


class embeddings():
    def __init__(self,model="gemini-embedding-001",tasktype="QUESTION_ANSWERING"):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = model
        self.tasktype= tasktype
        self.client = genai.Client(api_key=api_key)

    def create_embeddings(self,text)-> list:

        for attempt in range(5):
            try:
                response = self.client.models.embed_content(
                    model=self.model,
                    contents=text,
                    config=types.EmbedContentConfig(task_type=self.tasktype,output_dimensionality=3072)
                )
                return response.embeddings[0].values
            except Exception as e:
                if "429" in str(e):
                    wait = 20*(attempt+1)
                    print(f"Rate Limited, Retrying in {wait} seconds...")
                    time.sleep(wait)
                else:
                    raise
        raise  RuntimeError("Failed to create embeddings, due to rate limit.")
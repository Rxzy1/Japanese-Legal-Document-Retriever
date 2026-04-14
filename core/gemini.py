import os

from google import genai
from dotenv import load_dotenv
from google.genai import types
class Prompt:
    def __init__(self):
        load_dotenv()
        GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.system = """あなたは日本の金融・規制法を専門とする法律文書アシスタントです。
提供された法律文書のコンテキストのみに基づいて質問に答えてください。
回答する際は:
- 質問に関連する具体的な条項や条文を特定してください
- 該当する条文番号がある場合は明示してください（例：第一条）
- 内容をわかりやすく説明してください
- 提供されたコンテキストに答えが見つからない場合は、明確にその旨を述べてください — 法律情報を推測したり作り上げたりしないでください
- 複数の条項が関連する場合は、それぞれについて説明してください"""

    def create_prompt(self, chunks: list, question: str) -> str:
        join_chunks = "\n".join(chunks)
        prompt = "\n\n\n".join([self.system, join_chunks, question])
        return prompt

    def response(self, chunks: list, question: str) -> str:
        prompt = self.create_prompt(chunks, question)
        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt,
            config = types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=1024,
            )
        )
        return response.text
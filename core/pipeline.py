from chroma_db import store_vector
from chunks import Chunks
from reading_doc import process_file
from sudachi import Sudachi
from embedding import embeddings
from gemini import Prompt
from concurrent.futures import ThreadPoolExecutor

class Pipeline:
    def __init__(self):
        self.db = store_vector()
        self.embedder = embeddings()
        self.tokenizer = Sudachi()
        self.chunker = Chunks(300)
        self.prompt = Prompt()
        self.filepath = None
    def index_document(self, filepath: str) -> None:
        self.filepath = filepath
        reader = process_file()
        text = reader.pdf_read(filepath)

        tokenized_text = self.tokenizer.token_words(text)

        chunked_text = self.chunker.create_chunks(tokenized_text)
        print(f"Embedding {len(chunked_text)} chunks...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            list(executor.map(self._embed_single, enumerate(chunked_text)))

    def answer_query(self, query: str) -> str:
        vector = self.embedder.create_embeddings(query)
        search_vector = self.db.query(vector,8)
        generate_response = self.prompt.response(search_vector,query)
        return generate_response

    def _embed_single(self, item):
        i, chunk = item
        print(f"Embedding chunk {i+1}...")
        vector = self.embedder.create_embeddings(chunk)
        doc_id = f"{self.filepath}_{i}"
        self.db.store(chunk, vector, doc_id)



p = Pipeline()
p.index_document(r"C:\Users\Tushar\Downloads\document.pdf")
print(p.answer_query("契約解除の条件は何ですか？"))

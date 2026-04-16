import hashlib
from chroma_db import store_vector
from chunks import Chunks
from reading_doc import process_file
from sudachi import Sudachi
from embedding import embeddings
from gemini import Prompt
from reranking import reranking


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


class Pipeline:
    def __init__(self):
        self.db = store_vector()
        self.doc_embedder = embeddings(tasktype="RETRIEVAL_DOCUMENT")
        self.query_embedder = embeddings(tasktype="QUESTION_ANSWERING")
        self.tokenizer = Sudachi()
        self.chunker = Chunks(600)
        self.prompt = Prompt()
        self.rerank = reranking(512)

    def index_document(self, filepath: str) -> None:
        with open(filepath, "rb") as f:
            doc_hash = hash_bytes(f.read())

        reader = process_file()
        text = reader.pdf_read(filepath)
        doc_metadata = reader.metadata

        tokenized_text = self.tokenizer.token_words(text)
        chunked_text = self.chunker.create_chunks(tokenized_text)
        print(f"Embedding {len(chunked_text)} chunks...")

        vectors = []
        ids = []
        metas = []
        for i, chunk in enumerate(chunked_text):
            print(f"Embedding chunk {i+1}...")
            vectors.append(self.doc_embedder.create_embeddings(chunk))
            ids.append(f"{doc_hash}_{i}")
            metas.append({**doc_metadata, "doc_hash": doc_hash, "chunk_index": i})

        self.db.store(chunked_text, vectors, ids, metas)

    def answer_query(self, query: str, where: dict = None) -> str:
        vector = self.query_embedder.create_embeddings(query)
        search_vector = self.db.query(vector, 20, where=where)
        rerank = self.rerank.rerank(query, search_vector)[:10]
        return self.prompt.response(rerank, query)


if __name__ == "__main__":
    p = Pipeline()
    print(p.answer_query("この条例に違反した場合の罰則は何ですか？"))
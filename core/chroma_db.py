import chromadb
from importlib_metadata import metadata


class store_vector:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=r"C:\Project\Vectors")
        self.collection = self.client.get_or_create_collection("legal_documents")
    def store(self,chunk_text:list,embedding:list,doc_id:list,meta_data:list):
        self.collection.upsert(
            ids=doc_id,
            embeddings=embedding,
            documents=chunk_text,
            metadatas=meta_data,
        )
    def query(self,query_embedding:list,n_results: int = 5,where: dict=None):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )
        return results["documents"][0]

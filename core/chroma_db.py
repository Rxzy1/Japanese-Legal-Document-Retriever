import chromadb
class store_vector:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=r"C:\Project\Vectors")
        self.collection = self.client.get_or_create_collection("legal_documents")
    def store(self,chunk_text:str,embedding:list,doc_id:str):
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[chunk_text]
        )
    def query(self,query_embedding:list,n_results: int = 5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results["documents"][0]

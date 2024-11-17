import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="emi_collection")
documents = [
    {"id":"doc1", "text":"hello world"},
    {"id":"doc2", "text":"how are you today"},
    {"id":"doc3", "text":"i am out of here, good bye, see you later"},
]

for doc in documents:
    collection.upsert(documents=doc['text'], ids=doc['id'])

query_text = 'Hello World'

results = collection.query(
    query_texts=[query_text], 
    n_results=2
)

for idx, document in enumerate(results['documents'][0]):
    doc_id = results['ids'][0][idx]
    distance = results['distances'][0][idx]
    print(f"for the query:{query_text},\nFound similar document:{document} distance:{distance} doc_id:{doc_id}")
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

print(results)
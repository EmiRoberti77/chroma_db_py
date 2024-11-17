import chromadb
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()
croma_client = chromadb.PersistentClient(path='./db/chroma_persist')

collection = croma_client.get_or_create_collection(
    'emi_collection', embedding_function=default_ef)

documents = [
    {"id":"doc1", "text":"hello world"},
    {"id":"doc2", "text":"how are you today"},
    {"id":"doc3", "text":"i am out of here, good bye, see you later"},
    {"id":"doc4","text":"Apple is a tech company"}
]

for doc in documents:
    collection.upsert(ids=doc['id'], documents=[doc['text']])

query_text = 'Age of earth'

results = collection.query(query_texts=[query_text], n_results=2)

for idx, document in enumerate(results["documents"][0]):
    doc_id = results["ids"][0][idx]
    distance = results['distances'][0][idx]
    print(
        f"for the query {query_text}\nFound:{document} distane:{distance} id:{idx}"
    )
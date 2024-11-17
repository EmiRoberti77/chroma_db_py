import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="emi_collection")
collection.add(documents=[
    "this document is about formula 1, the next race in Las Vegas and Ferrari will win",
    "this document is about global economy and 2025 will see great improvements"
], ids=['id1', 'id2'])
results = collection.query(
    query_texts=["this is a document is about formula 1"], 
    n_results=2
)

print(results)
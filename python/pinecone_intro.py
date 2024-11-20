import os
from pinecone import Pinecone
from dotenv import load_dotenv
from pinecone import ServerlessSpec
load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(host='https://emi-pc-example-index-yj74edf.svc.aped-4627-b74a.pinecone.io')

index.upsert(
  vectors=[
    {
      "id": "A", 
      "values": [0.1] * 1536, 
      "metadata": {"genre": "comedy", "year": 2020}
    },
    {
      "id": "B", 
      "values": [0.2] * 1536,
      "metadata": {"genre": "documentary", "year": 2019}
    },
    {
      "id": "C", 
      "values": [0.3] * 1536,
      "metadata": {"genre": "comedy", "year": 2019}
    },
    {
      "id": "D", 
      "values": [0.4] * 1536,
      "metadata": {"genre": "drama"}
    }
  ]
)

res = index.query(
    vector=[0.2] * 1536,
    filter={
        "genre": {"$eq": "documentary"}
    },
    top_k=1,
    include_metadata=True # Include metadata in the response.
)

print(res)
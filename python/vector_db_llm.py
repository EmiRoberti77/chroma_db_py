import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

#create embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key, model_name="text-embedding-3-small"
)

#set up database to save vectors and emdebbing function
chroma_client = chromadb.PersistentClient(path="./db/chroma_persistent_storage")
collection_name = 'document_emi_collection'
collection = chroma_client.get_or_create_collection(
    name=collection_name, embedding_function=openai_ef
)

def load_documents_from_directory(directory_path):
    print('====== loading document =======')
    documents = []
    for filenane in os.listdir(directory_path):
        if(filenane.endswith(".txt")):
            with open( os.path.join(directory_path, filenane), "r", encoding='utf-8') as file:
                documents.append({"id":filenane, "text":file.read()})
    return documents


docs = load_documents_from_directory('./data/new_articles')
print(docs)
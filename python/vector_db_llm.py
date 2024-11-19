import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_key)

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

# method to break a string or section of a document into chunks
def split_text(text, chunck_size=1000, overlap=20):
    chunk = []
    start = 0
    while start < len(text):
        end = start + chunck_size
        chunk.append(text[start:end])
        start = end + overlap
    return chunk

#split document into chunkx
documensts = load_documents_from_directory('./data/new_articles')
chunked_documents = []
for doc in documensts:
    chunks = split_text(doc['text'])
    print("===== splitting document into chunks =====")
    for i, chunk in enumerate(chunks):
        chunked_documents.append({"id": f"{doc["id"]}_chunk{i+1}", "text":chunk})

def get_openai_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    embedding = response.data[0].embedding
    print("===== generating embedding =====")
    return embedding

# Generate embeddings for the document chunks
for doc in chunked_documents:
    print("==== Generating embeddings... ====")
    doc["embedding"] = get_openai_embedding(doc["text"])

# Upsert documents with embeddings into Chroma
for doc in chunked_documents:
    print("==== Inserting chunks into db ====")
    collection.upsert(
        ids=[doc["id"]], documents=[doc["text"]], embeddings=[doc["embedding"]]
    )

# Function to query documents
def query_documents(question, n_results=2):
    # query_embedding = get_openai_embedding(question)
    results = collection.query(query_texts=question, n_results=n_results)

    # Extract the relevant chunks
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    print("==== Returning relevant chunks ====")
    return relevant_chunks


# Function to generate a response from OpenAI
def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    answer = response.choices[0].message
    return answer


question = "give me a brief overview of the articles. Be concise, please."
relevant_chunks = query_documents(question)
answer = generate_response(question, relevant_chunks)

print("==== Answer ====")
print(answer.content)

from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

response = client.embeddings.create(
    input="this is my code and this line will be embedded", 
    model="text-embedding-3-small")

print(response.data[0].embedding)
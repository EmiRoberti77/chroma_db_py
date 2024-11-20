# this is to build a simple langchain.  the full resources for langchain can be found on www.langchain.com
# Emi Roberti
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
load_dotenv()
MODEL = 'gpt-4o-mini'
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model=MODEL)

messages = [
    SystemMessage(content="Translate the text into italian"),
    HumanMessage(content="Hi, how are you doing.  My name is Emi and i am a programmer")
]

response = model.invoke(messages)
print(response.content)

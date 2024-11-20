# this is to build a simple langchain.  the full resources for langchain can be found on www.langchain.com
# Emi Roberti
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.chains import create_retrieval_chain
load_dotenv()

MODEL = 'gpt-4o-mini'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

model = ChatOpenAI(model=MODEL)

#load the docmuents
loader = DirectoryLoader(
    path='./data/new_articles', glob="*.txt", loader_cls=TextLoader
)
document = loader.load()

#split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n"],
    chunk_size=1000,
    chunk_overlap=20,
)
documents = text_splitter.split_documents(document)
print(f"Number of documents: {len(documents)}")

# get embedding 
embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

# create vector store 
persist_directory = "./db/chroma_db_emi_sample"
vectordb = Chroma.from_documents(
    documents=documents, embedding=embedding, persist_directory=persist_directory
)

retriever = vectordb.as_retriever()

# to get the chain to work with the database we created the prompt
# with the {context to be passed in}
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

# Define the system and human message templates
system_message = SystemMessagePromptTemplate.from_template(system_prompt)
human_message = HumanMessagePromptTemplate.from_template("{input}")

# Create the chat prompt template
prompt = ChatPromptTemplate(messages=[system_message, human_message])

# this is where we prepare the tools to be able to ask the question and to assign a 
# LLM to resolve the text that has been found
question_answer_chain = create_stuff_documents_chain(
    llm=model,
    prompt=prompt
)

# this is where the magic happenes, we have a retrieval chain, we pass in the retriver from Chroma 
# and the quetion_answer_chain, this will resolve the query reading the relevant documents
# and passing them to the LLM to create a logical response
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#the chain is ready and can be invoked
response = rag_chain.invoke({
    "input":"talk about databricks news"
})

# extract the answer from the JSON output
res = response["answer"]

print(res)

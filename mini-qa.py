import os
from openai import OpenAI
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from datasets import load_dataset
from astrapy.db import AstraDB

# Initialize the client
db = AstraDB(
  token=os.environ["ASTRA_DB_TOKEN"],
  api_endpoint=os.environ["ASTRA_DB_END_POINT"],
  namespace=os.environ["ASTRA_DB_KEYSPACE"])

print(f"Connected to Astra DB: {db.get_collections()}")

llm = OpenAI()
my_embedding = OpenAIEmbeddings()

vstore = AstraDBVectorStore(
    embedding=my_embedding,collection_name=os.environ["ASTRA_DB_COLLECTION"],
    api_endpoint=os.environ["ASTRA_DB_END_POINT"],
    token=os.environ["ASTRA_DB_TOKEN"],
    namespace=os.environ["ASTRA_DB_KEYSPACE"]
)

print("Loading data from HuggingFace")
my_dataset = load_dataset("Biddls/Onion_News", split="train")
headlines = my_dataset["text"][:50]

print("\nGenerating embeddings and storing in AstraDB")
vstore.add_texts(headlines)

print("Inserted %i headlines.\n" % len(headlines))

vector_index = VectorStoreIndexWrapper(vectorstore=vstore)

first_question = True
while True:
    if first_question:
        query_text = input("\nEnter your next question (or type 'quit' to exit): ")
        first_question = False
    else:
        query_text = input("\nWhat's your next question (or type 'quit' to exit): ")

    if query_text.lower() == 'quit':
        break

    print(f"QUESTION: {query_text}")
    answer = vector_index.query(query_text, llm=llm)
    print(f"ANSWER: {answer}")

    print("DOCUMENTS BY RELEVANCE: ")
    for doc, score in vstore.similarity_search_with_score(query_text, k=4):
        print(score, doc.page_content[:60])
    

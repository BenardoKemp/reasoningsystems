from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from openai import OpenAI

# Load documents
loader = TextLoader("knowledge.txt")
documents = loader.load()

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create vector DB
vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

# Create retriever
retriever = vectorstore.as_retriever()

# Query
query = "Explain Chain-of-Thought reasoning"

results = retriever.get_relevant_documents(query)

context = "\n".join(
    [doc.page_content for doc in results]
)

prompt = f"""
Use the context below:

{context}

Question:
{query}
"""

# Generate answer
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
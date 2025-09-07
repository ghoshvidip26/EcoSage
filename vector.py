from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load dataset
df = pd.read_csv("dataset.csv")

# Embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Chroma DB path
db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []
    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={
                "country": row.get("country", ""),
                "sector": row.get("sector", ""),
                "value": row.get("value", ""),
                "date": row.get("date", ""),
                "timestamp": row.get("timestamp", "")
            },
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

# Create vector store
vector_store = Chroma(
    collection_name="carbon_footprint_reviews",
    embedding_function=embeddings,
    persist_directory=db_location
)

# Add docs if db was empty
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Expose retriever (default without filters)
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load dataset
df = pd.read_csv("Crop_recommendation.csv")
print(df.columns)
print(df.head())

# Embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Chroma DB path
db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)
# N,P,K,temperature,humidity,ph,rainfall,label
if add_documents:
    documents = []
    ids = []
    for i, row in df.iterrows():
        # Use the actual column names from the CSV
        N = row.get("N", "") if "N" in df.columns else row.get(df.columns[0], "")
        P = row.get("P", "") if "P" in df.columns else row.get(df.columns[1], "")
        K = row.get("K", "") if "K" in df.columns else row.get(df.columns[2], "")
        temperature = row.get("temperature", "") if "temperature" in df.columns else row.get(df.columns[3], "")
        humidity = row.get("humidity", "") if "humidity" in df.columns else row.get(df.columns[4], "")
        ph = row.get("ph", "") if "ph" in df.columns else row.get(df.columns[5], "")
        rainfall = row.get("rainfall", "") if "rainfall" in df.columns else row.get(df.columns[6], "")
        label = row.get("label", "") if "label" in df.columns else row.get(df.columns[7], "")
        document = Document(
            page_content=f"N: {N}, P: {P}, K: {K}, Temperature: {temperature}, Humidity: {humidity}, pH: {ph}, Rainfall: {rainfall}, Label: {label}",
            metadata={
                "N": row.get("N", ""),
                "P": row.get("P", ""),
                "K": row.get("K", ""),
                "temperature": row.get("temperature", ""),
                "humidity": row.get("humidity", ""),
                "ph": row.get("ph", ""),
                "label": row.get("label", ""),
            },
        )
        ids.append(str(i))
        documents.append(document)

# Create vector store
vector_store = Chroma(
    collection_name="crop_recommendations",
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

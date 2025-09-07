from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever, vector_store

model = OllamaLLM(model="llama3.2")

def format_reviews(docs):
    formatted = []
    for d in docs:
        meta = d.metadata
        formatted.append(
            f"Review: {d.page_content}\n"
            f"Country: {meta.get('country')}, Sector: {meta.get('sector')}, "
            f"Value: {meta.get('value')}, Date: {meta.get('date')}, Timestamp: {meta.get('timestamp')}"
        )
    return "\n\n".join(formatted)

def build_filter(question: str):
    filters = []
    q = question.lower()

    if "india" in q:
        filters.append({"country": {"$eq": "India"}})
    if "transport" in q:
        filters.append({"sector": {"$eq": "Transport"}})
    if "energy" in q:
        filters.append({"sector": {"$eq": "Energy"}})
    if "food" in q:
        filters.append({"sector": {"$eq": "Food"}})

    if filters:
        return {"$and": filters}
    return None

template = """
You are an expert on reducing carbon footprint.

Here are some relevant reviews with context:
{reviews}

The reviews may include:
- Country
- Date
- Sector (like transport, energy, food)
- Value (numerical score/impact)

The user has a question:
{question}

Use the reviews and their metadata to provide personalized, actionable eco-friendly advice.
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n--------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    query_filter = build_filter(question)
    docs = vector_store.similarity_search(
        question,
        k=5,
        filter=query_filter
    )

    reviews = format_reviews(docs)
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)

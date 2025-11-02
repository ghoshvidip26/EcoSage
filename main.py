from langchain_ollama import ChatOllama 
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever, vector_store
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import TOOLS

class EcoAdvice(BaseModel):
    topic: str = Field(..., description="Main sustainability topic")
    summary: str = Field(..., description="Concise eco-friendly advice")
    actions: list[str] = Field(..., description="List of actionable steps")
    sources: list[str] = Field(..., description="References or sources if available")

model = ChatOllama(model="llama3.2")

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

template = template = """
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
{agent_scratchpad}
"""

parser = PydanticOutputParser(pydantic_object=EcoAdvice)
prompt = ChatPromptTemplate.from_template(template)

agent = create_tool_calling_agent(
    llm=model,
    prompt=prompt,
    tools=TOOLS
)

agent_executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True)

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
    result = agent_executor.invoke({"reviews": reviews, "question": question})
    print("Result: ", result)
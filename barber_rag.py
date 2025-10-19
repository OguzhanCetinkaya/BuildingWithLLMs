import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

user_prompt = input("AI: How can I assist you today? \nUser: ")

instructions= """
You are a barber assistant that extracts user intent from input.

The user may ask either for services or business information.
Extract the intent type and relevant details from the user input.

intent types can be:
1. service_inquiry
2. business_information

Return the result in following json format {{"intent": "", "details": ""}}
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",instructions),
        ("human", user_prompt),
    ]
)
chain = prompt | llm

response = chain.invoke({"input_text":user_prompt})
data = json.loads(response.content)

intent = data["intent"]
details = data["details"]

if intent == "service_inquiry":
    with open("barber_services.txt", "r") as f:
        rag_context = f.read()
elif intent == "business_information":
    with open("barber_business_info.txt", "r") as f:
        rag_context = f.read()
else:
    rag_context = "No relevant information found."

instructions = """
You are a barber assistant that helps users based on their intent.

Answer the user's question based on following context:
{rag_context}
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", details),
    ]
)

chain = prompt | llm
response = chain.invoke(
    {
        "rag_context": rag_context
    }
)
print("AI: " + response.content)

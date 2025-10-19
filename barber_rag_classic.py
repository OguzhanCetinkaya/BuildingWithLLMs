import json
import sqlite3

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

def get_appointment_info():
    """Query the database for appointment information based on user details."""
    conn = sqlite3.connect('barber_appointments.db')
    cursor = conn.cursor()

    # Get all appointments with relevant information
    cursor.execute('''
        SELECT id, customer_name, phone_number, appointment_date, appointment_time,
               service_type, barber_name, duration_minutes, price, status, notes
        FROM appointments
        ORDER BY appointment_date, appointment_time
    ''')

    appointments = cursor.fetchall()
    conn.close()

    # Format the appointment information as context
    context = "Current Appointments:\n\n"
    for apt in appointments:
        context += f"ID: {apt[0]}\n"
        context += f"Customer: {apt[1]}\n"
        context += f"Phone: {apt[2]}\n"
        context += f"Date: {apt[3]}\n"
        context += f"Time: {apt[4]}\n"
        context += f"Service: {apt[5]}\n"
        context += f"Barber: {apt[6]}\n"
        context += f"Duration: {apt[7]} minutes\n"
        context += f"Price: ${apt[8]}\n"
        context += f"Status: {apt[9]}\n"
        if apt[10]:
            context += f"Notes: {apt[10]}\n"
        context += "\n"

    return context

    with open("barber_services.txt", "r") as f:
        rag_context = f.read()

    with open("barber_business_info.txt", "r") as f:
        rag_context = f.read()

barber_services = ""
with open("barber_services.txt", "r") as f:
    barber_services = f.read()
barber_business_info = ""
with open("barber_business_info.txt", "r") as f:
        barber_business_info = f.read()


vector_store = InMemoryVectorStore(embeddings)

document_1 = Document(
    page_content=barber_services,
    metadata={"type": "services"},
)
document_2 = Document(
    page_content=barber_business_info,
    metadata={"type": "business_info"},
)
document_3 = Document(
    page_content=get_appointment_info(),
    metadata={"type": "appointment_info"},
)

documents = [document_1, document_2, document_3]
vector_store.add_documents(documents=documents)

user_prompt = input("AI: How can I assist you today? \nUser: ")
instructions= """
You are a barber assistant that extracts user intent from input.

The user may ask for services, business information, or appointment information.
Extract the intent type and relevant details from the user input.

intent types can be:
1. service_inquiry
2. business_information
3. appointment_information

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

query = details
rag_context = vector_store.similarity_search(
    query = query,
    k=3,
    )

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

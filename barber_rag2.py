import json
import sqlite3

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

user_prompt = input("AI: How can I assist you today? \nUser: ")

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

if intent == "service_inquiry":
    with open("barber_services.txt", "r") as f:
        rag_context = f.read()
elif intent == "business_information":
    with open("barber_business_info.txt", "r") as f:
        rag_context = f.read()
elif intent == "appointment_information":
    rag_context = get_appointment_info()
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

import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

instructions= """
You are an assistant that extracts details from user input.
Extract the person type, location, and interests from the user input.
Return the result in following json format {{"person": "", "location": "", "interests": ""}}
"""
user_prompt = "{input_text}"
prompt = ChatPromptTemplate.from_messages(
    [
        ( "system",instructions),
        ("human", user_prompt),
    ]
)
chain = prompt | llm
user_prompt = input("Describe a person, location, and interests: ")
response = chain.invoke({"input_text":user_prompt})
data = json.loads(response.content)

person = data["person"]
location = data["location"]
interests = data["interests"]

instructions = "You are an assistant that helps people to plan their days effectively."
user_prompt = "Plan a weekend day for {person} in {location} who likes {interests}."
prompt = ChatPromptTemplate.from_messages(
    [
        ( "system",instructions),
        ("human", user_prompt),
    ]
)


chain = prompt | llm
response = chain.invoke(
    {
        "person": person,
        "location": location,
        "interests": interests,
    }
)
print(response.content)
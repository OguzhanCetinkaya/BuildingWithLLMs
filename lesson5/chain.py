from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

instructions = "You are an assistant that helps people to plan their days effectively."
user_prompt = "Plan a weekend day for {person} in {location} who likes {interests}."
prompt = ChatPromptTemplate.from_messages(
    [
        ( "system",instructions),
        ("human", user_prompt),
    ]
)

person = input("Enter a person type: ")
location = input("Enter the location: ")
interests = input("Enter the person's interests: ")

chain = prompt | llm
response = chain.invoke(
    {
        "person": person,
        "location": location,
        "interests": interests,
    }
)
print(response.content)
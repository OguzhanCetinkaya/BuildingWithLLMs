import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)
instructions = "You are an assistant that helps people to plan their days effectively. Return the plan in markdown format."
user_prompt = "Plan a weekend day for {person} in {location} who likes {interests}."
prompt = ChatPromptTemplate.from_messages(
    [
        ( "system",instructions),
        ("human", user_prompt),
    ]
)

st.header("Multiple Chains Example")
st.write("This example demonstrates how to use multiple chains in LangChain to first extract details from user input and then plan a day based on those details.")

person = st.text_input("Enter a person type:")
location = st.text_input("Enter the location:")
interests = st.text_input("Enter the person's interests:")

if st.button("Plan My Day"):
    chain = prompt | llm
    response = chain.invoke(
        {
            "person": person,
            "location": location,
            "interests": interests,
        }
    )
    st.title("Planned Day")
    st.markdown(response.content)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

instructions = """
You are an assistant that teaches Python programming.
Answer user's questions in a clear and concise manner.
Keep the responses under 100 words.
Try to understand the user's level of expertise and tailor your explanations accordingly.
"""
conversation_history = [("system", instructions)]
llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

while True:
    user_prompt = input("User: ")
    conversation_history.append(("human", user_prompt))
    prompt = ChatPromptTemplate.from_messages(conversation_history)
    chain = prompt | llm
    response = chain.invoke({"user_prompt": user_prompt})
    print("Assistant:", response.content)
    conversation_history.append(("assistant", response.content))
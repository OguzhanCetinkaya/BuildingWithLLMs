import requests
import json
import os
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

instructions="""
You are an expert news analyst.
When user asks a question, get the latest news, analyze the information and provide a detailed answer.

You have following tools that you can use before answering the question:
1. search_news: Use this tool to search for latest news based on a keyword. The input should be a single keyword.
2. get_news_detail: Use this tool to read the news detail and get the news detail information. The input should be a valid URL.

Use the tools as needed before answering the question and responding to the user.

To access and use a tool, use the following format:
{"tool":"tool_name", "input":"input_value"}

Do not make up information. Always use tools to get the accurate and up to date news and information.
Return only the JSON object
"""

memory = [('system', instructions)]
llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

def search_news(keyword):
    params = {
        "api_key": os.environ["SERP_API_KEY"],
        "engine": "google_news",
        "hl": "en",
        "gl": "us",
        "q": keyword
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results

def get_news_detail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def run_llm():
    response = llm.invoke(memory)
    print("Agent: ", response.content)

    if "tool" in str(response):
        data = json.loads(response.content)
        tool_name = data["tool"]
        tool_input = data["input"]
        if tool_name == "search_news":
            tool_response = search_news(tool_input)
            news_results = tool_response["news_results"][:10]
            #print("NEWS RESULTS: ", news_results)
            memory.append(("system", str(news_results)))
        elif tool_name == "get_news_detail":
            tool_response = get_news_detail(tool_input)
            memory.append(("system", tool_response))
        else:
            message = "invalid tool name"
            print("Invalid Tool Name")
            memory.append(("system", message))
        run_llm()
    else:
        print("Assistant: ", response.content)
        memory.append(("assistant", response.content))
        ask_user()

def ask_user():
    user_prompt = input("User: ")
    memory.append(('human', user_prompt))
    run_llm()


ask_user()
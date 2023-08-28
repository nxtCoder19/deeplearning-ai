import os
import pymongo
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools.base import BaseTool
from langchain.tools import Tool, StructuredTool, tool
import json
import feedparser

import warnings

import openai
warnings.filterwarnings("ignore")

openai.api_key  = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(temperature=0)

def fetchDataFromRssUrl(url: str) :
    hackerNewsFeed = feedparser.parse(url)
    return hackerNewsFeed.entries[1]
    # return f"results: `{hackerNewsFeed.entries}`"
    

tools = [
    StructuredTool.from_function(
        name="DataFetcherFromRssUrl",
        description="take url as argument and returns data ",
        func=fetchDataFromRssUrl
        )
]


# obj = StructuredTool(name="asdfasd", func=fetchDataFromCollection)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True
)

# print(agent.run("Are there any results in `https://hnrss.org/newest` rss url?"))
print(agent.run("get data from url `https://hnrss.org/newest`"))

# print(fetchDataFromRssUrl("https://hnrss.org/newest"))
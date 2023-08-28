import os
import pymongo
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools.base import BaseTool
from langchain.tools import Tool, StructuredTool, tool
import json

import warnings

import openai
warnings.filterwarnings("ignore")

openai.api_key  = os.getenv('OPENAI_API_KEY')


mongo_host = "localhost"
mongo_port = 27017 
mongo_username = "root"  
mongo_password = "rootpassword" 
mongo_database = "config"

client = pymongo.MongoClient(
    host=mongo_host,
    port=mongo_port,
    username=mongo_username,
    password=mongo_password,
    # authSource=mongo_database
)

db = client[mongo_database]

llm = ChatOpenAI(temperature=0)
# tools = load_tools(["llm-math", "wikipedia"], llm=llm)

def fetchDataFromCollection(collectionName: str, query: dict) -> []:
    collection = db[collectionName]
    result = collection.find(query)

    data = [x for x in result]
    return f"results: `{data}`"

tools = [
    StructuredTool.from_function(
        name="asdfasd",
        description="useful to fetch data from the given collection in mongo. It will take collection name as first parameter and query are second parameter. It will respond with results that match the query.",
        func=fetchDataFromCollection
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

agent.run("Are there any results in `configs` collection?")

print(agent.run("Are there any results in `configs` collection?"))
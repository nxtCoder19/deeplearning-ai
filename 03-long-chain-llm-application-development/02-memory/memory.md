# LangChain: Memory

## Outline
* ConversationBufferMemory
* ConversationBufferWindowMemory
* ConversationTokenBufferMemory
* ConversationSummaryMemory

## ConversationBufferMemory


```python
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import warnings
warnings.filterwarnings('ignore')
```


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

```


```python
llm = ChatOpenAI(temperature=0.0)
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)
```


```python
conversation.predict(input="Hi, my name is Andrew")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    
    Human: Hi, my name is Andrew
    AI:[0m
    
    [1m> Finished chain.[0m





    "Hello Andrew! It's nice to meet you. How can I assist you today?"




```python
conversation.predict(input="What is 1+1?")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    Human: Hi, my name is Andrew
    AI: Hello Andrew! It's nice to meet you. How can I assist you today?
    Human: What is 1+1?
    AI:[0m
    
    [1m> Finished chain.[0m





    '1+1 is equal to 2.'




```python
conversation.predict(input="What is my name?")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    Human: Hi, my name is Andrew
    AI: Hello Andrew! It's nice to meet you. How can I assist you today?
    Human: What is 1+1?
    AI: 1+1 is equal to 2.
    Human: What is my name?
    AI:[0m
    
    [1m> Finished chain.[0m





    'Your name is Andrew.'




```python
print(memory.buffer)
```

    Human: Hi, my name is Andrew
    AI: Hello Andrew! It's nice to meet you. How can I assist you today?
    Human: What is 1+1?
    AI: 1+1 is equal to 2.
    Human: What is my name?
    AI: Your name is Andrew.



```python
memory.load_memory_variables({})
```




    {'history': "Human: Hi, my name is Andrew\nAI: Hello Andrew! It's nice to meet you. How can I assist you today?\nHuman: What is 1+1?\nAI: 1+1 is equal to 2.\nHuman: What is my name?\nAI: Your name is Andrew."}




```python
memory = ConversationBufferMemory()
```


```python
memory.save_context({"input": "Hi"}, 
                    {"output": "What's up"})
```


```python
print(memory.buffer)
```

    Human: Hi
    AI: What's up



```python
memory.load_memory_variables({})
```




    {'history': "Human: Hi\nAI: What's up"}




```python
memory.save_context({"input": "Not much, just hanging"}, 
                    {"output": "Cool"})
```


```python
memory.load_memory_variables({})
```




    {'history': "Human: Hi\nAI: What's up\nHuman: Not much, just hanging\nAI: Cool"}



## ConversationBufferWindowMemory


```python
from langchain.memory import ConversationBufferWindowMemory
```


```python
memory = ConversationBufferWindowMemory(k=1)               
```


```python
memory.save_context({"input": "Hi"},
                    {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

```


```python
memory.load_memory_variables({})
```




    {'history': 'Human: Not much, just hanging\nAI: Cool'}




```python
llm = ChatOpenAI(temperature=0.0)
memory = ConversationBufferWindowMemory(k=1)
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=False
)
```


```python
conversation.predict(input="Hi, my name is Andrew")
```




    "Hello Andrew! It's nice to meet you. How can I assist you today?"




```python
conversation.predict(input="What is 1+1?")
```




    '1+1 is equal to 2.'




```python
conversation.predict(input="What is my name?")
```




    "I'm sorry, but I don't have access to personal information."



## ConversationTokenBufferMemory


```python
#!pip install tiktoken
```


```python
from langchain.memory import ConversationTokenBufferMemory
from langchain.llms import OpenAI
llm = ChatOpenAI(temperature=0.0)
```


```python
memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=30)
memory.save_context({"input": "AI is what?!"},
                    {"output": "Amazing!"})
memory.save_context({"input": "Backpropagation is what?"},
                    {"output": "Beautiful!"})
memory.save_context({"input": "Chatbots are what?"}, 
                    {"output": "Charming!"})
```


```python
memory.load_memory_variables({})
```




    {'history': 'AI: Beautiful!\nHuman: Chatbots are what?\nAI: Charming!'}



## ConversationSummaryMemory


```python
from langchain.memory import ConversationSummaryBufferMemory

```


```python
# create a long string
schedule = "There is a meeting at 8am with your product team. \
You will need your powerpoint presentation prepared. \
9am-12pm have time to work on your LangChain \
project which will go quickly because Langchain is such a powerful tool. \
At Noon, lunch at the italian resturant with a customer who is driving \
from over an hour away to meet you to understand the latest in AI. \
Be sure to bring your laptop to show the latest LLM demo."

memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
memory.save_context({"input": "Hello"}, {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})
memory.save_context({"input": "What is on the schedule today?"}, 
                    {"output": f"{schedule}"})
```


```python
memory.load_memory_variables({})
```




    {'history': 'System: The human and AI exchange greetings. The human mentions that they are not doing much. The AI informs the human about their schedule for the day, including a meeting with the product team, working on the LangChain project, and having lunch with a customer to discuss the latest in AI. The AI also reminds the human to bring their laptop to show a demo.'}




```python
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)
```


```python
conversation.predict(input="What would be a good demo to show?")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    System: The human and AI exchange greetings. The human mentions that they are not doing much. The AI informs the human about their schedule for the day, including a meeting with the product team, working on the LangChain project, and having lunch with a customer to discuss the latest in AI. The AI also reminds the human to bring their laptop to show a demo.
    Human: What would be a good demo to show?
    AI:[0m
    
    [1m> Finished chain.[0m





    'A good demo to show would be a live demonstration of the LangChain project. You can showcase the features and functionality of the language translation software, highlighting its accuracy and efficiency. Additionally, you could also demonstrate any recent updates or improvements made to the project. This would give the customer a firsthand experience of the capabilities of the AI technology and its potential benefits for their business.'




```python
memory.load_memory_variables({})
```




    {'history': 'System: The human and AI exchange greetings. The human mentions that they are not doing much. The AI informs the human about their schedule for the day, including a meeting with the product team, working on the LangChain project, and having lunch with a customer to discuss the latest in AI. The AI also reminds the human to bring their laptop to show a demo.\nHuman: What would be a good demo to show?\nAI: A good demo to show would be a live demonstration of the LangChain project. You can showcase the features and functionality of the language translation software, highlighting its accuracy and efficiency. Additionally, you could also demonstrate any recent updates or improvements made to the project. This would give the customer a firsthand experience of the capabilities of the AI technology and its potential benefits for their business.'}


# Attachments:
![Alt text](<Screenshot 2023-08-19 at 1.27.19 PM.png>)
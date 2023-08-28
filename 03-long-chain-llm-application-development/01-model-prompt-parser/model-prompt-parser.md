# LangChain: Models, Prompts and Output Parsers
Outline

    Direct API calls to OpenAI
    API calls through LangChain:
        Prompts
        Models
        Output parsers

Get your OpenAI API Key

#!pip install python-dotenv

#!pip install openai

```python
import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']
```

Chat API : OpenAI

Let's start with a direct API calls to OpenAI.

```python
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )

    return response.choices[0].message["content"]
```

​

```python
get_completion("What is 1+1?")

'1+1 equals 2.
```

```python
customer_email = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse,\
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!

"""
```
```python
style = """American English \

in a calm and respectful tone

"""
```
```python
prompt = f"""Translate the text \

that is delimited by triple backticks 

into a style that is {style}.

text: ```{customer_email}```

"""
```
​

```python
print(prompt)

Translate the text that is delimited by triple backticks 
into a style that is American English in a calm and respectful tone
.
text: ```
Arrr, I be fuming that me blender lid flew off and splattered me kitchen walls with smoothie! And to make matters worse,the warranty don't cover the cost of cleaning up me kitchen. I need yer help right now, matey!
```

```python
response = get_completion(prompt)

response

'I am quite frustrated that my blender lid flew off and made a mess of my kitchen walls with smoothie! To add to my frustration, the warranty does not cover the cost of cleaning up my kitchen. I kindly request your assistance at this moment, my friend.'
```
Chat API : LangChain

Let's try how we can do the same using LangChain.

#!pip install --upgrade langchain

Model

from langchain.chat_models import ChatOpenAI

# To control the randomness and creativity of the generated

# text by an LLM, use temperature = 0.0

```python
chat = ChatOpenAI(temperature=0.0)

chat

ChatOpenAI(verbose=False, callbacks=None, callback_manager=None, client=<class 'openai.api_resources.chat_completion.ChatCompletion'>, model_name='gpt-3.5-turbo', temperature=0.0, model_kwargs={}, openai_api_key=None, openai_api_base=None, openai_organization=None, request_timeout=None, max_retries=6, streaming=False, n=1, max_tokens=None)
```
```python
Prompt template

template_string = """Translate the text \

that is delimited by triple backticks \

into a style that is {style}. \

text: ```{text}```

"""
```

```python
from langchain.prompts import ChatPromptTemplate

​

prompt_template = ChatPromptTemplate.from_template(template_string)

​

prompt_template.messages[0].prompt

PromptTemplate(input_variables=['style', 'text'], output_parser=None, partial_variables={}, template='Translate the text that is delimited by triple backticks into a style that is {style}. text: ```{text}```\n', template_format='f-string', validate_template=True)
```
```python
prompt_template.messages[0].prompt.input_variables

['style', 'text']
```
```python
customer_style = """American English \

in a calm and respectful tone

"""

customer_email = """

Arrr, I be fuming that me blender lid \

flew off and splattered me kitchen walls \

with smoothie! And to make matters worse, \

the warranty don't cover the cost of \

cleaning up me kitchen. I need yer help \

right now, matey!

"""
```
```python
customer_messages = prompt_template.format_messages(

                    style=customer_style,

                    text=customer_email)

print(type(customer_messages))

print(type(customer_messages[0]))

<class 'list'>
<class 'langchain.schema.HumanMessage'>
```
```python
print(customer_messages[0])

content="Translate the text that is delimited by triple backticks into a style that is American English in a calm and respectful tone\n. text: ```\nArrr, I be fuming that me blender lid flew off and splattered me kitchen walls with smoothie! And to make matters worse, the warranty don't cover the cost of cleaning up me kitchen. I need yer help right now, matey!\n```\n" additional_kwargs={} example=False
```
# Call the LLM to translate to the style of the customer message

```python
customer_response = chat(customer_messages)

print(customer_response.content)

I'm really frustrated that my blender lid flew off and made a mess of my kitchen walls with smoothie! And to make things even worse, the warranty doesn't cover the cost of cleaning up my kitchen. I could really use your help right now, my friend!
```
```python
service_reply = """Hey there customer, \

the warranty does not cover \

cleaning expenses for your kitchen \

because it's your fault that \

you misused your blender \

by forgetting to put the lid on before \

starting the blender. \

Tough luck! See ya!

"""

service_style_pirate = """\

a polite tone \

that speaks in English Pirate\

"""
```
```python
service_messages = prompt_template.format_messages(

    style=service_style_pirate,

    text=service_reply)

​

print(service_messages[0].content)

Translate the text that is delimited by triple backticks into a style that is a polite tone that speaks in English Pirate. text: ```Hey there customer, the warranty does not cover cleaning expenses for your kitchen because it's your fault that you misused your blender by forgetting to put the lid on before starting the blender. Tough luck! See ya!
```
```
```python
service_response = chat(service_messages)

print(service_response.content)

Ahoy there, matey! I regret to inform ye that the warranty be not coverin' the costs o' cleanin' yer galley, as 'tis yer own fault fer misusin' yer blender by forgettin' to secure the lid afore ye started blendin'. Aye, tough luck, me heartie! Fare thee well!
```
```python
Output Parsers

Let's start with defining how we would like the LLM output to look like:

{

  "gift": False,

  "delivery_days": 5,

  "price_value": "pretty affordable!"

}

{'gift': False, 'delivery_days': 5, 'price_value': 'pretty affordable!'}
```
```python
customer_review = """\

This leaf blower is pretty amazing.  It has four settings:\

candle blower, gentle breeze, windy city, and tornado. \

It arrived in two days, just in time for my wife's \

anniversary present. \

I think my wife liked it so much she was speechless. \

So far I've been the only one using it, and I've been \

using it every other morning to clear the leaves on our lawn. \

It's slightly more expensive than the other leaf blowers \

out there, but I think it's worth it for the extra features.

"""
```
​

```python
review_template = """\

For the following text, extract the following information:

​

gift: Was the item purchased as a gift for someone else? \

Answer True if yes, False if not or unknown.

​

delivery_days: How many days did it take for the product \

to arrive? If this information is not found, output -1.

​

price_value: Extract any sentences about the value or price,\

and output them as a comma separated Python list.

​

Format the output as JSON with the following keys:

gift

delivery_days

price_value

​

text: {text}

"""
```
```python
from langchain.prompts import ChatPromptTemplate

​

prompt_template = ChatPromptTemplate.from_template(review_template)

print(prompt_template)

input_variables=['text'] output_parser=None partial_variables={} messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['text'], output_parser=None, partial_variables={}, template='For the following text, extract the following information:\n\ngift: Was the item purchased as a gift for someone else? Answer True if yes, False if not or unknown.\n\ndelivery_days: How many days did it take for the product to arrive? If this information is not found, output -1.\n\nprice_value: Extract any sentences about the value or price,and output them as a comma separated Python list.\n\nFormat the output as JSON with the following keys:\ngift\ndelivery_days\nprice_value\n\ntext: {text}\n', template_format='f-string', validate_template=True), additional_kwargs={})]
```
```python
messages = prompt_template.format_messages(text=customer_review)

chat = ChatOpenAI(temperature=0.0)

response = chat(messages)

print(response.content)

​

{
  "gift": false,
  "delivery_days": 2,
  "price_value": ["It's slightly more expensive than the other leaf blowers out there, but I think it's worth it for the extra features."]
}

type(response.content)

str
```
# You will get an error by running this line of code 

# because'gift' is not a dictionary

# 'gift' is a string

response.content.get('gift')

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[32], line 4
      1 # You will get an error by running this line of code 
      2 # because'gift' is not a dictionary
      3 # 'gift' is a string
----> 4 response.content.get('gift')

AttributeError: 'str' object has no attribute 'get'

Parse the LLM output string into a Python dictionary

from langchain.output_parsers import ResponseSchema

from langchain.output_parsers import StructuredOutputParser

gift_schema = ResponseSchema(name="gift",

                             description="Was the item purchased\

                             as a gift for someone else? \

                             Answer True if yes,\

                             False if not or unknown.")

delivery_days_schema = ResponseSchema(name="delivery_days",

                                      description="How many days\

                                      did it take for the product\

                                      to arrive? If this \

                                      information is not found,\

                                      output -1.")

price_value_schema = ResponseSchema(name="price_value",

                                    description="Extract any\

                                    sentences about the value or \

                                    price, and output them as a \

                                    comma separated Python list.")

​

response_schemas = [gift_schema, 

                    delivery_days_schema,

                    price_value_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()

​

print(format_instructions)

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

```json
{
	"gift": string  // Was the item purchased                             as a gift for someone else?                              Answer True if yes,                             False if not or unknown.
	"delivery_days": string  // How many days                                      did it take for the product                                      to arrive? If this                                       information is not found,                                      output -1.
	"price_value": string  // Extract any                                    sentences about the value or                                     price, and output them as a                                     comma separated Python list.
}
```

```python
review_template_2 = """\

For the following text, extract the following information:

​

gift: Was the item purchased as a gift for someone else? \

Answer True if yes, False if not or unknown.

​

delivery_days: How many days did it take for the product\

to arrive? If this information is not found, output -1.

​

price_value: Extract any sentences about the value or price,\

and output them as a comma separated Python list.

​

text: {text}

​

{format_instructions}

"""
​

```python
prompt = ChatPromptTemplate.from_template(template=review_template_2)

​

messages = prompt.format_messages(text=customer_review, 

                                format_instructions=format_instructions)

print(messages[0].content)

For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the productto arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,and output them as a comma separated Python list.

text: This leaf blower is pretty amazing.  It has four settings:candle blower, gentle breeze, windy city, and tornado. It arrived in two days, just in time for my wife's anniversary present. I think my wife liked it so much she was speechless. So far I've been the only one using it, and I've been using it every other morning to clear the leaves on our lawn. It's slightly more expensive than the other leaf blowers out there, but I think it's worth it for the extra features.


The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":
```
```json
{
	"gift": string  // Was the item purchased                             as a gift for someone else?                              Answer True if yes,                             False if not or unknown.
	"delivery_days": string  // How many days                                      did it take for the product                                      to arrive? If this                                       information is not found,                                      output -1.
	"price_value": string  // Extract any                                    sentences about the value or                                     price, and output them as a                                     comma separated Python list.
}
```

response = chat(messages)

print(response.content)

```json
{
	"gift": false,
	"delivery_days": "2",
	"price_value": "It's slightly more expensive than the other leaf blowers out there, but I think it's worth it for the extra features."
}
```

```python
output_dict = output_parser.parse(response.content)

output_dict

{'gift': False,
 'delivery_days': '2',
 'price_value': "It's slightly more expensive than the other leaf blowers out there, but I think it's worth it for the extra features."}

type(output_dict)

dict

output_dict.get('delivery_days')

'2'
```

# Attachments:

![Alt text](<Screenshot 2023-08-18 at 6.41.41 PM.png>) 
![Alt text](<Screenshot 2023-08-18 at 6.43.50 PM.png>) 
![Alt text](<Screenshot 2023-08-18 at 7.51.00 AM.png>) 
![Alt text](<Screenshot 2023-08-18 at 7.52.08 AM.png>)
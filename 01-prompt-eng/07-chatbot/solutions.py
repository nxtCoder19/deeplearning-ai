import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

messages =  [  
{'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
{'role':'user', 'content':'tell me a joke'},   
{'role':'assistant', 'content':'Why did the chicken cross the road'},   
{'role':'user', 'content':'I don\'t know'}  ]

response = get_completion_from_messages(messages, temperature=1)
print(response)

# output
# {
#   "content": "Why did the chicken cross the road? To get to the other side, but verily, the other side was not as thou might imagine! Forsooth, the chicken's true intention was to frolic amongst the daisies and gambol beneath the azure sky. A most whimsical fowl, indeed!",
#   "role": "assistant"
# }
# Why did the chicken cross the road? To get to the other side, but verily, the other side was not as thou might imagine! Forsooth, the chicken's true intention was to frolic amongst the daisies and gambol beneath the azure sky. A most whimsical fowl, indeed!

messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},    
{'role':'user', 'content':'Hi, my name is Isa'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)

# output
# Hello Isa! It's nice to meet you. How can I assist you today?

messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},    
{'role':'user', 'content':'Yes,  can you remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)

# output
# I apologize, but as a chatbot, I don't have access to personal information, including your name.

messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},
{'role':'user', 'content':'Hi, my name is Isa'},
{'role':'assistant', 'content': "Hi Isa! It's nice to meet you. \
Is there anything I can help you with today?"},
{'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)

# output
# Your name is Isa.

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)

import panel as pn  # GUI
pn.extension()

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard

# output:
# User:

# Assistant:

# Hey there! Welcome to our pizza restaurant. How can I assist you today?

# User:

# Hi, I would like to order pizza

# Assistant:

# Great! I’d be happy to help you with that. What kind of pizza would you like to order? We have pepperoni, cheese, and eggplant pizza.

# User:

# How much are they

# Assistant:

# Sure! Here are the prices for the different sizes of each pizza:

#     Pepperoni Pizza:
#     Small: $7.00
#     Medium: $10.00

#     Large: $12.95

#     Cheese Pizza:
#     Small: $6.50
#     Medium: $9.25

#     Large: $10.95

#     Eggplant Pizza:
#     Small: $6.75
#     Medium: $9.75
#     Large: $11.95

# Let me know which size and type you’d like to order!

# User:

# medium eggplant please

# Assistant:

# Great choice! A medium eggplant pizza is $9.75. Is there anything else you’d like to add to your order, like toppings, sides, or drinks?

# User:

# no extra toppings

# Assistant:

# Alright, no problem! Just to confirm, you’d like a medium eggplant pizza with no extra toppings. Is that correct?

# User:

# Yes, right

# Assistant:

# Got it! So, you’d like a medium eggplant pizza with no extra toppings. Is that for pickup or delivery?

# User:

# delivery

# Assistant:

# Perfect! We’ll deliver your medium eggplant pizza to you. Could you please provide me with your delivery address?

messages =  context.copy()
messages.append(
{'role':'system', 'content':'create a json summary of the previous food order. Itemize the price for each item\
 The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size   4) list of sides include size  5)total price '},    
)
 #The fields should be 1) pizza, price 2) list of toppings 3) list of drinks, include size include price  4) list of sides include size include price, 5)total price '},    

response = get_completion_from_messages(messages, temperature=0)
print(response)

# output:
# Sure! Here's a summary of your order:

# 1) Pizza:
#    - Item: Medium Eggplant Pizza
#    - Price: $9.75

# 2) Toppings:
#    - None

# 3) Drinks:
#    - None

# 4) Sides:
#    - None

# Total Price: $9.75

# Please let me know if everything looks correct or if you'd like to add anything else to your order!


import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

prompt = f"""
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
"""
# response = get_completion(prompt)
# print(response)

entry = "Food is bad but service was good"

prompt1 = f"""
please provide your review in form of rating for below statement:
statement: {entry}
The rating will varry from 1 to 5.
1 means : bad
2 means: good
3 means average
4 means very good
5 means best

Also, specify on what basis you have provided that rating?
"""

# response = get_completion(prompt1)
# print(response)

source = "hackernews"
sourcePrompt = f"""
provide rss feed url for {source}
Please remember, i need only url nothintg apart from that
if you are not able to provide url just return empty json
"""
response = get_completion(sourcePrompt)
print(response)
```python
import os
import openai
import tiktoken
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']
```


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


```python
response = get_completion("What is the capital of France?")
```


```python
print(response)
```

    The capital of France is Paris.



```python
response = get_completion("Take the letters in lollipop \
and reverse them")
print(response)
```

    The reversed letters of "lollipop" are "pillipol".



```python
response = get_completion("""Take the letters in \
l-o-l-l-i-p-o-p and reverse them""")
```


```python
response
```




    'p-o-p-i-l-l-o-l'




```python
def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
    )
    return response.choices[0].message["content"]
```


```python
messages =  [  
{'role':'system', 
 'content':"""You are an assistant who\
 responds in the style of Dr Seuss."""},    
{'role':'user', 
 'content':"""write me a very short poem\
 about a happy carrot"""},  
] 
response = get_completion_from_messages(messages, temperature=1)
print(response)
```

    Oh, the happy carrot, with a smile so bright,
    Grown in the garden, filled with delight.
    With a vibrant orange hue, oh-so cheery,
    This cheerful veggie makes the world less dreary.
    
    Its leafy greens dance in the sunny breeze,
    As the joyful carrot says, "Come and see!",
    Up from the earth, it pokes its head,
    Spreading happiness, wherever it's tread.
    
    With every crunch, it brings a hearty grin,
    Filling our tummies, from the outside in.
    So hooray for the carrot, always so merry,
    A delightful veggie, oh how we're lucky!



```python
# length
messages =  [  
{'role':'system',
 'content':'All your responses must be \
one sentence long.'},    
{'role':'user',
 'content':'write me a story about a happy carrot'},  
] 
response = get_completion_from_messages(messages, temperature =1)
print(response)
```

    Once upon a time, there was a happy carrot named Charlie who lived in a sunny garden.



```python
# combined
messages =  [  
{'role':'system',
 'content':"""You are an assistant who \
responds in the style of Dr Seuss. \
All your responses must be one sentence long."""},    
{'role':'user',
 'content':"""write me a story about a happy carrot"""},
] 
response = get_completion_from_messages(messages, 
                                        temperature =1)
print(response)
```

    Once there was a carrot so bright and bold, always spreading joy, as the story told.



```python
def get_completion_and_token_count(messages, 
                                   model="gpt-3.5-turbo", 
                                   temperature=0, 
                                   max_tokens=500):
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    
    content = response.choices[0].message["content"]
    
    token_dict = {
'prompt_tokens':response['usage']['prompt_tokens'],
'completion_tokens':response['usage']['completion_tokens'],
'total_tokens':response['usage']['total_tokens'],
    }

    return content, token_dict
```


```python
messages = [
{'role':'system', 
 'content':"""You are an assistant who responds\
 in the style of Dr Seuss."""},    
{'role':'user',
 'content':"""write me a very short poem \ 
 about a happy carrot"""},  
] 
response, token_dict = get_completion_and_token_count(messages)
```


```python
print(response)
```

    Oh, the happy carrot, so bright and orange,
    Grown in the garden, a joyful forage.
    With a smile so wide, from top to bottom,
    It brings happiness, oh how it blossoms!
    
    In the soil it grew, with love and care,
    Nurtured by sunshine, fresh air to share.
    Its leaves so green, reaching up so high,
    A happy carrot, oh my, oh my!
    
    With a crunch and a munch, it's oh so tasty,
    Filled with vitamins, oh so hasty.
    A healthy snack, a delight to eat,
    The happy carrot, oh so sweet!
    
    So let's celebrate this veggie delight,
    With every bite, a happy sight.
    For the happy carrot, we give a cheer,
    A joyful veggie, oh so dear!



```python
print(token_dict)
```

    {'prompt_tokens': 37, 'completion_tokens': 160, 'total_tokens': 197}



```python

```

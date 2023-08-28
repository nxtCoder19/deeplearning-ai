import os
import openai
import sys
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import NotionDirectoryLoader


sys.path.append('../../')
# load document from your local

open_api_key = os.getenv('OPEN_API_KEY')
loader = PyPDFLoader("./basic-link-1.pdf")
pages = loader.load()
print(len(pages))

page = pages[0]
# print(page.page_content[:600])
print(page.metadata)

# save audio from youtube url

# url = "https://www.youtube.com/watch?v=coZoSYJU1OY"
# save_dir="youtube/"
# loader = GenericLoader(
#     YoutubeAudioLoader([url],save_dir),
#     OpenAIWhisperParser()
# )
# docs = loader.load()
# print(docs[0].page_content[0:500])

# web base url

# loader = WebBaseLoader("https://github.com/basecamp/handbook/blob/master/37signals-is-you.md")
# docs = loader.load()
# print(docs[0].page_content[:500])

# notion db

# loader = NotionDirectoryLoader("docs/Notion_DB")
# docs = loader.load()
# print(docs[0].page_content[0:200])
# docs[0].metadata


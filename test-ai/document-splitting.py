import os
import openai
import sys
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
sys.path.append('../..')
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings


openai.api_key  = os.environ['OPENAI_API_KEY']

chunk_size =20
chunk_overlap = 6

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
c_splitter = CharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
text1 = 'abcdefghijklmnopqrstuvwxyz'
print(r_splitter.split_text(text1))

# recursive splitting details

some_text = """When writing documents, writers will use document structure to group content. \
This can convey to the reader, which idea's are related. For example, closely related ideas \
are in sentances. Similar ideas are in paragraphs. Paragraphs form a document. \n\n  \
Paragraphs are often delimited with a carriage return or two carriage returns. \
Carriage returns are the "backslash n" you see embedded in this string. \
Sentences have a period at the end, but also, have a space.\
and words are separated by space."""

print(len(some_text))

c_splitter1 = CharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0,
    separator = ' '
)
r_splitter1 = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0, 
    separators=["\n\n", "\n", " ", ""]
)

# print(c_splitter1.split_text(some_text))
# print(r_splitter1.split_text(some_text))

loader = PyPDFLoader("./machine_learning_tutorial.pdf")
pages = loader.load()
# print(len(pages))

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)

docs = text_splitter.split_documents(pages)

print(len(docs))
print(len(pages))

# Vector store and embedding

# Load PDF
loaders = [
    # Duplicate documents on purpose - messy data
    PyPDFLoader("./machine_learning_tutorial.pdf"),
    PyPDFLoader("./machine_learning_tutorial.pdf"),
    PyPDFLoader("./machine_learning_tutorial.pdf"),
    PyPDFLoader("./machine_learning_tutorial.pdf"),
    PyPDFLoader("./machine_learning_tutorial.pdf"),
    PyPDFLoader("./machine_learning_tutorial.pdf"),
    PyPDFLoader("./machine_learning_tutorial.pdf"),
    
]
docs = []
for loader in loaders:
    docs.extend(loader.load())

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)

splits = text_splitter.split_documents(docs)
print("length",len(splits))

embedding = OpenAIEmbeddings()

persist_directory = 'docs/chroma/'
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

print(vectordb._collection.count())

question = "is there any email i can ask for help"
doc1 = vectordb.similarity_search(question,k=3)
print(len(doc1))
print(doc1[1].page_content)
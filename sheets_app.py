import os
import qdrant_client
import sentence_transformers
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Qdrant
from langchain import HuggingFaceHub
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
import streamlit as st
import pandas as pd

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

url="https://3d7bfaa8-bd3a-4fc2-a3d7-d258ffa31eda.us-east4-0.gcp.cloud.qdrant.io:6333"
api_key="fTx_XsidcbLSZHka9s2d28M2kq8v9AVoqwMo0EcPSiSzffViVFMtig"

embeddings = HuggingFaceEmbeddings()

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Replace the placeholders with your API credentials
creds = service_account.Credentials.from_service_account_file(
    'lyrical-country-416813-b9ad9b74b0f8.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

# Replace the placeholders with your spreadsheet ID and range
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

st.title('🦜🔗 Sheets App')
#https://docs.google.com/spreadsheets/d/1dh771MJAZ7Q1F4CZtmlIHrCQ2iYWwKi_OQC0MQZi6kY/edit?usp=sharing
sheet = st.text_input('Link to editable Google sheet')
sheet_csv = sheet[39:-17]

llm = HuggingFaceHub(repo_id="declare-lab/flan-alpaca-base",model_kwargs={"temperature": 0,"max_length": 512})

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_response(input_text):
    st.info(rag_chain.invoke(input_text))

if sheet!="":

  result = sheet.values().get(spreadsheetId=sheet_csv, range='Form Responses 1').execute()
  df = pd.DataFrame(result)
  df.to_csv('file1.csv')
  documents = CSVLoader('file1.csv').load()

  qdrant = Qdrant.from_documents(
    documents[0:100],
    embeddings,
    url=url,
    prefer_grpc=True,
    api_key=api_key,
    collection_name="my_documents",
    force_recreate=False,
  )

  retriever = qdrant.as_retriever()

  rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
  )

  with st.form('My Query'):
    text = st.text_area('Enter Question:')
    submitted = st.form_submit_button('Submit')
    generate_response(text)

else:
  st.caption("Please paste file link")

import streamlit as st
from langchain.din.text_splitter import RecursiveCharacterText
from langchain.embeddings import OllamaEmbeddiocument_loaders import PyPDFLoader
from langchan
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from pptx import Presentation
from langchain.schema import Document
import os
import tempfile


st.title("======================Private ChatBox ===================")

def load_pdf(file_path):
    return 

def load_pptx(file_path):
    return
def load_docx(file_path):
    return
def process_file(file_path):
    return
def load_pdf(path):
    return
def load_docx(path):
    return


uploaded_files = st.file_uploader("Upload PDF's,PPTX or DOCX files",type = ["pdf","pptx","docx"],accept_multiple_files = True)
if uploaded_files:
    all_docs = []

    with st.spinner("Reading and Exploring Files "):
        for file in uploaded_files:
            ext = file.name.split('.')[-1].lower()
            with tempfile.NamedTemporaryFile(delete = False,suffix = '.'+ext )as tmp_file:
                 tmp_file.write(file.getvalue())
                 tmp_path = tmp_file.name

            if ext == 'pdf':
                 all_docs.extend(load_pdf(tmp_path))
            elif ext == 'docx':
                all_docs.extend(load_pptx(tmp_path))
            elif ext == 'pptx':
                all_docs.extend(load_pptx(tmp_path))
            else:
                st.warning(f'Unstoppable file type : {ext}') 
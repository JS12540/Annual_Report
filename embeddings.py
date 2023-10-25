from chromadb.utils import embedding_functions
import requests
#from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel
import torch
from chromadb.utils import embedding_functions
import chromadb

from chunking import create_pdf_text_chunks

huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="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",
    model_name="BAAI/bge-small-en-v1.5"
)

client = chromadb.Client()
collection = client.get_or_create_collection(name="collection", embedding_function=huggingface_ef)


def create_chunks(text:str):
    try:
        chunks =  create_pdf_text_chunks(text)
        id_list = []


        for i in range(1, len(chunks)+1):  # Range from 1 to 153
            id_list.append(f"id{i}")

        collection.add(
            documents=chunks,
            ids=id_list,
                    )
        return True
        
    except Exception as e:
        return False

 
def result(query, n_result = 4):
    return collection.query(
    query_texts=query,
    n_results=n_result)
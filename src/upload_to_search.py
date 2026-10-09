import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from ingestion.load_pandas import load_documents

load_dotenv()

documents = load_documents()

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_API_KEY")

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name="pyml-rag-index",
    credential=AzureKeyCredential(search_key)
)

search_documents = []

for i, (document, embedding) in enumerate(zip(documents, embeddings)):
    search_doc = {
        "id": str(i)
    }
    
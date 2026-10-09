import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from ingestion.load_pandas import load_documents
from test_azure_embeddings import generate_embeddings
from search_document import SearchDocument

load_dotenv()

documents = load_documents()

embeddings = generate_embeddings(documents)

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_API_KEY")

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name="pyml-rag-index",
    credential=AzureKeyCredential(search_key)
)

search_documents = []

for i, (document, embedding) in enumerate(zip(documents, embeddings)):
    search_doc = SearchDocument(
        id=str(i),
        content=document.page_content,
        source=document.metadata["source"],
        url=document.metadata["url"],
        content_vector=embedding
    )

    search_documents.append(search_doc.model_dump(mode="json"))

results = search_client.upload_documents(documents=search_documents)

for result in results:
    print(result.succeeded)
    
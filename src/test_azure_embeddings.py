import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from ingestion.load_pandas import load_documents

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-10-21"
)

def generate_embeddings(documents):
    response = client.embeddings.create(
        model=deployment_name,
        input=[document.page_content for document in documents]
    )
    embeddings = [vector_data.embedding for vector_data in response.data]
    return embeddings

if __name__ == "__main__":
    documents = load_documents()
    embeddings = generate_embeddings(documents)

    print(f"Liczba dokumentów: {len(documents)}")
    print(f"Liczba embeddingów: {len(embeddings)}")
    print(f"Długość pierwszego embeddinga: {len(embeddings[0])}")

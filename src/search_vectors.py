import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery

load_dotenv()

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_API_KEY")

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name="pyml-rag-index",
    credential=AzureKeyCredential(search_key)
)

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-10-21"
)

question = "Jak uzupełnić brakujące wartości w Pandas?"

response = client.embeddings.create(
    model=deployment_name,
    input=question
)

question_vector = response.data[0].embedding

vector_query = VectorizedQuery(
    vector=question_vector,
    k_nearest_neighbors=10,
    fields="content_vector"
)

results = list(search_client.search(
    search_text=question,
    vector_queries=[vector_query],
    top=10,
    query_type="semantic",
    semantic_configuration_name="semantic-config"
)
)

for result in results:
    print(f"Content: {result['content']}")
    print(f"Search score: {result['@search.score']}")
    print(f"Reranker score: {result.get('@search.reranker_score')}")

context = "\n\n".join(
    result["content"] for result in results[:3]
)

print(context)
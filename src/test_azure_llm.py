import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-10-21"
)

response = client.chat.completions.create(
    model=deployment_name, 
    messages=[
        {
            "role": "user", 
            "content": "Czym jest RAG? Odpowiedz jednym zdaniem."
        }
    ]
)

print(response.choices[0].message.content)
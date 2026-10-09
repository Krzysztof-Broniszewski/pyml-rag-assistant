import requests
import trafilatura
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer

url = "https://pandas.pydata.org/docs/user_guide/missing_data.html"

def load_documents():
    response = requests.get(url)
    print(response.status_code)

    text = trafilatura.extract(
        response.text,
        output_format="markdown"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)
    documents = [
        Document(
            page_content=chunk,
            metadata={"source": "pandas", "url": url}
        )
        for chunk in chunks
    ]
    return documents

def split_by_headers(content, header_level):
    header = "#" * header_level + " "
    actual_title = None
    actual_content = []
    sections = []
    for line in content.splitlines():
        if line.startswith(header):
            if actual_title is not None:
                sections.append({"title": actual_title, "content": "\n".join(actual_content)})

            actual_title = line
            actual_content = []

        else:
            actual_content.append(line)

    if actual_title is not None:
        sections.append({"title": actual_title, "content": "\n".join(actual_content)})

    return sections

# actual_title = None
# actual_content = []
# sections = []

# split_text = text.splitlines()
# for line in split_text:
#     if line.startswith("## "):
#         if actual_title is not None:
#             sections.append({"title": actual_title, "content": "\n".join(actual_content)})

#         actual_title = line
#         actual_content = []

#     else:
#         actual_content.append(line)

# if actual_title is not None:
#     sections.append({"title": actual_title, "content": "\n".join(actual_content)})
    
# sections = split_by_headers(text, 2)

if __name__ == "__main__":
    documents = load_documents()
    print(f"Liczba dokumentów: {len(documents)}")


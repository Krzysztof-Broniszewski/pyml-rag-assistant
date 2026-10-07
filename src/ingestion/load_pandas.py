import requests
import trafilatura

url = "https://pandas.pydata.org/docs/user_guide/missing_data.html"

response = requests.get(url)
print(response.status_code)

text = trafilatura.extract(
    response.text,
    output_format="markdown"
)

actual_title = None
actual_content = []
sections = []

split_text = text.splitlines()
for line in split_text:
    if line.startswith("## "):
        if actual_title is not None:
            sections.append({"title": actual_title, "content": actual_content})

        actual_title = line
        actual_content = []

    else:
        actual_content.append(line)
    
for section in sections:
    print(section)



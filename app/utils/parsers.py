import json
from bs4 import BeautifulSoup

def parse_text(file_content: bytes) -> str:
    return file_content.decode("utf-8")

def parse_markdown(file_content: bytes) -> str:
    return file_content.decode("utf-8")

def parse_json(file_content: bytes) -> str:
    data = json.loads(file_content.decode("utf-8"))
    return json.dumps(data, indent=2)

def parse_html(file_content: bytes) -> str:
    soup = BeautifulSoup(file_content, "html.parser")
    return soup.get_text(separator="\n")

def parse_file(filename: str, content: bytes) -> str:
    if filename.endswith(".txt"):
        return parse_text(content)
    elif filename.endswith(".md"):
        return parse_markdown(content)
    elif filename.endswith(".json"):
        return parse_json(content)
    elif filename.endswith(".html"):
        return parse_html(content)
    else:
        return content.decode("utf-8", errors="ignore")

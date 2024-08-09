import requests
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
import re
import psutil
import threading
import time

# Get the list of all pages to parse
import requests
import re

def get_all_pages():
    url = "https://wiki.archlinux.org/api.php"
    params = {
        "action": "query",
        "list": "allpages",
        "aplimit": "max",
        "format": "json"
    }
    pages = []
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        for page in data['query']['allpages']:
            title = page['title']
            # Filter out non-English pages
            if not re.search(r'\(.*\)$', title) and re.match(r'^[A-Za-z0-9\s\-_]+$', title):
                pages.append(title)
        if 'continue' in data:
            params.update(data['continue'])
        else:
            break
    return pages


# Parse the content of each page
def create_index(es, index_name):
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "standard"
                    },
                    "custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "section_title": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "content": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "timestamp": {
                    "type": "date"
                }
            }
        }
    }

    es.indices.delete(index=index_name, body=settings)
    es.indices.create(index=index_name, body=settings)


def get_page_content(title):
    url = "https://wiki.archlinux.org/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "revisions",
        "rvprop": "content",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    content = page['revisions'][0]['*'] if 'revisions' in page else None
    return content

def clean_section_title(title):
    # Remove leading and trailing equal signs and whitespace
    return re.sub(r'^[=]+\s*(.*?)\s*[=]+$', r'\1', title.strip())

def split_content_into_chunks(content):
    chunks = []
    sections = re.split(r'(==+ .+ ==+)', content)  # Split by headings
    for i in range(1, len(sections), 2):
        section_title = clean_section_title(sections[i])
        section_content = sections[i + 1].strip()
        chunks.append({
            "section_title": section_title,
            "section_content": section_content
        })
    return chunks


def index_document(es, index, id, body):
    es.index(index=index, id=id, body=body)


def monitor_resources():
    process = psutil.Process()
    while True:
        cpu_usage = process.cpu_percent(interval=1)
        memory_usage = process.memory_info().rss / (1024 * 1024)
        print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage} MB")
        time.sleep(5)


def main():
    monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
    monitor_thread.start()

    es = Elasticsearch('http://localhost:9200')
    index_name = "archwiki"

    # Create the index with settings and mappings
    create_index(es, index_name)

    all_pages = get_all_pages()  # Function to retrieve all English page titles
    print(f"Total pages: {len(all_pages)}")

    for page_title in tqdm(all_pages):
        content = get_page_content(page_title)  # Function to fetch page content
        if content:
            chunks = split_content_into_chunks(content)

            # Skip indexing empty pages (redirects)
            if len(chunks) == 0:
                print("Skipping an empty page")
                continue
            for i, chunk in enumerate(chunks):
                document = {
                    "title": page_title,
                    "section_title": chunk["section_title"],
                    "content": chunk["section_content"],
                    "timestamp": "2024-07-29T12:00:00Z"  # Example timestamp
                }
                doc_id = f"{page_title.replace(' ', '_').lower()}_{i}"
                index_document(es, index_name, doc_id, document)
            print(f"Indexed page: {page_title} with {len(chunks)} chunks")
        else:
            print(f"Page not found: {page_title}")


if __name__ == "__main__":
    main()
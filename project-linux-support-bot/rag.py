# This class implement RAG using the index from indexer and various LLMs
import time
import os

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

# Load variables
load_dotenv()

ollama_client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key="ollama",
)
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI()
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")


# Define the search function
def elastic_search(field, vector, course, index_name = "archwiki"):
    knn = {
        "field": field,
        "query_vector": vector,
        "k": 5,
        "num_candidates": 10000,
        "filter": {"term": {"course": course}},
    }

    search_query = {
        "knn": knn,
        "_source": ["text", "section", "question", "course", "id"],
    }

    es = Elasticsearch('http://localhost:9200')
    es_results = es.search(index=index_name, body=search_query)

    return [hit["_source"] for hit in es_results["hits"]["hits"]]


# Define the prompt to send to LLM
def build_prompt(query, search_results):
    prompt_template = """
        You're a support engineer that helps users work and troubleshoot their Arch Linux distributions. 
        Answer the QUESTION based on the CONTEXT from the Arch wiki database.
        Use only the facts from the CONTEXT when answering the QUESTION.

        QUESTION: {question}

        CONTEXT: 
        {context}
        """.strip()

    context = "\n\n".join(
        [
            f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}"
            for doc in search_results
        ]
    )
    return prompt_template.format(question=query, context=context).strip()


# Define a function to talk to LLM
def llm(prompt, used_model = 'gemma2:2b'):
    # Log the start time
    start_time = time.time()

    # Logic to choose the model
    if used_model == 'gemma2:2b' or used_model == 'qwen2:1.5b' or used_model == 'phi3':
        response = ollama_client.chat.completions.create(
            model=used_model,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
    elif used_model == 'gpt-4o-mini':
        response = openai_client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
    else:
        raise ValueError(f"Unknown model choice: {used_model}")

    # Log the end time and calculate how much it took to provide an answer
    end_time = time.time()
    response_time = end_time - start_time
    return answer


# Put everything together
def rag(query, used_model='gemma2:2b'):
    vector = model.encode(query)
    search_results = elastic_search('question_text_vector', vector, "course")
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, used_model)
    return answer


def main():
    query = "How do I install asusctl on Arch?"
    print(rag(query, 'phi3'))


if __name__ == "__main__":
    main()

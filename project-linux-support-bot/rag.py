# This class implement RAG using the index from indexer and various LLMs
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

class rag:
    # Load variables
    load_dotenv()

    ollama_client = OpenAI(base_url=os.getenv('OLLAMA_URL'), api_key="ollama")
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Define the search function
    def elastic_search(self, query):
        return

    # Define the prompt to send to LLM
    def build_prompt(self, query, search_results):
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
    def llm(self, prompt, used_model='llama3.1'):
        # Log the start time
        start_time = time.time()

        # Logic to choose the model
        if used_model == 'llama3.1' or used_model == 'qwen2' or used_model == 'zephyr':
            response = self.ollama_client.chat.completions.create(
                model = used_model,
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
        elif used_model == 'gpt-4o-mini':
            response = self.openai_client.chat.completions.create(
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
    def rag(self, query):
        search_results = self.elastic_search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm(prompt)
        return answer
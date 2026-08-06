# All required Imports
import os
from dotenv import load_dotenv
from google import genai

from utils.load_documents import load_documents
from utils.chunker import chunk_text
from utils.embeddings import create_embedding
from vector_store.vector_store import create_vector_store
from utils.retriever import retrieve_chunks
from utils.prompt_builder import build_prompt


def initialize_rag():
    """
    Loads documents, creates embeddings,
    builds the vector store, and initializes Gemini.
    """

    # Load environment variables
    load_dotenv()

    # Read API Key
    api_key = os.getenv("GEMINI_API_KEY")

    # Create Gemini Client
    client = genai.Client(api_key=api_key)

    # Load Documents
    documents = load_documents()

    # Create Chunks + Embeddings
    all_chunks = []

    for doc in documents:

        chunks = chunk_text(doc["content"])

        for chunk in chunks:

            embedding = create_embedding(chunk)

            all_chunks.append(
                {
                    "filename": doc["filename"],
                    "chunk": chunk,
                    "embedding": embedding,
                }
            )

    # Create Vector Store
    index, metadata = create_vector_store(all_chunks)

    print("✅ Vector Store Created Successfully!")

    return client, index, metadata


def ask_question(question, client, index, metadata):
    """
    Takes a user question and returns an answer.
    """

    retrieved_chunks = retrieve_chunks(
        question,
        index,
        metadata,
    )

    prompt = build_prompt(
        question,
        retrieved_chunks,
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


def main():

    client, index, metadata = initialize_rag()

    while True:

        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = ask_question(
            question,
            client,
            index,
            metadata,
        )

        print("\nAnswer")
        print("-" * 50)
        print(answer)


if __name__ == "__main__":
    main()
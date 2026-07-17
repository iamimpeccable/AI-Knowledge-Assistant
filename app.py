#All required Imports
import os
from dotenv import load_dotenv
from google import genai
from utils.load_documents import load_documents
from utils.chunker import chunk_text
from utils.embeddings import create_embedding
from vector_store.vector_store import create_vector_store
from utils.retriever import retrieve_chunks
from utils.prompt_builder import build_prompt


# Load environment variables
load_dotenv()

#Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send a prompt
#response = client.models.generate_content(
#    model="gemini-2.5-flash",
#    contents="Say hello! Tell me you're ready to build an AI Knowledge Assistant."
#)

#print(response.text)

# -------------------------
# Load Documents
# -------------------------
documents = load_documents()


# -------------------------
# Create Chunks + Embeddings
# -------------------------
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

# -------------------------
# Create FAISS Index
# -------------------------

index, metadata = create_vector_store(all_chunks)
print("\n✅ Vector Store Created Successfully!")

while True:
    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    retrieved_chunks = retrieve_chunks(
        question,
        index,
        metadata
    )

   # for chunk in retrieved_chunks:
    #    print(f"\n {chunk['filename']}")
    #    print(chunk["chunk"])

    prompt = build_prompt(
    question,
    retrieved_chunks
    )

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    print("\nAnswer")
    print("-" * 50)
    print(response.text)


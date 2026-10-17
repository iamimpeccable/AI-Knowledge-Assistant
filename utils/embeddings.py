import os
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer
load_dotenv()


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def create_embeddings(texts, batch_size=32):
    if not texts:
        return []

    vectors = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=len(texts) > 32,
    )
    return vectors.tolist()


def create_embedding(text):
    return create_embeddings([text])[0]
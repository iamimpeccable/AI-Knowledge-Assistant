def build_prompt(question, retrieved_chunks):

    context = ""

    for chunk in retrieved_chunks:
        context += chunk["chunk"] + "\n\n"

    prompt = f"""
You are an AI Knowledge Assistant.

Use ONLY the information provided in the context below.

If the answer is not present in the context, say:
"I couldn't find relevant information in your knowledge base."

Context:
-----------------------
{context}

-----------------------

Question:
{question}

Answer:
"""

    return prompt
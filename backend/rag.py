import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# ===== CONFIG =====
import os

load_dotenv()  
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "mdd_collection"
TRANSCRIPT_FILE = "mdd_transcript.txt"
SIMILARITY_THRESHOLD = 0.5  # cosine similarity threshold

groq_client = Groq(api_key=GROQ_API_KEY)

# ===== INIT =====
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

model = SentenceTransformer("all-MiniLM-L6-v2")


# ===== CHUNKING =====
def chunk_text(text, max_sentences=5):
    sentences = text.split(". ")
    chunks = []
    current_chunk = []

    for sentence in sentences:
        current_chunk.append(sentence.strip())

        if len(current_chunk) >= max_sentences:
            chunks.append(". ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(". ".join(current_chunk))

    return chunks


# ===== BUILD COLLECTION =====
def build_collection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    transcript_path = os.path.join(base_dir, TRANSCRIPT_FILE)

    if not os.path.exists(transcript_path):
        raise FileNotFoundError("Transcript file not found.")

    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        raise ValueError("Transcript file is empty.")

    chunks = chunk_text(text)
    print("Number of chunks:", len(chunks))

    embeddings = model.encode(chunks)
    vector_size = len(embeddings[0])

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embeddings[i].tolist(),
            payload={"text": chunks[i]},
        )
        for i in range(len(chunks))
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print("Collection built and data uploaded successfully.")


# ===== RETRIEVAL =====
def retrieve(query):
    query_embedding = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=3,
    ).points

    if not results:
        return None

    context = " ".join([r.payload["text"] for r in results])
    return context
    


def generate_answer(context, question):
        if context is None:
            return "Data not found"

        prompt = f"""
        You are a medical assistant chatbot.

        Use ONLY the provided context.
        Do NOT use prior knowledge.
        If the answer is not explicitly present in the context, respond exactly with:
        Data not found.

        Context:
        {context}

        Question:
        {question}

        Provide a clear and structured answer.
        """

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content















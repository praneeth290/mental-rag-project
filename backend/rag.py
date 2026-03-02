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

model = SentenceTransformer("all-mpnet-base-v2")  # Better for medical content


# ===== CHUNKING =====
def chunk_text(text, max_sentences=7):
    """Improved chunking with better semantic boundaries"""
    sentences = text.split(". ")
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        current_chunk.append(sentence)
        current_length += len(sentence.split())

        # Chunk based on both sentence count and word count for better context
        if len(current_chunk) >= max_sentences or current_length > 150:
            chunks.append(". ".join(current_chunk) + ".")
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(". ".join(current_chunk) + ".")

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
        limit=5,  # Retrieve more results for better context
        score_threshold=SIMILARITY_THRESHOLD,  # Filter by relevance
    ).points

    if not results:
        return None

    # Sort by score and combine best matches
    sorted_results = sorted(results, key=lambda x: x.score, reverse=True)
    context = " ".join([r.payload["text"] for r in sorted_results])
    return context
    


def generate_answer(context, question):
        if context is None:
            return "I don't have information about that in our database. Please consult a mental health professional."

        prompt = f"""You are an expert medical assistant specializing in Major Depressive Disorder (MDD) and mental health.

Your task is to answer questions accurately using ONLY the provided context.

CRITICAL RULES:
1. Use ONLY the provided context - do NOT use prior knowledge
2. If the answer is not in the context, respond: "This information is not available in our database. Please consult with a healthcare professional."
3. Be accurate, clear, and structured
4. For medical symptoms or treatments, provide specific details from the context
5. If asking for medical advice, remind users to consult professionals

Context Information:
{context}

User Question:
{question}

Provide a clear, well-structured answer based ONLY on the context above."""

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Slightly higher for more natural responses
            max_tokens=500,
        )

        return response.choices[0].message.content















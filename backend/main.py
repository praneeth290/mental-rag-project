from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag import retrieve, generate_answer

app = FastAPI()

# Enable CORS (important for React frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QueryRequest):
    question = request.question.strip()

    context = retrieve(question)

    if context is None:
        return {"answer": "Data not found"}

    answer = generate_answer(context, question)

    return {"answer": answer}
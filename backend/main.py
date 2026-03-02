from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag import retrieve, generate_answer
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()
frontend_url = os.getenv("FRONTEND_URL")
# Enable CORS for all origins (or restrict if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        question = request.question.strip()
        
        if not question:
            return {"answer": "Please provide a question"}

        context = retrieve(question)

        if context is None:
            return {"answer": "I don't have information about that. Please consult a mental health professional."}

        answer = generate_answer(context, question)

        return {"answer": answer}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"answer": f"An error occurred: {str(e)}"}
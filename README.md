git clone <https://github.com/praneeth290/mental-rag-project>
cd mental-rag-project

>>Go to Backend Folder
cd backend

>>Create Virtual Environment
python -m venv venv

>>Activate Virtual Environment
venv\Scripts\activate

>>Install Dependencies
pip install -r requirements.txt

>>Add Environment Variables
Create a .env file inside the backend/ folder and add:
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
GROQ_API_KEY=your_groq_api_key

>>Inside backend/, create a file:
build_index.py in that add:
from rag import build_collection
if __name__ == "__main__":
    build_collection()

>>Run Backend Server
uvicorn main:app --reload
Backend will run at:
http://127.0.0.1:8000
Swagger API documentation:
http://127.0.0.1:8000/docs


>>Open a NEW terminal window.
Go to Frontend Folder
cd frontend
Install Node Dependencies:
npm install


>>Start React Application
npm start
Frontend runs at:
http://localhost:3000

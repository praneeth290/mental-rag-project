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




To run this project locally, first clone the repository and navigate into the project folder. Then go to the backend directory and create a virtual environment using python -m venv venv, and activate it (on Windows use venv\Scripts\activate, on Mac/Linux use source venv/bin/activate). After activating the environment, install all required dependencies using pip install -r requirements.txt. Next, configure the required environment variables by creating a .env file inside the backend folder (or by setting system environment variables) and add your QDRANT_URL, QDRANT_API_KEY, and GROQ_API_KEY. Once the environment is configured, you must build the vector database collection by running python build_index.py. This step reads the transcript data, generates embeddings, and uploads them to Qdrant; it only needs to be done once during initial setup or whenever new transcript data is added. After the collection is successfully created, start the backend server using uvicorn main:app --reload. The backend will run at http://127.0.0.1:8000, and you can verify the API using http://127.0.0.1:8000/docs. To run the frontend, open a new terminal window, navigate to the frontend folder, install dependencies using npm install, and then start the React application using npm start. The frontend will run at http://localhost:3000 and will communicate with the FastAPI backend. Both backend and frontend must be running simultaneously for the chatbot to function properly. If new video transcripts are added in the future, run python build_index.py again to rebuild the vector database before restarting the backend server.

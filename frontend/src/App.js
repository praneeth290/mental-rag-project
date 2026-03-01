import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        question: question,
      });

      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer("Error connecting to server.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>MDD RAG Chatbot</h1>

      <textarea
        placeholder="Ask about Major Depressive Disorder..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={handleAsk} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div className="answer">
          <h3>Answer:</h3>
          <ReactMarkdown>{answer}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;



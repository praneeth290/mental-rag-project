import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import ReactMarkdown from "react-markdown";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const SUGGESTIONS = [
  "What are the symptoms of MDD?",
  "How is MDD diagnosed?",
  "What treatments are available?",
  "MDD vs Bipolar disorder",
];

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [isError, setIsError] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleAsk = async (q) => {
    const query = q || question;
    if (!query.trim()) return;

    if (q) setQuestion(q);
    setLoading(true);
    setAnswer("");
    setIsError(false);

    try {
      const response = await axios.post(`${BACKEND_URL}/ask`, {
        question: query,
      });
      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer("Unable to connect to the server. Please ensure the backend is running.");
      setIsError(true);
    }

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      handleAsk();
    }
  };

  return (
    <div className="app-wrapper">
      {/* Header */}
      <header className="app-header">
        <div className="badge">
          <span className="badge-dot" />
          RAG-Powered · Clinical Knowledge Base
        </div>
        <h1>MDD <em>Research</em> Assistant</h1>
        <p>Ask clinical questions about Major Depressive Disorder — powered by retrieval-augmented generation.</p>
      </header>

      {/* Main card */}
      <div className="chat-card">

        {/* Suggestion chips */}
        <div className="suggestions">
          <span className="suggestions-label">Suggested questions</span>
          {SUGGESTIONS.map((s) => (
            <button key={s} className="chip" onClick={() => handleAsk(s)}>
              {s}
            </button>
          ))}
        </div>

        {/* Input */}
        <div className="input-section" style={{ marginTop: 20 }}>
          <span className="input-label">Your question</span>
          <div className="textarea-wrapper">
            <textarea
              placeholder="e.g. What are the first-line pharmacological treatments for MDD?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>
        </div>

        {/* Toolbar */}
        <div className="toolbar">
          <span className="char-count">
            {question.length > 0 ? `${question.length} chars · Ctrl+Enter to send` : "Ctrl+Enter to send"}
          </span>
          <button className="ask-btn" onClick={() => handleAsk()} disabled={loading || !question.trim()}>
            {loading ? (
              <>
                <span className="spinner" />
                Analyzing...
              </>
            ) : (
              <>
                <svg className="btn-icon" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M2 8h12M9 3l5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Ask
              </>
            )}
          </button>
        </div>

        {/* Answer */}
        {(answer || loading) && (
          <>
            <div className="section-divider" />
            {isError ? (
              <div className="error-msg">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M8 5v4M8 11v.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                {answer}
              </div>
            ) : (
              <div className="answer-section">
                <div className="answer-header">
                  <div className="answer-avatar">🧠</div>
                  <div className="answer-meta">
                    <span className="answer-name">MDD Assistant</span>
                    <span className="answer-tag">RAG · Evidence-based response</span>
                  </div>
                </div>
                <div className="answer-body">
                  {loading ? (
                    <p style={{ color: "var(--text-muted)", fontStyle: "italic" }}>Retrieving relevant documents and generating response…</p>
                  ) : (
                    <ReactMarkdown>{answer}</ReactMarkdown>
                  )}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Disclaimer */}
      <p className="disclaimer">
        <strong>For research & educational use only.</strong> This tool does not provide medical advice. Always consult a qualified healthcare professional for clinical decisions.
      </p>
    </div>
  );
}

export default App;
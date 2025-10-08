import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { HistoryPanel } from './HistoryPanel';

const API_URL = '/api';

function saveHistoryFile(history, format = "md") {
  let content = "";
  if(format === "md") {
    content = history.map(msg => 
      `${msg.isUser ? "**You:**" : "**AI:**"} ${msg.text.replace(/\n/g, "  \n")}`
    ).join('\n\n');
  } else {
    content = history.map(msg => 
      `${msg.isUser ? "You:" : "AI:"} ${msg.text.replace(/\n/g, "\n   ")}`
    ).join('\n\n');
  }
  const blob = new Blob([content], {type: 'text/plain'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.download = `chat_history.${format}`;
  a.href = url;
  a.click();
  URL.revokeObjectURL(url);
}

function App() {
  // const [messages, setMessages] = useState([
  //   { text: "Hello! I'm your AI assistant. How can I help you today?", isUser: false }
  // ]);
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("chat_history");
    return saved ? JSON.parse(saved) : [
      { text: "Hello! I'm your AI assistant.", isUser: false, timestamp: new Date().toISOString() }
    ];
  });
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const conversationHistory = useRef([]);
  const [showHistory, setShowHistory] = useState(false);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    localStorage.setItem("chat_history", JSON.stringify(messages));
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkBackendHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/chat/health`);
      const data = await response.json();
      console.log(data);
      setIsConnected(data.status === 'healthy' && data.model_loaded);
    } catch (err) {
      console.error('Backend health check failed:', err);
      setIsConnected(false);
      showError('Unable to connect to backend. Please ensure the server is running.');
    }
  };

  const showError = (message) => {
    setError(message);
    setTimeout(() => setError(null), 3000);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    const message = inputMessage.trim();
    if (!message || isLoading) return;

    // Add user message to chat
    const userMessage = { text: message, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          history: conversationHistory.current
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response
      const botMessage = { text: data.response, isUser: false };
      setMessages(prev => [...prev, botMessage]);

      // Update conversation history
      conversationHistory.current = [
        ...conversationHistory.current,
        { role: 'user', content: message },
        { role: 'assistant', content: data.response }
      ];

    } catch (err) {
      console.error('Error sending message:', err);
      showError('Sorry, I encountered an error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🤖 AI Chat Assistant</h1>
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '● Connected' : '○ Disconnected'}
          </div>
        </div>

        <button 
          className="toggle-history-btn" 
          onClick={() => setShowHistory(!showHistory)}>
          {showHistory ? "Hide Timeline" : "Show Timeline"}
        </button>

        <button onClick={() => {
          setMessages([]);
          conversationHistory.current = [];
          localStorage.removeItem("chat_history");
          }} >Clear History
        </button>

        {/* Render HistoryPanel */}
        <HistoryPanel
          history={messages}
          show={showHistory}
          onClose={() => setShowHistory(false)}
          onSave={() => saveHistoryFile(messages, "md")} // or "txt"
        />

        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`message ${msg.isUser ? 'user' : 'bot'}`}
            >
              <div className="message-content">
                {msg.text}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form className="chat-input-container" onSubmit={handleSendMessage}>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading || !isConnected}
            className="message-input"
            autoComplete="off"
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputMessage.trim() || !isConnected}
            className="send-button"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;

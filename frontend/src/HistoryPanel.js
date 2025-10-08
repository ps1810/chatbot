// src/HistoryPanel.js
import React from 'react';

export function HistoryPanel({ history, show, onClose, onSave }) {
  if (!show) return null;
  return (
    <div className="history-panel">
      <div className="history-header">
        <span>Conversation History</span>
        <button onClick={onClose}>Close</button>
        <button onClick={onSave}>Save Chat</button>
      </div>
      <div className="history-body">
        {history.map((msg, idx) => (
          <div key={idx} className={`history-msg ${msg.isUser ? 'user' : 'bot'}`}>
            <span className="history-role">{msg.isUser ? "You:" : "AI:"}</span>
            <span className="history-text">{msg.text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

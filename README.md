# ChatBot

A full-stack AI chatbot application built with FastAPI backend and React frontend, featuring real-time conversation with a local language model.

## 🌟 Features

- **Real-time AI Chat**: Interactive conversations with SmolLM2-1.7B-Instruct model
- **Conversation History**: Track and review your chat timeline
- **Export Chat**: Save conversations in Markdown or Text format
- **Docker Support**: Easy deployment with Docker Compose
- **Memory Management**: Automatic cleanup and optimization for resource efficiency
- **Health Monitoring**: Backend health checks and connection status indicators

## 🏗️ Architecture

### Backend (FastAPI + PyTorch)
- **Framework**: FastAPI with async support
- **Model**: HuggingFace Transformers (SmolLM2-1.7B-Instruct)
- **Memory Optimization**: Periodic cleanup and garbage collection
- **API**: RESTful endpoints for chat and health checks

### Frontend (React)
- **Framework**: React 19.2.0
- **Styling**: Custom CSS with gradient themes
- **State Management**: React Hooks (useState, useEffect, useRef)
- **Storage**: LocalStorage for chat persistence
- **Proxy**: Nginx for API routing in production

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended)
- OR:
  - Python 3.13+
  - Node.js 18+
  - Poetry (Python package manager)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/ps1810/chatbot
cd chatbot
```

2. **Start the application**
```bash
docker compose up --build
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Health Check: http://localhost:8000/chat/health

### Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Install dependencies with Poetry**
```bash
poetry install
```

3. **Run the backend server**
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm start
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    model_name: str = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    max_memory_mps: str = "4GB"
    max_memory_cpu: str = "8GB"
    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    max_history: int = 3
    cors_origins: List[str] = ["http://localhost:3000"]
    cleanup_interval_seconds: int = 60
```

### Environment Variables

Create `.env` files in backend and frontend directories:

**Backend `.env`:**
```env
MODEL_NAME=HuggingFaceTB/SmolLM2-1.7B-Instruct
MAX_MEMORY_MPS=4GB
MAX_MEMORY_CPU=8GB
```

## 📁 Project Structure

```
brainbay-chatbot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── chat.py          # Chat endpoint
│   │   ├── core/
│   │   │   ├── config.py            # Configuration
│   │   │   ├── lifecycle.py         # App lifecycle
│   │   │   ├── logger.py            # Logging setup
│   │   │   ├── model_context.py     # Model management
│   │   │   └── periodic_cleanup.py  # Memory cleanup
│   │   ├── dependencies/
│   │   │   └── providers.py         # Dependency injection
│   │   ├── domain/
│   │   │   └── chat.py              # Domain models
│   │   ├── infrastructure/
│   │   │   └── model_loader.py      # Model loading
│   │   ├── middleware/
│   │   │   └── timeout.py           # Request timeout
│   │   ├── schemas/
│   │   │   └── chat.py              # Pydantic schemas
│   │   ├── services/
│   │   │   └── chat_service.py      # Chat logic
│   │   └── main.py                  # FastAPI app
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js                   # Main component
│   │   ├── App.css                  # Styles
│   │   ├── HistoryPanel.js          # History sidebar
│   │   └── index.js                 # Entry point
│   ├── nginx.conf
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## 🔌 API Endpoints

### Chat Endpoint
```http
POST /chat/
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

Response:
```json
{
  "response": "I'm doing well, thank you for asking!"
}
```

### Health Check
```http
GET /chat/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 🎨 Features in Detail

### Conversation History Panel
- View all past messages in a timeline format
- Distinguish between user and AI messages
- Export conversations as Markdown or Text files
- Toggle visibility with a single click

### Memory Management
- Automatic periodic cleanup every 60 seconds

### Error Handling
- Connection status indicators
- Graceful error messages
- Automatic retry mechanisms
- Timeout handling (60s default)

## 🐳 Docker Details

### Build Individual Services

**Backend:**
```bash
docker build -t brainbay-backend ./backend
```

**Frontend:**
```bash
docker build -t brainbay-frontend ./frontend
```

### Health Checks
Both services include health check configurations:
- Backend: Every 30s, checks `/chat/health`
- Frontend: Every 30s, checks nginx status

## 📊 Performance Considerations

- **Model Size**: SmolLM2-1.7B (~3.5GB)

## 🔒 Security

- CORS configuration for allowed origins
- Request timeout middleware
- Input validation with Pydantic
- Nginx security headers in production
- No sensitive data stored in localStorage
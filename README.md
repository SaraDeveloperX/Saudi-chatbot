# 🇸🇦 Saudipedia RAG Chatbot | مساعد سعوديبيديا الذكي

**An AI-powered RAG (Retrieval-Augmented Generation) chatbot for searching and answering questions about Saudi Arabia based on the Saudipedia dataset.**

مشروع مساعد ذكي يعتمد على تقنية RAG للإجابة على الأسئلة المتعلقة بالمملكة العربية السعودية باستخدام قاعدة بيانات سعوديبيديا.

---

## 🛠️ Tech Stack | التقنيات المستخدمة

- **Frontend**: Vue 3, TypeScript, TailwindCSS (Mobile-first design)
- **Backend**: FastAPI (Python)
- **Vector DB**: Weaviate (running via Docker)
- **AI/LLM**: OpenAI `text-embedding-3-small` (Embeddings) + `gpt-4o-mini` (Generation)

---

## ⚡ Quick Start (One Command)
If you have `make` installed (or use standard commands):

```bash
# Starts Weaviate, Backend, and Frontend in new terminals
make up

# Stops Weaviate
make down
```

---

## 🏗️ Architecture | البنية التقنية

```mermaid
graph LR
    A[Frontend (Vue 3)] -->|POST /chat| B[Backend API (FastAPI)]
    B -->|Query| C{Intent Check}
    C -->|Greeting| D[Immediate Response]
    C -->|Question| E[Retriever (Weaviate)]
    E -->|Context Docs| F[Generator (OpenAI GPT-4o)]
    F -->|Answer + Sources| B
    B -->|JSON Response| A
```

1. **User** sends a message via the Vue 3 frontend.
2. **Backend** checks if it's a greeting/small-talk (returns fast response).
3. If factual, **Retriever** fetches relevant chunks from Weaviate.
4. **Generator** synthesizes an answer using the retrieved context + GPT-4o-mini.
5. **Response** includes the answer and citation sources.

---

## 🚀 Setup Instructions | خطوات التثبيت

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### 1. Start Vector Database (Weaviate)
```bash
# From project root
docker-compose up -d
```
*Ensure Weaviate is running on `localhost:8080`*

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Ingest data (one-time setup)
python scripts/ingest.py

# Run Server
uvicorn app.main:app --reload
```
*Backend runs on `http://localhost:8000`*

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run Development Server
npm run dev
```
*Frontend runs on `http://localhost:5173`*

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Required for Embeddings & Chat generation |
| `VITE_API_BASE_URL` | Frontend config for Backend API URL (default: http://localhost:8000) |

---

## 💡 Usage Examples

### Test via CURL
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is Riyadh Season?"}'
```

### Response Format
```json
{
  "answer": "Riyadh Season is an annual entertainment festival...",
  "sources": [
    {
      "section": "Tourism",
      "score": 0.89,
      "snippet": "..."
    }
  ]
}
```

---

## 📸 Screenshots

## 📸 Screenshots

> **Note:** Place your screenshots in `docs/screenshots/` with the exact filenames below.

### Welcome Screen
![Welcome Screen](docs/screenshots/welcome.png)

### Chat Interface
![Chat Interface](docs/screenshots/chat.png)

### Sources Sheet
![Sources Sheet](docs/screenshots/sources.png)

---

## ❓ Troubleshooting

- **Docker not running**: Verify with `docker ps`. If Weaviate fails, check port 8080 conflicts.
- **CORS Errors**: Ensure `backend/app/main.py` has the correct `allow_origins`.
- **Mobile Access**: If testing on phone/LAN, update `VITE_API_BASE_URL` in frontend to your PC's local IP (e.g., `http://192.168.1.5:8000`) instead of `localhost`.

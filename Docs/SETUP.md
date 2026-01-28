# Setup Guide

This guide covers local development setup for the Saudipedia RAG Chatbot.

## Requirements

- Docker + Docker Compose
- Python 3.10+
- Node.js 18+
- (Optional) `make`

---

## 1) Start the Vector Database (Weaviate)

From the project root:

```bash
docker-compose up -d
```

Verify it is running:

- Weaviate: `http://localhost:8080`

If port `8080` is already in use, stop the conflicting service or update the port mapping in `docker-compose.yml`.

---

## 2) Backend Setup (FastAPI)

```bash
cd backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Add OPENAI_API_KEY to .env

python scripts/ingest.py
uvicorn app.main:app --reload
```

Backend runs at:

- API: `http://localhost:8000`

Notes:
- `python scripts/ingest.py` is typically a one-time setup unless you change the dataset or embeddings.

---

## 3) Frontend Setup (Vue 3)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

- Web: `http://localhost:5173`

---

## Environment Variables

### Backend

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Required for embeddings and answer generation |

### Frontend

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Backend API base URL (default: `http://localhost:8000`) |

---

## API Smoke Test

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Riyadh Season?"}'
```

Expected shape:

```json
{
  "answer": "...",
  "sources": [
    {
      "section": "...",
      "score": 0.89,
      "snippet": "..."
    }
  ]
}
```

---

## Troubleshooting

### Docker not running / Weaviate not starting
- Check Docker status:
  ```bash
  docker ps
  ```
- Check container logs:
  ```bash
  docker-compose logs -f
  ```

### Port conflict (8080)
- Ensure no other service is using port `8080`.
- If needed, change the port mapping in `docker-compose.yml`.

### CORS errors
- Ensure FastAPI CORS middleware allows your frontend origin (e.g. `http://localhost:5173`).
- Update the allowed origins in `backend/app/main.py`.

### Testing from mobile / LAN
If you want to access the frontend from your phone:
1. Use your machine’s local IP for the backend (example):
   - `http://192.168.1.5:8000`
2. Set it in the frontend environment:
   - `VITE_API_BASE_URL=http://192.168.1.5:8000`

---

## Shutdown / Cleanup

Stop containers:

```bash
docker-compose down
```

If you used `make`:

```bash
make down
```

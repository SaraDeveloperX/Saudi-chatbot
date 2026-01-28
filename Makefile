.PHONY: up down backend frontend

# Quick up: Start Weaviate (Docker) + Backend (New Terminal) + Frontend (New Terminal)
up:
	@echo "Starting Weaviate..."
	docker-compose up -d
	@echo "Starting Backend server..."
	start "Saudipedia Backend" cmd /k "cd backend && (if exist venv\Scripts\activate call venv\Scripts\activate) && uvicorn app.main:app --reload"
	@echo "Starting Frontend server..."
	start "Saudipedia Frontend" cmd /k "cd frontend && npm run dev"

# Stop services
down:
	@echo "Stopping Weaviate..."
	docker-compose down

# Run backend only (current terminal)
backend:
	cd backend && uvicorn app.main:app --reload

# Run frontend only (current terminal)
frontend:
	cd frontend && npm run dev

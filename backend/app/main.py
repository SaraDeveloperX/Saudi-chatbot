from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from app.rag.retriever import retrieve
from app.rag.generator import generate_answer, NO_ANSWER_MESSAGE

app = FastAPI(title="Saudipedia Chatbot API")

# CORS for frontend
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    message: str

class SourceItem(BaseModel):
    section: str
    question: str
    source: str
    score: float
    snippet: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]

@app.get("/health")
def health_check():
    return {"status": "ok"}

def check_intent(message: str) -> Optional[str]:
    """
    Check if the message is a greeting or small talk.
    Returns the response string if matched, else None.
    """
    msg = message.strip().lower()
    
    # Greetings
    greetings = ["هلا", "هلا والله", "مرحبا", "السلام عليكم", "صباح الخير", "مساء الخير", "hi", "hello"]
    if any(g in msg for g in greetings):
        if "السلام عليكم" in msg:
            return "وعليكم السلام 👋 تفضل/ي، وش ودّك تعرف عن السعودية؟"
        return "هلا والله 👋 أنا هنا عشان أساعدك بمعلومات عن السعودية. وش تحب تعرف؟"
        
    # Thanks
    thanks = ["شكرا", "يعطيك العافية", "thx", "thanks"]
    if any(t in msg for t in thanks):
        return "العفو! إذا عندك سؤال ثاني عن السعودية أنا حاضر 😊"
        
    # Goodbye
    goodbye = ["مع السلامة", "باي", "bye"]
    if any(g in msg for g in goodbye):
        return "مع السلامة 👋 وإذا احتجت أي معلومة عن السعودية ارجع لي بأي وقت."
        
    return None

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    RAG Chat endpoint.
    Retrieves relevant documents and generates an Arabic answer with citations.
    """
    try:
        # 1. Check intent (Greetings/Small-talk)
        intent_response = check_intent(request.message)
        if intent_response:
            return ChatResponse(answer=intent_response, sources=[])

        # Retrieve relevant documents
        contexts = retrieve(request.message, top_k=5)
        
        # Generate answer
        answer = generate_answer(request.message, contexts)
        
        # Build sources list with snippets
        sources = []
        for ctx in contexts:
            sources.append(SourceItem(
                section=ctx["section"],
                question=ctx["question"],
                source=ctx["source"],
                score=ctx["score"],
                snippet=ctx["text"][:200] + "..." if len(ctx["text"]) > 200 else ctx["text"]
            ))
        
        return ChatResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

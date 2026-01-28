<p align="center">
  <img
    src="Docs/Logo.png"
    alt="Saudi RAG Chatbot"
    width="170"
    style="border-radius: 50%;"
  />
</p>

<h1 align="center">Saudi RAG Chatbot</h1>

<p align="center">
  Production-grade Retrieval-Augmented Generation (RAG) system for answering factual questions about Saudi Arabia using the Saudipedia knowledge base.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/Vue-3-brightgreen" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-success" />
  <img src="https://img.shields.io/badge/Weaviate-VectorDB-orange" />
  <img src="https://img.shields.io/badge/Docker-Ready-blue" />
</p>

---

## Overview

This system combines semantic retrieval with controlled language generation to produce accurate, source-grounded answers with explicit source attribution.

---

## System Overview

<p align="center">
  <img src="Docs/System-Overview.png" width="85%"/>
</p>

---

## Quick Start

```
make up
```

Starts:
- Weaviate
- Backend API
- Frontend app

Stop services:
```
make down
```

> For full setup and local development details, see:  
→ **[Setup Guide](Docs/SETUP.md)**


---

## API

```
POST /chat
```

Response:
```
{
  "answer": "...",
  "sources": [...]
}
```

---

## Data Source

[Saudipedia Arabic Q&A Knowledge Base](https://www.kaggle.com/datasets/ahmadhakami/saudipedia-arabic-q-and-a-knowledge-base)

---

## License

MIT License

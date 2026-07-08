<div align="center">

# ✉️ AetherMail

### Your Inbox. Managed by AI That Actually Does Things.

*Not a chatbot that tells you what to do. Two agents that do it for you.*

<br>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Graph-6C63FF?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash_Lite-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC143C?style=for-the-badge)](https://qdrant.tech)
[![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-Local_Embeddings-FFB300?style=for-the-badge)](https://www.sbert.net)
[![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-Stream_Layer-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)](https://kafka.apache.org)
[![Apache Spark](https://img.shields.io/badge/Apache_Spark-Big_Data-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org)
[![HDFS](https://img.shields.io/badge/HDFS-Data_Lake-66CCFF?style=for-the-badge&logo=apache&logoColor=white)](https://hadoop.apache.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br>

> *"Most AI email tools summarize your inbox. AetherMail acts on it — and now it can answer questions about your documents too."*

</div>

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Overall Architecture](#-overall-architecture)
3. [Assistant 1: Autonomous Email Agent](#-assistant-1-autonomous-email-agent)
4. [Assistant 2: Benefits RAG Assistant](#-assistant-2-benefits-rag-assistant-new)
5. [RAG Pipeline Deep Dive](#-rag-pipeline-deep-dive)
6. [Big Data Pipeline](#-big-data-pipeline)
7. [Backend Architecture](#-backend-architecture)
8. [Frontend Architecture](#-frontend-architecture)
9. [Project Structure](#-project-structure)
10. [API Reference](#-api-reference)
11. [Setup & Installation](#-setup--installation)
12. [Roadmap](#-roadmap)
13. [Tech Stack](#-tech-stack)
14. [Contributors](#-contributors)

---

## 🧠 Project Overview

AetherMail has grown from a single email agent into a **multi-assistant AI platform**. It now ships with **two independent, swappable AI assistants** sitting behind one unified chat interface:

- **Email Agent** — a LangGraph-powered agent that autonomously manages your Gmail inbox: searching, labeling, drafting replies, and delegating bulk operations to a real Apache Spark cluster.
- **Benefits Assistant** *(new)* — a Retrieval-Augmented-Generation (RAG) assistant that answers questions strictly from your own documents (e.g. company benefits PDFs), with confidence scoring and page-level source attribution so it never hallucinates.

This isn't a wrapper around a chatbot with a Gmail plugin. It's a purpose-built platform with:

- A **Big Data pipeline** (Kafka → Spark → HDFS + PostgreSQL + Qdrant) that processes your inbox in real time
- A fully modular **local RAG pipeline** (Qdrant + Sentence Transformers) that answers questions only from retrieved evidence
- A **stateful AI agent** (LangGraph) that reasons step-by-step, chooses the right tool, and executes autonomously
- A **multi-assistant frontend** where switching assistants swaps the endpoint, welcome screen, suggestions, and behavior — with zero code duplication
- **AES encryption at rest** for every email body stored in HDFS
- **Full OAuth 2.0 + PKCE** Gmail integration with secure token management

---

## 🏗️ Overall Architecture

```
                                   USER
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │  (Assistant Switch)  │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    ▼                                ▼
        ┌───────────────────────┐        ┌───────────────────────────┐
        │   Email Agent          │        │   Benefits Assistant       │
        │   /api/v1/agent/execute│        │   /api/v1/benefits/ask     │
        └───────────┬───────────┘        └─────────────┬─────────────┘
                    │                                    │
                    ▼                                    ▼
        ┌───────────────────────┐        ┌───────────────────────────┐
        │  LangGraph State Machine│      │   RAG Service Pipeline      │
        │  Gemini 2.5 Flash Lite   │      │   Retriever → Context →    │
        │  Tool Router             │      │   Generator → Confidence   │
        └───────────┬───────────┘        └─────────────┬─────────────┘
                    │                                    │
      ┌─────────────┼──────────────┐                    │
      ▼             ▼              ▼                    ▼
 ┌─────────┐  ┌──────────┐  ┌────────────┐      ┌───────────────┐
 │Gmail API│  │  Kafka   │  │   HDFS     │      │    Qdrant      │
 │(Actions)│  │ → Spark  │  │ (Encrypted │      │ (Vector Search │
 │         │  │ Streaming│  │  Archive)  │      │  + Metadata)   │
 └─────────┘  └────┬─────┘  └────────────┘      └───────────────┘
                    │
                    ├──► PostgreSQL (metadata)
                    ├──► HDFS (AES-encrypted body)
                    └──► Qdrant (vector embeddings)
```

Both assistants share the same Qdrant vector store and PostgreSQL instance, but operate on independent collections and independent conversational contexts, wired together only through a shared `ASSISTANTS` configuration on the frontend.

---

## 🤖 Assistant 1: Autonomous Email Agent

**Purpose:** natural language email management.

> *"Delete all newsletters older than 6 months."*

The agent reasons using a compiled **LangGraph** state machine and decides which tools to execute — it doesn't just suggest actions, it performs them.

### Capabilities

- Gmail semantic search
- Gmail label creation & management
- Draft replies
- Email organization (archive, delete, move)
- Bulk operations delegated to Spark via Kafka
- Full chain-of-thought audit trail

### Agent State

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_id: str  # injected per-request for tool authorization
```

### Agent Tools

| Tool | Backend | When the Agent Uses It |
|---|---|---|
| `search_emails_semantic` | Qdrant vector search | "Find emails about the Q3 report" |
| `organize_email` | Gmail API | "Archive all newsletters" |
| `create_new_label` | Gmail API | "Create a folder called 'Tax 2025'" |
| `create_draft_reply` | Gmail API | "Draft a reply saying I'll call back tomorrow" |
| `trigger_bulk_action_job` | Kafka producer | "Delete all emails older than 2023 from marketing@..." |
| `fetch_raw_email_from_hdfs` | Spark + HDFS | "Quote the exact text from the contract email" |

### Routing Logic

```
START → agent node
           │
           ├── has tool_calls? → tools node → back to agent
           │
           └── no tool_calls?  → END (return final response)
```

The agent's system prompt enforces strict architectural rules: bulk operations on hundreds of emails **must** be delegated to Kafka/Spark rather than looped over individually — this is prompt-level enforcement backed by a real distributed pipeline.

---

## 📚 Assistant 2: Benefits RAG Assistant *(NEW)*

**Purpose:** question answering over your own documents — no internet knowledge, no guessing.

> *"What dental services are covered?"*

Instead of relying on the LLM's parametric knowledge, this assistant performs **Retrieval-Augmented Generation** end-to-end: it retrieves the most relevant chunks from your documents, builds grounded context, and generates an answer that cites exactly where it came from.

### Assistant Pipeline

```
Question
   │
   ▼
Retriever  ──►  Qdrant Vector Search  ──►  Top-K Documents
   │
   ▼
Context Builder  (formats chunks + doc name + page + score)
   │
   ▼
Generator  (Gemini 2.5 Flash Lite, strict grounded prompt)
   │
   ▼
Confidence Evaluation
   │
   ▼
Structured Response { answer, confidence, sources }
```

### Structured Response Format

```json
{
  "answer": "...",
  "confidence": 0.76,
  "sources": [
    { "document": "DentalPPO.pdf", "page": 51 },
    { "document": "DentalPPO.pdf", "page": 50 },
    { "document": "DentalPPO.pdf", "page": 44 }
  ]
}
```

### Confidence System — No Hallucinations

```
Highest similarity score
        │
        ▼
Compare against threshold
        │
        ▼
Too low?  ──► "I couldn't find reliable information..."
        │
Above threshold?  ──► Generate grounded answer
```

Every answer surfaces a **confidence badge** and a **sources list** (document name + page number) directly in the chat UI, so the user can verify every claim at a glance.

---

## 🧩 RAG Pipeline Deep Dive

The RAG module is fully modular — every stage is a swappable, independently-testable component.

```
rag/
├── config.py                 # RAG-wide configuration
├── document.py                # Document/chunk data models
├── ingest.py                  # PDF loading + chunking
├── embedder.py                 # Embedding generation entrypoint
├── qdrant_store.py            # Vector store client
├── retriever.py                # Top-K semantic retrieval + scoring
├── context_builder.py          # Formats retrieved chunks into prompt context
├── generator.py                # Gemini-backed, grounded-only generation
├── rag_response.py             # Structured response schema
├── rag_service.py              # Central orchestrator
└── providers/
    ├── base.py                     # EmbeddingProvider interface
    ├── factory.py                  # get_embedding_provider()
    └── sentence_transformer_embeddings.py
```

### Component Responsibilities

**Retriever** — generates query embeddings, searches Qdrant, retrieves Top-K chunks, attaches similarity scores.

**Context Builder** — formats retrieved chunks with document name, page number, and similarity score into a single prompt context.

**Generator** — uses Gemini 2.5 Flash Lite under a strict prompt: answer *only* from retrieved context, never hallucinate, refuse when the answer isn't present.

**RAG Service** — the orchestrator tying Retriever → Context Builder → Generator → Confidence Evaluation into one structured response.

### Embedding Architecture

The project **migrated away from Gemini embeddings** to a fully local embedding stack:

```
Gemini Embeddings  ──►  Sentence Transformers (all-MiniLM-L6-v2)
```

**Why the switch:** local, fast, free, zero API cost, and no external rate limits.

### Embedding Provider Abstraction

```
EmbeddingProvider (interface)
        │
        ▼
get_embedding_provider()  ── factory
        │
        ▼
SentenceTransformerEmbeddingProvider  (current implementation)
```

This abstraction means future embedding models — Gemini, OpenAI, Voyage AI, BGE, Instructor XL — can be swapped in without touching the rest of the RAG pipeline.

### Qdrant Storage

Stores both vectors and rich metadata (`document`, `page`, `chunk`, `source`, `filename`), and performs semantic search via cosine similarity.

---

## ⚙️ Big Data Pipeline

This is the part that makes the Email Agent different from every other "AI + Gmail" project.

When ingestion is triggered, emails are not processed one-by-one in Python — they flow through a **distributed streaming pipeline**.

### Step 1 — Ingest (Gmail → Kafka)
The FastAPI endpoint fetches raw Gmail JSON payloads in a background task and streams them into a Kafka topic (`raw_emails`). The response returns immediately — no blocking.

### Step 2 — Transform (Spark Structured Streaming)
A Spark job listens to the Kafka topic in real time and, for each batch, fans out to three destinations in parallel:

| Destination | What Happens |
|---|---|
| **PostgreSQL** | Structured metadata (sender, subject, thread_id, labels) written via JDBC |
| **HDFS Data Lake** | Raw email body **AES-encrypted** via a Spark UDF, written as Parquet to `hdfs://localhost:9000/aethermail/raw_emails` |
| **Qdrant** | Email snippet embedded and stored with metadata payload for semantic search |

```
Gmail API
   │
   ▼ (raw JSON)
Kafka Topic: raw_emails
   │
   ▼ (Spark Structured Streaming)
   ├──► PostgreSQL    → metadata (sender, subject, date, labels)
   ├──► HDFS Parquet  → AES-encrypted body_text
   └──► Qdrant        → vector embedding + metadata payload
```

---

## 🖥️ Backend Architecture

### Security

- **OAuth 2.0 + PKCE** — Gmail authorization uses the PKCE flow; the verifier is stored temporarily during the handshake and wiped after code exchange
- **JWT Access + Refresh Pair** — refresh tokens carry a typed claim to prevent token-type confusion attacks
- **AES Encryption at Rest** — email bodies in HDFS are Fernet-encrypted (AES-128 CBC + HMAC); decryption only happens when a tool explicitly requests it
- **No Credentials in Code** — all secrets loaded via `.env` through Pydantic Settings

### Database Schema

```
users
  │
  ├── oauth_tokens (1:1)     → access_token, refresh_token, pkce_verifier, scopes
  ├── emails (1:N)           → gmail_id, thread_id, vector_id (→ Qdrant), hdfs_path (→ HDFS)
  ├── user_preferences (1:N) → key-value JSON store for user settings
  └── agent_tasks (1:N)
        └── action_logs (1:N)
              └── agent_thoughts (1:N)  → tool_used, thought_process (chain-of-thought audit)
```

Every agent action is fully auditable: task → action log → thought chain, with the tool used and reasoning recorded at every step.

---

## 🎨 Frontend Architecture

Built with **React + Vite**, using the Context API for state management.

### AuthContext
Handles login, logout, OAuth, and JWT lifecycle.

### ChatContext
Handles conversations, active chat state, thinking/loading state, **assistant selection**, API routing, and conversation history.

### Multi-Assistant System *(NEW)*

Rather than hardcoding a single assistant, the frontend is driven by an `ASSISTANTS` configuration file:

```
Benefits Assistant  ──►  /benefits/ask
Email Agent         ──►  /agent/execute
```

Each assistant entry defines its own `name`, `endpoint`, welcome title, subtitle, and suggestion prompts. **Future assistants require only a configuration entry — no new code.**

### Chat Flow

```
User Message
     │
     ▼
ChatContext
     │
     ▼
Assistant Config (selects endpoint + behavior)
     │
     ▼
Backend API
     │
     ▼
Assistant Response
     │
     ▼
Chat Window
```

### Benefits Chat UI Features

- Confidence badge (e.g. `76%`)
- Sources section (document name + page number)
- Multi-line, bullet-formatted answers

### Assistant Switching

Switching between Email Agent and Benefits Assistant automatically swaps the endpoint, welcome screen, suggestions, placeholder text, and chat behavior — with no code duplication.

---

## 📦 Project Structure

```
autonomous_mail/
│
├── backend/
│   ├── alembic/                        # Database migration versions
│   │   └── versions/
│   │       ├── b610e434963d_*.py       # Initial schema
│   │       └── 7648cf5586b8_*.py       # Add PKCE verifier
│   │
│   ├── app/
│   │   ├── agent/
│   │   │   ├── graph.py                # LangGraph state machine + system prompt
│   │   │   ├── llm.py                  # Gemini 2.5 Flash Lite config
│   │   │   └── tools/
│   │   │       ├── email_tools.py      # Qdrant semantic search tool
│   │   │       └── action_tools.py     # Gmail + Kafka + HDFS action tools
│   │   │
│   │   ├── rag/
│   │   │   ├── config.py
│   │   │   ├── context_builder.py
│   │   │   ├── document.py
│   │   │   ├── embedder.py
│   │   │   ├── generator.py
│   │   │   ├── ingest.py
│   │   │   ├── qdrant_store.py
│   │   │   ├── rag_response.py
│   │   │   ├── rag_service.py
│   │   │   ├── retriever.py
│   │   │   └── providers/
│   │   │       ├── base.py
│   │   │       ├── factory.py
│   │   │       └── sentence_transformer_embeddings.py
│   │   │
│   │   ├── api/v1/endpoints/
│   │   │   ├── auth.py                 # Google OAuth, JWT, PKCE flow
│   │   │   ├── emails.py               # Email CRUD + ingestion trigger
│   │   │   ├── agent.py                # POST /agent/execute endpoint
│   │   │   └── benefits.py             # POST /benefits/ask endpoint
│   │   │
│   │   ├── providers/                  # Shared provider abstractions
│   │   │
│   │   ├── core/
│   │   │   ├── gmail_service.py        # Gmail API client + token management
│   │   │   ├── parsing.py              # Raw Gmail JSON → Pydantic parser
│   │   │   ├── security.py             # JWT creation (access + refresh)
│   │   │   └── config.py               # Pydantic Settings
│   │   │
│   │   ├── data_pipeline/
│   │   │   ├── producer.py             # Kafka producer (EmailKafkaProducer)
│   │   │   └── spark_stream.py         # Spark Structured Streaming job
│   │   │
│   │   ├── models/                     # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── email.py
│   │   │   ├── oauth_token.py
│   │   │   ├── agent.py                # AgentTask, ActionLog, ActionType
│   │   │   └── agent_thought.py        # Chain-of-thought audit trail
│   │   │
│   │   └── schemas/                    # Pydantic request/response schemas
│   │
│   └── tests/                          # Retriever, Generator, Context Builder,
│                                        # Qdrant, Embeddings, RAG, PDF Loader,
│                                        # Batch Embedding, Dimension Validation
│
└── frontend/                           # React + Vite frontend
    └── src/
        └── context/
            ├── AuthContext.jsx
            └── ChatContext.jsx
```

---

## 🔌 API Reference

### Email Agent

```
POST /api/v1/agent/execute
```

**Request**
```json
{ "prompt": "Find emails from my manager about the Q3 report and label them as Urgent" }
```

**Response**
```json
{
  "task_id": "a3f2c1d4-...",
  "agent_response": "Done. I found 3 emails related to the Q3 report and labeled 2 from your manager as Urgent."
}
```

### Benefits Assistant

```
POST /api/v1/benefits/ask
```

**Request**
```json
{ "question": "What dental services are covered?" }
```

**Response**
```json
{
  "answer": "...",
  "confidence": 0.76,
  "sources": [
    { "document": "DentalPPO.pdf", "page": 51 }
  ]
}
```

---

## ⚡ Setup & Installation

### Prerequisites

| Service | Purpose |
|---|---|
| Python 3.10+ | Backend runtime |
| PostgreSQL | Structured metadata storage |
| Apache Kafka | Email streaming queue |
| Apache Spark | Distributed stream processing |
| Apache Hadoop (HDFS) | Raw email data lake |
| Qdrant | Vector search database |
| Sentence Transformers (`all-MiniLM-L6-v2`) | Local embedding model |
| Google Cloud Console project | OAuth 2.0 + Gmail API |
| Gemini API key | LLM for both assistants |

### 1. Clone the repository
```bash
git clone https://github.com/VedeshP/autonomous_mail.git
cd autonomous_mail/backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in `backend/`:
```env
# PostgreSQL
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=aethermail
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# JWT
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Gemini
GEMINI_API_KEY=your_gemini_api_key

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# HDFS Encryption
HDFS_ENCRYPTION_KEY=your_fernet_key_here
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start infrastructure services
```bash
# Kafka (using Docker)
docker-compose up -d kafka zookeeper

# Qdrant
docker run -p 6333:6333 qdrant/qdrant

# HDFS (local pseudo-distributed mode)
start-dfs.sh
```

### 7. Start the Spark streaming job
```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.postgresql:postgresql:42.6.0 \
  app/data_pipeline/spark_stream.py
```

### 8. Ingest documents for the Benefits Assistant
```bash
python -m app.rag.ingest --source ./documents/
```

### 9. Start the FastAPI server
```bash
uvicorn app.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`

### 10. Start the frontend
```bash
cd ../frontend
npm install
npm run dev
```

---

## 🗺️ Roadmap

- [x] Google OAuth 2.0 + PKCE authentication flow
- [x] Gmail API integration (labels, drafts, read)
- [x] Kafka producer for email ingestion
- [x] Spark Structured Streaming pipeline
- [x] HDFS data lake with AES encryption at rest
- [x] Qdrant vector store
- [x] LangGraph agentic state machine
- [x] Full database audit trail (tasks → logs → thoughts)
- [x] Alembic schema migrations
- [x] Local Sentence Transformer embeddings
- [x] Modular embedding provider abstraction
- [x] Benefits RAG Assistant
- [x] RAG pipeline (retriever, context builder, generator)
- [x] Confidence scoring
- [x] Source attribution (document + page)
- [x] Multi-assistant frontend architecture
- [ ] Conversation memory
- [ ] Streaming responses
- [ ] Hybrid retrieval (BM25 + Vector)
- [ ] Re-ranking
- [ ] User memory / preference-aware responses
- [ ] Agentic RAG
- [ ] Multi-document reasoning
- [ ] Gmail Push Notifications via Pub/Sub (real-time inbox watch)
- [ ] Multi-account support
- [ ] Bulk analytics via Spark SQL (email trends, sender stats)
- [ ] Docker Compose full-stack setup

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Agent Orchestration | LangGraph (StateGraph) |
| LLM | Gemini 2.5 Flash Lite |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) — local, free, no API cost |
| Vector Database | Qdrant |
| Stream Processing | Apache Spark Structured Streaming |
| Message Queue | Apache Kafka |
| Data Lake | HDFS (Hadoop) + Parquet |
| Relational DB | PostgreSQL |
| ORM | SQLAlchemy + Alembic |
| Auth | Google OAuth 2.0 (PKCE) + JWT (python-jose) |
| Encryption | Fernet (AES-128 CBC + HMAC) |
| Gmail Integration | Google Gmail API v1 |
| Validation | Pydantic v2 |
| Frontend | React + Vite + Context API + CSS Modules |

---

## 🤝 Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/VedeshP">
        <img src="https://github.com/VedeshP.png" width="100px;" alt=""/>
        <br />
        <sub><b>Vedesh Pandya</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/chetangadhiya5062">
        <img src="https://github.com/chetangadhiya5062.png" width="100px;" alt=""/>
        <br />
        <sub><b>Chetan Gadhiya</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/piyush-2k5">
        <img src="https://github.com/piyush-2k5.png" width="100px;" alt=""/>
        <br />
        <sub><b>Piyush Soni</b></sub>
      </a>
    </td>
  </tr>
</table>

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

*Built with obsessive attention to backend architecture — now with grounded, hallucination-free RAG.*

⭐ **Star the repo** · 🐛 **Open an issue** · 🔀 **Submit a PR**

</div>

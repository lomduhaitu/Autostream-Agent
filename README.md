# Social-to-Lead AI Agent 
---

## 1. Project Overview

This project implements a **Conversational AI Agent** for *AutoStream*, a video editing SaaS platform. The agent is built to automate the top-of-funnel sales process by acting as a knowledgeable representative.

**Key Capabilities:**
* **🤖 Answer Questions:** Uses **RAG (Retrieval-Augmented Generation)** to fetch accurate pricing, policy, and feature information from a local knowledge base (`knowledge_base.md`).
* **🧠 Detect Intent:** Intelligently distinguishes between casual inquiries and **high-intent buying signals**.
* **🎣 Capture Leads:** Automatically switches context to collect specific user details (Name, Email, Creator Platform) and executes a backend lead capture tool only when all slots are filled.

---

## 2. How to Run Locally

### Prerequisites
* **Python 3.9+**
* **Google AI Studio API Key** (for Gemini 1.5 Flash)

### Installation Steps

**1. Clone the Repository**
```bash
git clone <your-repo-url-here>
cd AutoStream-Agent
```

**2. Create & Activate Virtual Environment Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

Mac: 
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables Create a .env file in the root directory and add your Google API key**

GOOGLE_API_KEY=AIzaSy...Your_Key_Here

**Usage**
Option A: Web Interface (Recommended for Demo) Runs a polished chat UI using Streamlit.
```bash
streamlit run app.py
```

Option B: CLI Mode (Terminal) Runs the agent directly in your command line for debugging.
```bash
python main.py
```

**3. Architecture Explanation**


Why LangGraph?

For this workflow, I chose LangGraph over standard linear chains (LangChain) or AutoGen. The "Social-to-Lead" problem requires a cyclic state machine rather than a linear pipeline.

Cyclic Behavior: Real conversations are non-linear. If a user provides an invalid email or forgets to mention their platform, the agent must "loop back" and ask specifically for that missing piece of data. Standard DAGs (Directed Acyclic Graphs) struggle with these dynamic loops.

Fine-Grained Control: LangGraph allows the agent to decide the next step dynamically—choosing whether to call the RAG tool, the Lead Capture tool, or simply reply with text—based on the current conversation state.

State Management
State is persisted using LangGraph’s MemorySaver checkpointer.


**Data Flow Diagram:**

1. Ingest: knowledge_base.md → Split into Chunks → Google Embeddings → FAISS Index.

2. Query: User Question → Google Embeddings → Semantic Search on FAISS.

3. Augment: Top 3 relevant chunks + User Question → System Prompt.

4. Generate: Gemini 1.5 Flash → Final Answer.

Mechanism: The graph maintains a messages list within its state. Every user input and AI response is appended to this history.

Persistence: A unique thread_id is assigned to every user session. This acts as "Short-Term Memory," allowing the LLM to recall previous turns (e.g., remembering the user's name mentioned 3 messages ago) to fill the required lead slots without asking redundant questions.

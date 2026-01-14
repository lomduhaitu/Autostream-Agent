# Social-to-Lead AI Agent (Inflx)

**Company:** ServiceHive | **Product:** Inflx  
**Role:** Machine Learning Intern Assignment  
**Author:** Vaishnav Bhor

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
cd AutoStream-Agent'''bash

**2. Create & Activate Virtual Environment Windows:**
python -m venv venv
.\venv\Scripts\activate

Mac: 
python3 -m venv venv
source venv/bin/activate

**3. Install Dependencies**
pip install -r requirements.txt

**4. Configure Environment Variables Create a .env file in the root directory and add your Google API key**
GOOGLE_API_KEY=AIzaSy...Your_Key_Here

**Usage**
Option A: Web Interface (Recommended for Demo) Runs a polished chat UI using Streamlit.
streamlit run app.py

Option B: CLI Mode (Terminal) Runs the agent directly in your command line for debugging.
python main.py

**3. Architecture Explanation**


Why LangGraph?
For this workflow, I chose LangGraph over standard linear chains (LangChain) or AutoGen. The "Social-to-Lead" problem requires a cyclic state machine rather than a linear pipeline.

Cyclic Behavior: Real conversations are non-linear. If a user provides an invalid email or forgets to mention their platform, the agent must "loop back" and ask specifically for that missing piece of data. Standard DAGs (Directed Acyclic Graphs) struggle with these dynamic loops.

Fine-Grained Control: LangGraph allows the agent to decide the next step dynamically—choosing whether to call the RAG tool, the Lead Capture tool, or simply reply with text—based on the current conversation state.

State Management
State is persisted using LangGraph’s MemorySaver checkpointer.

Mechanism: The graph maintains a messages list within its state. Every user input and AI response is appended to this history.

Persistence: A unique thread_id is assigned to every user session. This acts as "Short-Term Memory," allowing the LLM to recall previous turns (e.g., remembering the user's name mentioned 3 messages ago) to fill the required lead slots without asking redundant questions.


**4. WhatsApp Deployment Strategy**


To deploy this agent on WhatsApp, I would integrate it using the Meta Cloud API and a FastAPI middleware.

**Architecture Flow**
WhatsApp User → Meta Cloud → FastAPI Webhook → LangGraph Agent → Response

**Implementation Plan**
1. Webhook Setup: Develop a Python FastAPI application with a POST /webhook endpoint. This endpoint verifies the Meta verification token and receives incoming messages.

2. Message Handling: When a webhook event triggers, the system extracts the JSON payload:

3. Identity: The user's phone number (wa_id) is extracted.

4. Session Mapping: The phone number is used as the thread_id in LangGraph. This ensures every WhatsApp user has a completely isolated conversation history.

5. Async Processing: LLM inference can take 2-5 seconds, which may cause the Meta webhook to timeout. To solve this, I would use Background Tasks (via asyncio or Celery). The API immediately returns a 200 OK to Meta to acknowledge receipt, while the agent processes the logic asynchronously.

6. Response Delivery: Once the LangGraph agent generates a response, the system sends a POST request to the Meta Graph API (/messages endpoint) to push the reply back to the user's specific WhatsApp number.

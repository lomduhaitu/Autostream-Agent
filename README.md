**Social-to-Lead AI Agent (Inflx)
Company: ServiceHive | Product: Inflx**

**1. Project Overview**

This project implements a Conversational AI Agent for video editing platform. The agent is designed to:

Answer Questions: Uses RAG (Retrieval-Augmented Generation) to answer pricing and policy questions from a local knowledge base.
Detect Intent: Distinguishes between casual queries and high-intent buying signals.
Capture Leads: Intelligently collects user details (Name, Email, Platform) and executes a lead capture tool only when all information is gathered.

**2. How to Run Locally**

Prerequisites:
Python 3.9+
A Google AI Studio API Key (for Gemini 1.5 Flash)

Installation Steps

1. Clone the Repository
Bash
git clone <repository-url>

2. Set directory
cd AutoStream-Agent

3. Create & Activate Virtual Environment
Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

4. Install Dependencies
Bash
pip install -r requirements.txt

5. Configure Environment Variables Create a .env file in the root directory and add your API key:
Code snippet
GOOGLE_API_KEY=**AIzaSy...Your_Key_Here**

6. Running the Agent
**Option A:** Web Interface (Recommended for Demo) Runs a polished chat UI using Streamlit.
Bash
streamlit run app.py

**Option B:** CLI Mode (Terminal) Runs the agent directly in your command line.
Bash
python main.py

**3. Architecture Explanation**

Why LangGraph? For this workflow, I chose LangGraph over standard linear chains (LangChain) or AutoGen. The "Social-to-Lead" problem requires a cyclic state machine rather than a straight line.
Cyclic Behavior: If a user provides an invalid email or misses a specific slot (e.g., forgets to mention their platform), the agent must loop back and ask again. Standard chains are Directed Acyclic Graphs (DAGs) and struggle with these dynamic loops.
Control: LangGraph provides fine-grained control over the "Reasoning Loop," allowing the agent to decide whether to call a tool (RAG/Lead Capture) or respond to the user based on the current context, rather than following a hard-coded set of steps.
State Management State is persisted using LangGraph’s MemorySaver checkpointer.
Mechanism: The graph maintains a messages list within its state. Every user input and AI response is appended to this history.
Persistence: A unique thread_id is assigned to every user session. This allows the LLM to access the full conversation context (short-term memory) to determine which slots (Name, Email, Platform) have already been filled and which remain missing, ensuring a natural, multi-turn conversation without data loss.

**4. WhatsApp Deployment Strategy**

To deploy this agent on WhatsApp, I would integrate it using the Meta Cloud API and a FastAPI middleware.
Architecture: WhatsApp User -> Meta Cloud -> FastAPI Webhook -> LangGraph Agent -> Response

**Implementation Steps:**

Webhook Setup: Develop a Python FastAPI application with a POST /webhook endpoint. This endpoint will be verified and registered in the Meta Developer Portal.
Message Handling: When a user sends a message, Meta sends a JSON payload to the webhook.
Extract: Parse the user's phone number (wa_id) and text body.
Session Mapping: Use the phone number as the thread_id in LangGraph. This ensures that every WhatsApp user has their own isolated conversation memory.
Async Processing: Since LLM inference can take a few seconds (which might time out the Meta webhook), I would use a background task (using asyncio or Celery). The API immediately acknowledges the webhook with a 200 OK, while the agent processes the logic in the background.
Response Delivery: Once the LangGraph agent generates a text response (or tool output), the system sends a POST request back to the Meta Graph API (/messages endpoint) to deliver the reply to the user's WhatsApp number.

**Author:** Vaishnav Bhor

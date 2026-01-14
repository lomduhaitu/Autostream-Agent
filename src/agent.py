from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from src.tools import lookup_policy, mock_lead_capture
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 2. Define the System Prompt
SYSTEM_PROMPT = """
You are 'Inflx', a sales development representative for AutoStream, a video editing SaaS.

Your goal is to assist users and convert high-intent users into leads.

### INSTRUCTIONS:
1. **Intent Detection**:
   - If the user greets (e.g., "Hi"), respond warmly and briefly introduce AutoStream.
   - If the user asks about Pricing/Policies, use the `lookup_policy` tool to find the answer.
   - If the user shows **High Intent** (e.g., "I want to buy", "Sign me up", "Interested in Pro"), you must shift to Lead Capture mode.

2. **Lead Capture Protocol (High Intent Only)**:
   - You need to collect three pieces of info: **Name**, **Email**, and **Creator Platform** (e.g., YouTube, Insta).
   - Do NOT ask for all three at once. Ask naturally in conversation. 
   - Once you have ALL three values, you MUST call the `mock_lead_capture` tool immediately.

3. **Tone**: Professional, helpful, and concise.
"""

# 3. Create the Agent Graph
memory = MemorySaver()
tools = [lookup_policy, mock_lead_capture]

# --- THE FIX IS HERE ---
# We changed 'state_modifier' to 'prompt' to match your installed version.
agent_executor = create_react_agent(
    llm, 
    tools, 
    checkpointer=memory,
    prompt=SYSTEM_PROMPT 
)

def get_agent():
    return agent_executor
import streamlit as st
import uuid
from src.agent import get_agent

# Page Configuration
st.set_page_config(page_title="AutoStream AI Agent", page_icon="🤖")
st.title("🤖 AutoStream Sales Agent")
st.caption("Powered by Gemini 1.5 Flash & LangGraph")

# 1. Initialize Agent (Cached to prevent reloading on every interaction)
@st.cache_resource
def load_agent():
    return get_agent()

agent = load_agent()

# 2. Initialize Session State (Memory for the UI)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if prompt := st.chat_input("Ask about AutoStream plans..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        
        # Stream the response
        try:
            # We use stream() to get events as they happen
            events = agent.stream(
                {"messages": [("user", prompt)]},
                config,
                stream_mode="values"
            )

            for event in events:
                if "messages" in event:
                    last_msg = event["messages"][-1]
                    
                    # Only show AI messages (skip tool calls/user msgs)
                    if last_msg.type == "ai" and not last_msg.tool_calls:
                        content = last_msg.content
                        
                        # Fix for Gemini's list output format
                        if isinstance(content, list):
                            clean_text = "".join(
                                [part["text"] for part in content if "text" in part]
                            )
                            full_response = clean_text
                        else:
                            full_response = content
                        
            # Display final result
            if full_response:
                message_placeholder.markdown(full_response)
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                # Fallback if no text (e.g., tool just ran)
                pass 

        except Exception as e:
            st.error(f"An error occurred: {e}")
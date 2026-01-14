import uuid
from src.agent import get_agent

def main():
    agent = get_agent()
    
    # Generate a unique session ID
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("--- AutoStream AI Agent Initialized (Type 'q' to quit) ---")
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["q", "quit", "exit"]:
                print("Exiting...")
                break
            
            # Stream the agent's thought process and response
            events = agent.stream(
                {"messages": [("user", user_input)]},
                config,
                stream_mode="values"
            )

            for event in events:
                if "messages" in event:
                    last_msg = event["messages"][-1]
                    
                    # Check if it's an AI message (not a user or tool message)
                    if last_msg.type == "ai":
                        # If it has tool_calls, we ignore it (it's internal thinking)
                        if last_msg.tool_calls:
                            continue
                        
                        # --- FIX FOR GEMINI OUTPUT FORMAT ---
                        content = last_msg.content
                        
                        # If content is a list (Gemini format), extract the text
                        if isinstance(content, list):
                            # Join all text parts together
                            clean_text = "".join(
                                [part["text"] for part in content if "text" in part]
                            )
                            if clean_text:
                                print(f"Agent: {clean_text}")
                        
                        # If content is already a string (OpenAI format or simple text)
                        else:
                            print(f"Agent: {content}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
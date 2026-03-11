import os
from dotenv import load_dotenv
from sre_agent import agent_executor  # Importing the executor from your logic file

# 1. Load Environment Variables
load_dotenv()

def run_sre_assistant():
    """
    Main execution loop for the Agentic SRE Assistant.
    """
    print("="*60)
    print("🚀 AGENTIC SRE ASSISTANT IS ONLINE")
    print("="*60)
    print("Type 'exit' or 'quit' to stop the session.\n")

    while True:
        # Get user input from the terminal
        user_input = input("SRE-Task > ").strip()

        if user_input.lower() in ['exit', 'quit']:
            print("\nShutting down SRE Assistant. Stay stable! 🛠️")
            break

        if not user_input:
            continue

        try:
            print("\n[AI Thinking...]")
            # Running the imported agent_executor
            result = agent_executor.invoke({"input": user_input})
            
            print("\n" + "-"*30)
            print("✅ FINAL ADVICE / ACTION:")
            print(result["output"])
            print("-"*30 + "\n")

        except Exception as e:
            print(f"\n❌ ERROR: An issue occurred during execution: {e}\n")

if __name__ == "__main__":
    # Ensure OpenAI Key is present before starting
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ CRITICAL ERROR: OPENAI_API_KEY not found in .env file.")
    else:
        run_sre_assistant()
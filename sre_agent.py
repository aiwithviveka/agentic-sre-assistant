import os
import sys
import requests
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ API Key missing. Please check your environment variables.")
    sys.exit(1)

# 2. Define SRE Toolset
@tool
def monitor_api(url: str) -> str:
    """Checks the status and latency of a given URL."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        latency = (time.time() - start_time) * 1000
        status = "UP" if response.status_code == 200 else f"DOWN ({response.status_code})"
        return f"API {url} is {status}. Latency: {latency:.2f}ms."
    except Exception as e:
        return f"API {url} is DOWN. Error: {str(e)}"

@tool
def analyze_logs(filename: str = "sre_logs.log") -> str:
    """Reads the SRE log file from the workspace root using an absolute path."""
    # This fix ensures the UI and Terminal sessions look at the same file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    
    try:
        if not os.path.exists(file_path):
            return f"Log file '{file_path}' not found at {file_path}."
        with open(file_path, "r") as f:
            # We read the last 50 lines to keep context relevant and save tokens
            lines = f.readlines()
            content = "".join(lines[-50:])
        return f"Recent logs from {filename}:\n{content}"
    except Exception as e:
        return f"Error reading logs: {str(e)}"

@tool
def restart_service(service_name: str) -> str:
    """Simulates restarting a service or pod to resolve high memory or 500 errors."""
    print(f"🔄 [Action] Initiating restart for: {service_name}...")
    time.sleep(2)  # Simulate the 'Ops' wait time
    return f"Success: Service '{service_name}' has been restarted and memory cleared."

@tool
def notify_team(message: str) -> str:
    """Sends a critical alert to the SRE team."""
    print(f"📢 [Alert]: {message}")
    return f"Notification sent to team: {message}"

# 3. Setup Agent Toolkit
tools = [monitor_api, analyze_logs, restart_service, notify_team]

# 4. Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 5. Define System Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior SRE Agent.
    Your goal is to maintain 99.9% uptime. 
    - If you see a memory trend above 90% or a 500 error in logs, RESTART the affected service.
    - If you see security threats, NOTIFY the team.
    - Always verify the API health if backend errors are suspected."""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 6. Create Agent Executor
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 7. Main Execution (for terminal use)
if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "Run a full system health check."
    print(f"\n🚀 SRE AGENT ONLINE | Task: {user_input}\n")
    try:
        agent_executor.invoke({"input": user_input})
    except Exception as e:
        print(f"Critical Agent Failure: {str(e)}")
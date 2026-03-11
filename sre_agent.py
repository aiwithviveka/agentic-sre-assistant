import os
import ssl
import socket
import datetime
import numpy as np
import requests
from OpenSSL import crypto
from kubernetes import client, config as k8s_config
from dotenv import load_dotenv

# --- 2026 STABLE IMPORT LOGIC ---
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

# Direct imports to bypass __init__ and AttributeError
try:
    from langchain.agents.agent_executor import AgentExecutor
    from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
except ImportError:
    from langchain.agents import AgentExecutor, create_tool_calling_agent

# 1. SETUP CONFIGURATION
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ API Key missing. Please check your .env file.")

# Initialize the LLM (GPT-4o)
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

# --- MODULE 1: SSL MONITOR ---
@tool
def check_ssl_expiry(domain: str):
    """Returns the number of days until an SSL certificate expires for a domain."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                der_cert = ssock.getpeercert(True)
                x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, der_cert)
                expiry_str = x509.get_notAfter().decode('ascii')
                expiry_date = datetime.datetime.strptime(expiry_str, '%Y%m%d%H%M%SZ')
                days_left = (expiry_date - datetime.datetime.utcnow()).days
                return f"SSL for {domain} expires in {days_left} days."
    except Exception as e:
        return f"Error checking SSL for {domain}: {str(e)}"

# --- MODULE 2: LOG ANALYZER ---
@tool
def analyze_logs(file_path: str, search_query: str = "ERROR"):
    """Scans local log files for specific patterns like ERROR or CRITICAL."""
    if not os.path.exists(file_path):
        return "Log file not found."
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-100:] 
            matches = [l.strip() for l in lines if search_query.upper() in l.upper()]
        return f"Found {len(matches)} occurrences of '{search_query}': {matches[:3]}..."
    except Exception as e:
        return f"Log Read Error: {str(e)}"

# --- MODULE 3: API MONITORING ---
@tool
def monitor_api(url: str):
    """Checks the health and latency of a public or internal API endpoint."""
    try:
        start = datetime.datetime.now()
        response = requests.get(url, timeout=5)
        latency = (datetime.datetime.now() - start).total_seconds() * 1000
        status = "UP" if response.status_code == 200 else f"DOWN ({response.status_code})"
        return f"API {url} is {status}. Latency: {latency:.2f}ms."
    except Exception as e:
        return f"API {url} is unreachable: {str(e)}"

# --- MODULE 4: ANOMALY DETECTOR ---
@tool
def detect_anomalies(metrics_list: list[float]):
    """Uses Z-Score to identify statistical anomalies in a list of numbers."""
    if len(metrics_list) < 3: return "Not enough data for anomaly detection."
    data = np.array(metrics_list)
    mean, std = np.mean(data), np.std(data)
    z_scores = [(x - mean) / std if std > 0 else 0 for x in data]
    anomalies = [data[i] for i, z in enumerate(z_scores) if abs(z) > 2]
    return f"Anomalies found: {anomalies}. Mean: {mean:.2f}." if anomalies else "No anomalies detected."

# --- MODULE 5: KUBERNETES POD MANAGER ---
@tool
def manage_pods(action: str, namespace: str = "default", pod_name: str = None):
    """Actions: 'list_restarts' or 'restart' a pod."""
    try:
        k8s_config.load_kube_config()
        v1 = client.CoreV1Api()
        if action == "list_restarts":
            pods = v1.list_namespaced_pod(namespace)
            failing = [f"{p.metadata.name} ({sum(c.restart_count for c in p.status.container_statuses)} restarts)" 
                       for p in pods.items if p.status.container_statuses and any(c.restart_count > 0 for c in p.status.container_statuses)]
            return failing if failing else "All pods healthy."
        elif action == "restart" and pod_name:
            v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
            return f"Restarted pod {pod_name} in {namespace}."
    except Exception as e:
        return f"K8s Error: {str(e)}"

# --- 2. AGENT CONFIGURATION ---
tools = [check_ssl_expiry, analyze_logs, monitor_api, detect_anomalies, manage_pods]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Senior AI SRE. Use your tools for SSL, Logs, API, Anomaly Detection, and K8s. Troubleshoot step-by-step."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Define the agent and executor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# 3. SELF-TEST
if __name__ == "__main__":
    test_query = "Check health of https://api.github.com"
    print(f"Running self-test: {test_query}")
    try:
        agent_executor.invoke({"input": test_query})
    except Exception as e:
        print(f"Self-test failed: {e}")
        
        
# 🛡️ Agentic SRE Assistant: Autonomous Infrastructure Healing
An intelligent, **closed-loop automation system** designed to bridge the gap between observability and action. This agent doesn't just monitor logs; it reasons through system failures and autonomously executes remediation steps to maintain 99.9% uptime.

## About Me

Hey there! I'm Viveka Sharma, a Senior TechOps and DevOps Engineer and Agentic AI Developer with 5+ years of experience in infrastructure operations, automation, and observability. I specialize in building intelligent systems that make data work smarter — not harder!

## What I Do Best:

⚙️ Experienced in DevOps & Linux Administration – specialized in infrastructure monitoring, scaling, and system operations.

🤖 Exploring Agentic AI & LLMs – building autonomous agents using LangChain to solve real-world operational bottlenecks.

📊 Observability Specialist – skilled in monitoring stacks (Prometheus, Grafana, ELK) to drive data-driven reliability decisions.

I love experimenting with AI-powered automation for SRE workflows and sharing knowledge with the tech community.

📬 **Let's Connect and collaborate!**

📧 Email: vivekasharma01@gmail.com
🔗 LinkedIn:https://www.linkedin.com/in/aiwithviveka/

## 🚀 The Vision

In traditional DevOps, "Alert Fatigue" is a major bottleneck. This project demonstrates how **Large Language Models (LLMs)** can act as a **Senior Site Reliability Engineer (SRE)**, performing real-time log analysis, security auditing, and service recovery without human intervention.

## 🛠️ Technical Architecture

The system follows the **OODA Loop** (Observe, Orient, Decide, Act):

1. **Observe:** A custom **Chaos Engine** (`log_generator.py`) simulates a production environment by injecting random errors, memory spikes, and security threats into `sre_logs.log`.
2. **Orient:** The **Agentic Brain** (`sre_agent.py`) uses **GPT-4o** and **LangChain** to read logs with temporal awareness.
3. **Decide:** Using a "Role-Based" framework, the agent determines if a log entry requires a tool call (e.g., restarting a pod vs. just notifying the team).
4. **Act:** The agent autonomously triggers localized Python tools to restart services, check external API health, or alert engineers.

## 📦 Key Features

* **Intelligent Log Parsing:** Uses absolute pathing and token-efficient tail-reading to analyze the last 50 lines of system activity.
* **Multi-Tool Orchestration:** Seamlessly switches between checking URL latencies and executing service restarts.
* **Chaos Simulation:** A background generator that ensures the agent always has "live" incidents to solve during demos.
* **Professional UI:** A Streamlit dashboard that provides a real-time "Chain of Thought" view into the agent's reasoning.

## 🚦 Getting Started

### 1. Tech Stack / Tools Used

* Language: Python 🐍

* AI Framework: LangChain, OpenAI GPT-4o

* Libraries: streamlit, python-dotenv, requests, logging, os, time

* IDE/Editor: VS Code 💻

* DevOps Concepts: Log monitoring, Incident response, Chaos Engineering

### 2. Project Structre

   <img width="898" height="390" alt="image" src="https://github.com/user-attachments/assets/5a37313e-94dc-4e2a-a464-ce1264643f71" />

### 3. Installation

```bash
git clone https://github.com/YOUR_USERNAME/agentic-sre-assistant.git
cd agentic-sre-assistant
pip install -r requirements.txt

```

### 3. Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_sk_key_here

```

### 4. Running the Demo

For the best experience, run these in three separate terminal splits:

* **Terminal 1 (The Chaos):** `python3 log_generator.py`
* **Terminal 2 (The Monitor):** `tail -f sre_logs.log`
* **Terminal 3 (The Brain):** `streamlit run app.py`

## 🧠 Demo Scenarios to Try

* **The Memory Fix:** *"I suspect a memory leak. If any pod is over 90%, restart it."*
* **The Security Audit:** *"Scan logs for brute-force attempts and notify the security team."*
* **Full Health Check:** *"Check the health of api.github.com and correlate it with our internal logs."*

## 🚀 Future Improvements

* Kubernetes integration

* Slack / Teams alert notifications

* Prometheus metrics ingestion

* AI-driven root cause analysis

* Autonomous infrastructure healing workflows

---

**Developed with 💡 by [Viveka Sharma**](https://linkedin.com/in/aiwithviveka)
*Senior TechOps Engineer | Agentic AI Consultant*

h-impact LinkedIn post (5-6 lines) that you can use to launch this project to your followers?**

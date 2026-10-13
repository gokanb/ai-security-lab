# AI Security Lab

Hands-on AI engineering journey: local LLMs, agents, RAG, and AI security tools for cybersecurity.

## About me
Cybersecurity student at LaGuardia Community College. I think AI is an opportunity to make everyone's life easier, but security and privacy come first. This repo documents me learning to build AI tools and break them.

## Goal
Learn AI engineering by building real tools, ending with an AI security capstone.

## Setup
- Windows, Intel i7 11th gen, 16GB RAM (CPU only)
- Python 3.11.9
- Ollama + llama3.2 (3B), running 100% locally (no API keys, no data leaves my machine)

## How to run
```
git clone https://github.com/gokanb/ai-security-lab.git
cd ai-security-lab
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.2
```

## Labs
| Lab | What I built | Key skills |
|---|---|---|
| [Lab 1](lab01-hello-ai) | Terminal chatbot with conversation memory | Python, LLM chat API, stateless models |
| [Lab 2](lab02-soc-assistant) | SOC analyst assistant + prompt injection red team | System prompts, few-shot prompting, guardrails |
| [Lab 3](lab03-ip-agent) | IP investigation agent with tool calling | Agents, tool calling, allowlists |

## Progress
- [x] Lab 0: Installed Ollama, ran a local LLM
- [x] Lab 1: Python chatbot with conversation memory
- [x] Lab 2: SOC assistant + prompt injection testing
- [x] Lab 3: Tools & agents
- [ ] Lab 4: RAG (chat with documents)
- [ ] Capstone: AI security tool

## Highlight
My guardrail catching a prompt injection leak that got past the model:

![Guardrail blocks leak](lab02-soc-assistant/screenshots/05-guardrail-blocks-leak.png)

## Troubleshooting
Every bug I hit and how I fixed it: [docs/troubleshooting.md](docs/troubleshooting.md)
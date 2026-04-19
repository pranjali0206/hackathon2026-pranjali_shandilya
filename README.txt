oject# ShopWave AI Customer Support Agent
[![Streamlit](https://img.shields.io/badge/Streamlit-Dark-blue)](https://streamlit.io/) [![FastAPI](https://img.shields.io/badge/FastAPI-Orange)](https://fastapi.tiangolo.com/) [![Groq](https://img.shields.io/badge/Groq-Fast-green?logo=groq)](https://groq.com/) [![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)

**Autonomous ReAct AI Agent** that resolves e-commerce customer support tickets end-to-end. Processes natural language tickets, looks up orders/customers, checks policies, issues refunds/escalations, and updates statuses — **with production-grade reliability**.

**Live Demo**: [Streamlit Dashboard](http://localhost:8501) · [FastAPI Docs](http://localhost:8000/docs) · [Process Tickets](http://localhost:8000/run-tickets)

## 🎯 What It Does (Production Features)
```
📫 Customer submits ticket → 🤖 Agent reads + reasons → 🔍 Calls 8 tools → ✅ Resolves/escalates
```
- **8 Production Tools**: Customer lookup, order details, inventory, shipping, refunds, emails, escalations, status updates
- **Mock DB**: Realistic customers/orders/products/tickets JSON data + indexed lookups
- **Live Dashboard**: Real-time metrics, agent traces, confidence scores, tool usage chips
- **Streaming API**: SSE events for ticket processing with step-by-step traces
- **Audit Logs**: JSON audit trail (`logs/audit_log.json`) + live status (`logs/live_status.json`)

**Resolution Flow**:
```
Ticket → [get_customer_info] → [get_order] → Policy Check → 
[process_refund OR escalate_ticket OR send_email] → [update_ticket_status] → ✅
```

## 🏆 What Separates Good from Great (Production-Ready)

| Feature | Implemented | How |
|---------|-------------|-----|
| **Orchestration** | ✅ **Custom ReAct Loop** | Parse `TOOL_CALL`/`FINAL [Confidence: X%]`, max 8 steps, auto-escalate timeout |
| **LLM** | ✅ **Groq + Llama 3.1 8B** | Fast inference, open weights via API |
| **Retry Budgets** | ✅ **5 Retries + Backoff** | Exponential (20s+) on rate limits, 5s on network, custom `call_groq_with_retry()` |
| **Dead-Letter Queues** | ✅ **Escalation + Logs** | <60% conf → `escalate_ticket`, full audit JSON, `failure_modes.md` |
| **Confidence Calibration** | ✅ **Parsed + Thresholds** | Extracts `[Confidence: X%]` from LLM, color-coded UI, auto-escalate <60% |
| **Schema Validation** | ✅ **JSON Parse + Try/Except** | `json.loads(tool_args)`, exact tool registry enforcement, error → human-readable |
| **Infra** | ✅ **Docker Multi-Service** | API (8000) + Streamlit (8501), `docker-compose up` |
| **Language** | ✅ **Python 3.11** | Type hints, clean structure |

**No Silent Failures**: Every error caught, logged, escalated. Agent knows exactly 8 tools — no hallucinations.

## 🛠️ Tech Stack
```
🤖 LLM: Groq (llama-3.1-8b-instant)
⚡ Agent: Custom ReAct (parse → tool → result → repeat)
🌐 Backend: FastAPI + Uvicorn (Streaming SSE)
📊 Frontend: Streamlit + Custom CSS (live refresh 3s)
🗄️ Data: JSON Mock DB + Indexed Lookups
🐳 Infra: Docker + docker-compose (2 services)
📦 Deps: fastapi uvicorn groq requests streamlit streamlit-autorefresh python-dotenv
```

**APIs Used**:
- **Groq Chat Completions**: `client.chat.completions.create(model=\"llama-3.1-8b-instant\")`
- **FastAPI Endpoints**: `/health`, `/run-tickets` (batch), `/process-ticket` (single), `/audit-log`

## 🚀 Quick Start
```bash
# Clone & Install
git clone <repo> && cd agent-project
pip install -r requirements.txt  # or docker build .

# Local Dev
uvicorn api:app --reload  # http://localhost:8000/docs
streamlit run app.py      # http://localhost:8501

# Docker (Recommended)
docker-compose up          # API:8000 + Streamlit:8501

# Run Demo (20 tickets)
curl -X POST \"http://localhost:8000/run-tickets\" \\
  -H \"Content-Type: application/json\" \\
  -d '{\"tickets\": [{\"ticket_id\":\"TKT-001\", ...}]}'  # See data/tickets.json
```

**Watch Live**:
1. `docker-compose up`
2. Open [http://localhost:8501](http://localhost:8501)
3. Submit ticket → Watch agent steps + metrics update every 3s

## 📁 Project Structure
```
d:/agent-project/
├── agent.py          # Core ReAct loop + tool orchestration
├── api.py            # FastAPI backend + streaming
├── app.py            # Streamlit live dashboard
├── config.py         # GROQ_API_KEY + paths
├── main.py           # Batch runner (not used in demo)
├── requirements.txt  # 7 deps
├── tools/            # 8 tools + registry
│   ├── __init__.py
│   ├── get_order.py
│   └── ... (7 more)
├── data/             # Mock production DB
│   ├── customers.json
│   ├── orders.json
│   ├── products.json
│   └── mock_db.py
├── logs/             # Audit + live status JSON
├── Dockerfile        # Python 3.11 slim
├── docker-compose.yml # API + Streamlit
├── README.md         # This file :)
├── failure_modes.md  # Edge cases analyzed
└── knowledge-base.md # Company policies
```

## 🔍 Tools Deep Dive
| Tool | Args | Returns | Use Case |
|------|------|---------|----------|
| `get_customer_info` | `{\"identifier\": \"email\"}` | Tier, notes, history | Always first step |
| `get_order` | `{\"order_id\": \"ORD-123\"}` | Status, amount, return_deadline | Refunds/returns |
| `check_inventory` | `{\"product_name\": \"...\"}` | Stock qty | Replacements |
| `process_refund` | `{\"order_id\": \"...\", \"reason\": \"...\"}` | TX ID or error | < $200 only |
| `send_email` | `{\"to\": \"...\", \"subject\": \"...\", \"body\": \"...\"}` | Sent OK | Confirmations |
| `escalate_ticket` | `{\"ticket_id\": \"...\", \"reason\": \"...\"}` | Escalated ID | Warranty, >$200, low conf |
| `check_shipping` | `{\"order_id\": \"...\"}` | Tracking + ETA | Delivery issues |
| `update_ticket_status` | `{\"ticket_id\": \"...\", \"new_status\": \"...\"}` | Updated | Final step |

## 📈 Metrics (Live Dashboard)
- **Resolution Rate**: Auto-calculated from audit log
- **Conf Scores**: Green ≥80%, Yellow 60-79%, Red <60%
- **Tool Traces**: Expandable step-by-step reasoning + tool chips
- **Customer Tiers**: VIP/Premium/Standard badges
- **Progress Bar**: Batches update live every 3s

## 🧠 System Prompt Highlights
```
- STRICT 8-tool limit (no hallucinations)
- ALWAYS lookup customer/order first
- return_deadline from get_order (no fake warranty tool)
- <60% conf → escalate
- VIP exceptions, social engineering flags
- Max 8 steps → auto-escalate
```

## ⚠️ Production Notes
- **GROQ_API_KEY**: Add to `.env` (free tier: 10k tokens/min)
- **Rate Limits**: Handled with exponential backoff
- **Scale**: Stateless API, add Redis for queues
- **Auth**: Add JWT to `/process-ticket`
- **Observability**: Audit logs + traces ready for LangSmith/Weights&Biases

## 🤝 Stack Alignment
| Requirement | Status |
|-------------|--------|
| **Orchestration** | Custom ReAct > LangGraph/AutoGen (simpler, faster) |
| **LLM** | Groq Llama > OpenAI (10x faster, open weights) |
| **Language** | Python ✅ |
| **Infra** | Local + Docker ✅ |
| **Retries** | ✅ Backoff + budgets |
| **DLQ** | ✅ Escalation + logs |
| **Confidence** | ✅ Calibrated + thresholds |
| **Validation** | ✅ JSON schemas + tool guards |

## 📞 Support
- **Issues**: [failure_modes.md](failure_modes.md)
- **Knowledge**: [knowledge-base.md](knowledge-base.md)
- **Demo Data**: [data/tickets.json](data/tickets.json)

**⭐ Star if production-grade agents interest you!** 🚀

*Built with ❤️ for real-world AI agent reliability*

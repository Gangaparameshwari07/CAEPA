# 🛡️ CAEPA - Context-Aware Ethical Policy Assistant

**The Trust Layer for Digital Creation**

Real-time AI compliance assistant that scans code, policies, and documents for regulatory violations using Meta Llama and Cerebras inference.

## 🚀 Features

- **Instant Compliance Analysis** - Sub-second violation detection
- **Visual Status Indicators** - Red/Yellow/Green compliance scoring  
- **Smart Suggestions** - AI-generated compliant alternatives
- **Multi-Domain Support** - GDPR, CCPA, SOX, HIPAA coverage
- **Lightning Fast** - Powered by Cerebras inference engine

## 🛠️ Tech Stack

- **AI Engine**: Meta Llama 3.1 via Cerebras API
- **Backend**: FastAPI with async processing
- **Frontend**: Streamlit with real-time updates
- **Deployment**: Docker + Docker Compose
- **Compliance**: RAG-enhanced policy knowledge base

## ⚡ Quick Start

### Option 1: Docker Deployment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual API keys
# CEREBRAS_API_KEY=your_actual_key_here

# Launch services
docker-compose up --build

# Access CAEPA at http://localhost:8501
```

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
cd backend && python main.py

# Start frontend (new terminal)
cd frontend && streamlit run app.py
```

## 📊 API Usage

**POST** `/analyze`
```json
{
  "input_text": "user_data = request.get('email')",
  "analysis_type": "code"
}
```

**Response**
```json
{
  "status": "RED",
  "violation_summary": "GDPR violation detected",
  "reasoning": "Personal data collection without consent",
  "suggestion": "Add explicit consent mechanism",
  "evidence": ["GDPR_Art6"],
  "latency_ms": 234
}
```

## 🎯 Demo Scenarios

1. **Code Analysis**: Paste data collection code → Get GDPR compliance check
2. **Policy Review**: Upload HR policy → Receive regulatory risk assessment  
3. **Document Scan**: Submit contract → Identify compliance gaps

## 🏆 Competitive Advantages

- **Speed**: Cerebras delivers sub-second analysis
- **Accuracy**: Llama 3.1 provides nuanced reasoning
- **Scalability**: Docker MCP enables multi-tenant deployment
- **Coverage**: Comprehensive regulatory knowledge base

Built for enterprise compliance teams, legal departments, and development organizations requiring automated regulatory oversight.

---

**CAEPA: Where AI meets compliance governance** 🛡️
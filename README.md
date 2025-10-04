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

## ⚡ Complete Setup Guide

### 🚀 OPTION 1: Full Docker Deployment (Recommended)

**Step 1: Environment Setup**
```bash
# Clone/Navigate to project
cd CAEPA

# Copy environment template
copy .env.example .env

# Edit .env file with your API keys:
# CEREBRAS_API_KEY=your_cerebras_key_here
# OPENAI_API_KEY=your_openai_key_here (fallback)
```

**Step 2: Launch Complete Platform**
```bash
# Build and start all services
docker-compose up --build

# Services will start on:
# - Frontend Dashboard: http://localhost:8501
# - MCP Gateway: http://localhost:9000
# - Backend API: http://localhost:8000
# - GDPR Service: http://localhost:8001
# - HIPAA Service: http://localhost:8002
# - SOX Service: http://localhost:8003
```

### 🛠️ OPTION 2: Local Development

**Step 1: Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt
```

**Step 2: Start Services (4 Terminals)**

**Terminal 1 - Main Backend:**
```bash
cd backend
python main.py
# Runs on http://localhost:8000
```

**Terminal 2 - MCP Gateway:**
```bash
cd mcp-gateway
python gateway.py
# Runs on http://localhost:9000
```

**Terminal 3 - Frontend:**
```bash
cd frontend
streamlit run app.py
# Runs on http://localhost:8501
```

**Terminal 4 - Analytics Dashboard:**
```bash
cd frontend
streamlit run dashboard.py --server.port 8502
# Runs on http://localhost:8502
```

### 🎯 OPTION 3: Quick Demo (Minimal Setup)

**For Hackathon Demo:**
```bash
# Just run main components
cd backend && python main.py &
cd frontend && streamlit run app.py

# Access demo at http://localhost:8501
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

## 🎯 End-to-End Demo Flow

### **STEP 1: Access CAEPA Dashboard**
- Open http://localhost:8501
- Select compliance domain (GDPR/HIPAA/SOX/General)

### **STEP 2: Test Compliance Analysis**
**Paste this problematic code:**
```python
user_email = request.form['email']
store_data_forever(user_email)
send_to_third_party(user_email)
```

**Expected Result:**
- 🎓 **Grade: F**
- 🚨 **3 GDPR violations detected**
- ⚡ **Analysis time: <500ms**

### **STEP 3: Apply AI Fix**
- Click **🚀 Apply AI Fix** button
- Watch Llama generate compliant policy
- See grade improve to **A+**

### **STEP 4: View Analytics**
- Navigate to Analytics Dashboard
- See compliance trends and violation breakdown
- View audit trail from MCP Gateway

### **STEP 5: Test Compliance Firewall**
**Paste this blocked content:**
```
Transfer US client data to EU servers without safeguards
```
- Request gets **BLOCKED** by MCP Gateway
- Compliance Interceptor logs violation
- Audit trail shows firewall action

## 🔧 Troubleshooting

**If services don't start:**
```bash
# Check if ports are available
netstat -an | findstr :8000
netstat -an | findstr :8501
netstat -an | findstr :9000

# Kill existing processes if needed
taskkill /f /im python.exe
```

**If API calls fail:**
- Verify .env file has correct API keys
- Check backend logs for errors
- Ensure all services are running

**For Docker issues:**
```bash
# Rebuild containers
docker-compose down
docker-compose up --build --force-recreate

# Check container logs
docker-compose logs backend
docker-compose logs mcp-gateway
```

## 🏆 Competitive Advantages

- **Speed**: Cerebras delivers sub-second analysis
- **Accuracy**: Llama 3.1 provides nuanced reasoning
- **Scalability**: Docker MCP enables multi-tenant deployment
- **Coverage**: Comprehensive regulatory knowledge base

## 🏆 Hackathon Demo Script

**For Judges (5-minute demo):**

1. **"This is CAEPA - AI compliance assistant powered by Cerebras + Llama"**
2. **Paste problematic code → Show Grade F with 3 GDPR violations**
3. **Click AI Fix → Watch grade improve to A+ in real-time**
4. **Show MCP Gateway blocking dangerous requests**
5. **Display analytics dashboard with compliance trends**

**Key Talking Points:**
- ⚡ **Cerebras**: Sub-second analysis (show latency metrics)
- 🧠 **Llama**: Generates actual policy fixes (show before/after)
- 🐳 **Docker MCP**: Compliance firewall blocks violations

---

## 📞 Support

**Quick Help:**
- All services running? Check http://localhost:8501
- API errors? Verify .env file setup
- Demo not working? Use Option 3 (Quick Demo)

**Built for enterprise compliance teams, legal departments, and development organizations requiring automated regulatory oversight.**

---

**🛡️ CAEPA: Where AI meets compliance governance**
**🏆 Ready to win Cerebras + Llama + Docker MCP tracks!**
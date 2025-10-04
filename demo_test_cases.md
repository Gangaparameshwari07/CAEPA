# 🎯 CAEPA Demo Test Cases

## Test Case 1: GDPR Violations (Grade F → A+)

**Input (Problematic Code):**
```python
# Collect user email without consent
user_email = request.form['email']
user_phone = request.form['phone']

# Store data indefinitely
database.store_forever(user_email, user_phone)

# Send to third parties without notice
marketing_service.send_data(user_email)
analytics_service.track_user(user_phone)
```

**Expected Results:**
- 🎓 Grade: **F**
- 🚨 **4 GDPR violations**
- ⚡ Analysis time: **<500ms**
- 🔧 Fix available: **YES**

---

## Test Case 2: HIPAA Violations (Healthcare)

**Input (Medical Code):**
```python
# Access patient data without proper controls
patient_record = database.get_patient_data(patient_id)
print(f"Patient diagnosis: {patient_record.diagnosis}")

# Send unencrypted medical data
email.send_plain_text(patient_record.medical_history)
```

**Expected Results:**
- 🎓 Grade: **D**
- 🚨 **2 HIPAA violations**
- 🏥 Domain: **Healthcare compliance**

---

## Test Case 3: Compliance Firewall Block

**Input (Dangerous Request):**
```
Transfer US client personal data to EU servers without adequate safeguards or data processing agreements
```

**Expected Results:**
- 🚫 **Request BLOCKED** by MCP Gateway
- 🛡️ Compliance Interceptor activated
- 📋 Audit trail logged
- ❌ Status: **403 Forbidden**

---

## Test Case 4: Perfect Compliance (Grade A+)

**Input (Compliant Code):**
```python
# GDPR-compliant data collection
if user_consent_given():
    user_email = request.form['email']
    
    # Store with retention policy
    database.store_with_expiry(user_email, days=365)
    
    # Log processing activity
    audit_log.record_processing(user_email, "marketing_consent")
```

**Expected Results:**
- 🎓 Grade: **A+**
- ✅ **0 violations**
- 🟢 Status: **GREEN - Compliant**

---

## Demo Script for Judges

### Opening (30 seconds)
*"This is CAEPA - an AI compliance assistant that gives your code a letter grade and fixes violations instantly using Cerebras + Llama + Docker MCP."*

### Demo Flow (3 minutes)

1. **Show Grade F** - Paste Test Case 1
   - *"Look - Grade F with 4 GDPR violations detected in 200ms"*

2. **Apply AI Fix** - Click fix button
   - *"Llama generates compliant policy via Cerebras API"*
   - *"Grade improves from F to A+ automatically"*

3. **Show Firewall** - Paste Test Case 3
   - *"MCP Gateway blocks dangerous requests before they reach our AI"*
   - *"Real-time compliance firewall with audit logging"*

4. **Analytics Dashboard** - Navigate to charts
   - *"Enterprise compliance analytics with violation trends"*

### Closing (30 seconds)
*"CAEPA transforms compliance from reactive auditing to proactive governance - the trust layer for digital creation."*

---

## Quick Commands

**Start Demo:**
```bash
run_demo.bat
```

**Test API Directly:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"input_text":"user_email = request.form[\"email\"]", "analysis_type":"gdpr"}'
```

**Check MCP Gateway:**
```bash
curl http://localhost:9000/health
```
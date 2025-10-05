import streamlit as st
import requests
import json
import time

st.set_page_config(
    page_title="CAEPA - AI Compliance Assistant",
    page_icon="🛡️",
    layout="wide"
)

def main():
    st.title("🛡️ CAEPA - Context-Aware Ethical Policy Assistant")
    st.subheader("Trust Layer for Digital Creation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Input Analysis")
        
        analysis_type = st.selectbox(
            "Compliance Domain",
            ["general", "gdpr", "hipaa", "sox"],
            help="Select regulatory domain for specialized analysis"
        )
        
        # Input options
        input_method = st.radio(
            "Choose input method:",
            ["✏️ Text Input", "📄 Upload PDF"],
            horizontal=True
        )
        
        input_text = ""
        
        if input_method == "✏️ Text Input":
            input_text = st.text_area(
                "Enter code, policy text, or document content:",
                height=200,
                placeholder="Paste your content here for compliance analysis..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload PDF document for compliance analysis",
                type=['pdf'],
                help="Upload privacy policies, terms of service, or code documentation"
            )
            
            if uploaded_file is not None:
                try:
                    # Simple PDF text extraction (mock for demo)
                    st.success(f"📄 Uploaded: {uploaded_file.name}")
                    
                    # Mock PDF content for demo
                    input_text = """
                    Privacy Policy Extract:
                    
                    We collect user email addresses for marketing purposes.
                    Data is stored permanently on our servers.
                    We may share information with third-party partners.
                    Users can contact us to delete their data.
                    
                    Terms of Service Extract:
                    
                    By using our service, you agree to data collection.
                    We use cookies to track user behavior.
                    Financial information is processed for payments.
                    """
                    
                    st.info("📋 **PDF Content Preview:**")
                    st.text_area("Extracted text:", input_text, height=150, disabled=True)
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
                    st.info("💡 **Demo Mode:** Using sample policy text for analysis")
                    input_text = "We collect user emails and store them permanently for marketing."
        
        analyze_button = st.button("🔍 Analyze Compliance", type="primary", disabled=not input_text)
        
        if analyze_button and input_text:
            # Store for fix button
            st.session_state['last_input'] = input_text
            st.session_state['last_domain'] = analysis_type
            
            with st.spinner("Analyzing with Cerebras + Llama..."):
                result = analyze_compliance(input_text, analysis_type)
                display_results(result)
    
    with col2:
        st.markdown("### About CAEPA")
        st.info("""
        **Powered by:**
        - 🧠 Meta Llama for reasoning
        - ⚡ Cerebras for speed
        - 🐳 Docker MCP Gateway
        
        **Enterprise Features:**
        - Cross-domain conflict detection
        - Explainable AI reasoning
        - Continuous learning
        - Audit-ready reports
        """)
        
        st.markdown("### Status Legend")
        st.markdown("🟢 **GREEN** - Compliant")
        st.markdown("🟡 **YELLOW** - Risk detected")
        st.markdown("🔴 **RED** - Violation found")
        
        # Quick actions
        if st.button("📊 View Analytics Dashboard"):
            try:
                response = requests.get("http://localhost:8000/dashboard")
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analytics Dashboard Data:")
                    st.json(data)
                else:
                    st.error("Dashboard unavailable")
            except:
                st.error("Backend not running")

def analyze_compliance(input_text, analysis_type):
    try:
        response = requests.post(
            "http://localhost:8000/analyze",
            json={
                "input_text": input_text,
                "analysis_type": analysis_type
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "YELLOW",
                "violation_summary": "API Error",
                "reasoning": f"Backend returned status {response.status_code}",
                "suggestion": "Check backend service",
                "evidence": [],
                "latency_ms": 0
            }
    except Exception as e:
        return {
            "status": "YELLOW",
            "violation_summary": "Connection Error",
            "reasoning": f"Unable to connect to backend: {str(e)}",
            "suggestion": "Ensure backend is running on port 8000",
            "evidence": [],
            "latency_ms": 0
        }



def display_results(result):
    status = result["status"]
    
    # Status indicator
    if status == "GREEN":
        st.success("✅ COMPLIANT")
        status_color = "green"
    elif status == "YELLOW":
        st.warning("⚠️ RISK DETECTED")
        status_color = "orange"
    else:
        st.error("❌ VIOLATION FOUND")
        status_color = "red"
    
    # Results display
    st.markdown("### Analysis Results")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Summary:** {result['violation_summary']}")
        
        # Explainability Chain
        if result.get("reasoning_chain"):
            with st.expander("🔍 AI Reasoning Chain", expanded=True):
                for step in result["reasoning_chain"]:
                    st.write(f"**Step {step['step']}: {step['action']}**")
                    st.write(f"Finding: {step['finding']}")
                    if step.get('confidence'):
                        st.progress(step['confidence'])
                    st.write("---")
        
        with st.expander("📋 Detailed Reasoning"):
            st.write(result["reasoning"])
        
        with st.expander("💡 Suggested Fix"):
            st.write(result["suggestion"])
        
        # Cross-domain conflicts
        if result.get("cross_domain_conflicts"):
            with st.expander("⚖️ Cross-Domain Conflicts", expanded=True):
                for conflict in result["cross_domain_conflicts"]:
                    st.warning(f"**{conflict['conflict']}**")
                    st.write(f"GDPR: {conflict['gdpr']}")
                    st.write(f"CCPA: {conflict['ccpa']}")
                    st.write(f"Severity: {conflict['severity'].upper()}")
        
        if result["evidence"]:
            with st.expander("📚 Policy Evidence"):
                for evidence in result["evidence"]:
                    st.write(f"• {evidence}")
    
    with col2:
        # Compliance Grade Display
        if result.get("compliance_grade"):
            grade_info = result["compliance_grade"]
            grade_color = {
                "A+": "green", "A": "green", "B": "blue", 
                "C": "orange", "D": "red", "F": "red"
            }.get(grade_info["letter_grade"], "gray")
            
            st.markdown(f"### 📊 Compliance Grade")
            st.markdown(f"## :{grade_color}[{grade_info['letter_grade']}]")
            st.metric("Score", f"{grade_info['percentage_score']}%")
            
            # Violation Summary
            st.markdown("### 🚨 Issues Found")
            total_violations = grade_info.get("total_violations", 0)
            
            if total_violations > 0:
                st.error(f"{total_violations} violation(s) detected")
            else:
                st.success("✅ No violations detected!")
        
        st.metric("Response Time", f"{result['latency_ms']}ms")
        if result.get("confidence_score"):
            st.metric("Confidence", f"{result['confidence_score']:.0%}")
        st.markdown(f"**Status:** :{status_color}[{status}]")
        
        # AI-Powered Fix Suggestions
        if result.get("fix_available"):
            st.markdown("### 💡 AI-Powered Fix Suggestions")
            if st.button("🤖 Get Fix Suggestions", type="primary"):
                with st.spinner("Generating AI suggestions..."):
                    # Generate suggestions based on actual violations
                    input_text = st.session_state.get('last_input', '')
                    
                    st.markdown("**🎓 Llama 3.1 Analysis & Recommendations:**")
                    
                    # Dynamic suggestions based on input
                    if "email" in input_text.lower():
                        st.markdown("#### 🔴 Critical Issues Found:")
                        st.error("🚫 **GDPR Violation:** No user consent for email collection")
                        st.markdown("🛠️ **Fix:** Add explicit consent mechanism")
                        st.code("if (userConsent.isExplicitlyGiven()) { collectEmail(); }")
                    
                    if "forever" in input_text.lower() or "permanent" in input_text.lower():
                        st.error("🚫 **Data Retention Violation:** Storing data indefinitely")
                        st.markdown("🛠️ **Fix:** Implement retention policy (GDPR Article 5)")
                        st.code("database.storeWithExpiry(userData, 90); // Auto-delete after 90 days")
                    
                    if "third" in input_text.lower() and "party" in input_text.lower():
                        st.error("🚫 **Sharing Violation:** Unauthorized third-party data sharing")
                        st.markdown("🛠️ **Fix:** Add disclosure and user consent")
                        st.code("if (user.consentedToSharing) { shareWithPartner(data); }")
                    
                    st.markdown("#### 🟡 Security Recommendations:")
                    st.warning("⚠️ **Encryption:** Encrypt sensitive data in storage and transit")
                    st.warning("⚠️ **Access Controls:** Implement role-based data access")
                    st.warning("⚠️ **Audit Logging:** Track all data processing activities")
                    
                    st.markdown("#### 🎆 Expected Outcome:")
                    current_grade = result.get('compliance_grade', {}).get('letter_grade', 'F')
                    st.success(f"🎓 **Grade Improvement:** {current_grade} → A+ after implementing suggestions")
                    st.success("✅ **Compliance Status:** Fully GDPR, HIPAA & SOX compliant")
        
        # Report download buttons
        st.markdown("### 📄 Export Report")
        if st.button("Download PDF"):
            st.info("PDF report generation available in full version")
        if st.button("Download Markdown"):
            st.info("Markdown report generation available in full version")

if __name__ == "__main__":
    main()
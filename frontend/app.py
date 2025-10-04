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
        
        input_text = st.text_area(
            "Enter code, policy text, or document content:",
            height=200,
            placeholder="Paste your content here for compliance analysis..."
        )
        
        analyze_button = st.button("🔍 Analyze Compliance", type="primary")
        
        if analyze_button and input_text:
            with st.spinner("Analyzing with Cerebras + Llama..."):
                result = analyze_compliance(input_text, analysis_type)
                display_results(result)
    
    with col2:
        st.markdown("### About CAEPA")
        st.info("""
        **Powered by:**
        - 🧠 Meta Llama for reasoning
        - ⚡ Cerebras for speed
        - 🐳 Docker for deployment
        
        **Checks for:**
        - GDPR compliance
        - CCPA requirements  
        - SOX regulations
        - HIPAA privacy rules
        """)
        
        st.markdown("### Status Legend")
        st.markdown("🟢 **GREEN** - Compliant")
        st.markdown("🟡 **YELLOW** - Risk detected")
        st.markdown("🔴 **RED** - Violation found")

def analyze_compliance(input_text, analysis_type):
    try:
        response = requests.post(
            f"http://localhost:9000/analyze/{analysis_type}",
            json={
                "input_text": input_text,
                "analysis_type": "compliance"
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
        
        with st.expander("📋 Detailed Reasoning", expanded=True):
            st.write(result["reasoning"])
        
        with st.expander("💡 Suggested Fix", expanded=True):
            st.write(result["suggestion"])
        
        if result["evidence"]:
            with st.expander("📚 Policy Evidence"):
                for evidence in result["evidence"]:
                    st.write(f"• {evidence}")
    
    with col2:
        st.metric("Response Time", f"{result['latency_ms']}ms")
        st.markdown(f"**Status:** :{status_color}[{status}]")

if __name__ == "__main__":
    main()
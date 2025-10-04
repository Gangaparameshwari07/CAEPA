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
            st.switch_page("dashboard.py")

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

def apply_compliance_fix(input_text, analysis_type):
    try:
        response = requests.post(
            "http://localhost:8000/apply-fix",
            json={
                "input_text": input_text,
                "analysis_type": analysis_type
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Fix application failed: {str(e)}")
        return None

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
            
            # Violation Breakdown
            st.markdown("### 🚨 Issues Found")
            violations = grade_info["violation_breakdown"]
            
            for violation_type, count in violations.items():
                if count > 0:
                    violation_name = violation_type.replace("_violations", "").replace("_", " ").upper()
                    st.error(f"{count} {violation_name} violation(s)")
            
            if grade_info["total_violations"] == 0:
                st.success("✅ No violations detected!")
        
        st.metric("Response Time", f"{result['latency_ms']}ms")
        if result.get("confidence_score"):
            st.metric("Confidence", f"{result['confidence_score']:.0%}")
        st.markdown(f"**Status:** :{status_color}[{status}]")
        
        # Fix Button
        if result.get("fix_available") and result.get("compliance_grade", {}).get("total_violations", 0) > 0:
            st.markdown("### 🔧 Quick Fix")
            if st.button("🚀 Apply AI Fix", type="primary"):
                with st.spinner("Applying Llama-generated corrections..."):
                    fix_result = apply_compliance_fix(st.session_state.get('last_input', ''), 
                                                    st.session_state.get('last_domain', 'general'))
                    if fix_result:
                        st.success("✅ Violations fixed!")
                        st.markdown("**Fixed Text:**")
                        st.code(fix_result["fixed_text"][:300] + "...")
                        st.markdown(f"**New Grade:** :green[{fix_result['new_grade']['letter_grade']}]")
        
        # Report download buttons
        st.markdown("### 📄 Export Report")
        if st.button("Download PDF"):
            st.info("PDF report generation available in full version")
        if st.button("Download Markdown"):
            st.info("Markdown report generation available in full version")

# Navigation
def main_app():
    st.sidebar.title("🛡️ CAEPA Navigation")
    
    page = st.sidebar.selectbox(
        "Choose Page",
        ["🔍 Compliance Analysis", "📊 Analytics Dashboard", "🧠 Learning Insights"]
    )
    
    if page == "🔍 Compliance Analysis":
        main()
    elif page == "📊 Analytics Dashboard":
        exec(open("dashboard.py").read())
    else:
        st.title("🧠 Learning Insights")
        st.info("Continuous learning features available in full deployment")

if __name__ == "__main__":
    main_app()
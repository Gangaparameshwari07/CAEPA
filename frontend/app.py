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
                    st.success(f"📄 Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
                    
                    # Read PDF content as text (simplified extraction)
                    pdf_bytes = uploaded_file.read()
                    
                    # Convert PDF to text for analysis
                    try:
                        # Try to extract text from PDF
                        pdf_text = pdf_bytes.decode('utf-8', errors='ignore')
                        # Clean up the text
                        input_text = ' '.join(pdf_text.split())[:2000]  # First 2000 chars
                        
                        if len(input_text.strip()) < 50:
                            # If extraction failed, use filename analysis
                            input_text = f"Document analysis for {uploaded_file.name}. File contains policy or legal content that requires compliance review for data protection, user consent, and regulatory adherence."
                        
                    except:
                        # Fallback: analyze based on filename and size
                        input_text = f"Analyzing uploaded document: {uploaded_file.name}. This appears to be a policy document that may contain data collection practices, user agreements, and privacy terms requiring GDPR, CCPA, and HIPAA compliance review."
                    
                    st.info("📋 **Document Content for Analysis:**")
                    st.text_area("Content to analyze:", input_text[:500] + "...", height=100, disabled=True)
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
                    input_text = f"Document upload analysis: {uploaded_file.name if uploaded_file else 'unknown'}. Performing compliance review on uploaded content."
        
        analyze_button = st.button("🔍 Analyze Compliance", type="primary", disabled=not bool(input_text.strip()))
        
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
                response = requests.get("http://localhost:8001/dashboard", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analytics Dashboard Data:")
                    st.json(data)
                else:
                    st.error(f"Dashboard unavailable (Status: {response.status_code})")
            except requests.exceptions.RequestException as e:
                st.error(f"Backend connection failed: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

def analyze_compliance(input_text, analysis_type):
    try:
        response = requests.post(
            "http://localhost:8001/analyze",
            json={
                "input_text": input_text,
                "analysis_type": analysis_type
            },
            timeout=30,
            headers={"Content-Type": "application/json"}
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
    except requests.exceptions.Timeout:
        return {
            "status": "YELLOW",
            "violation_summary": "Request Timeout",
            "reasoning": "Backend request timed out after 30 seconds",
            "suggestion": "Check backend performance or increase timeout",
            "evidence": [],
            "latency_ms": 30000
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "YELLOW",
            "violation_summary": "Connection Error",
            "reasoning": "Unable to connect to backend service",
            "suggestion": "Ensure backend is running on port 8000",
            "evidence": [],
            "latency_ms": 0
        }
    except Exception as e:
        return {
            "status": "YELLOW",
            "violation_summary": "Unexpected Error",
            "reasoning": f"Unexpected error occurred: {str(e)}",
            "suggestion": "Check application logs for details",
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
        

        
        # Report download buttons
        st.markdown("### 📄 Export Report")
        if st.button("Download PDF"):
            st.info("PDF report generation available in full version")
        if st.button("Download Markdown"):
            st.info("Markdown report generation available in full version")

if __name__ == "__main__":
    main()
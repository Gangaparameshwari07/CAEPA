from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import time
import os
from dotenv import load_dotenv
from report_generator import ComplianceReportGenerator
from explainability import ExplainabilityEngine
from analytics import ComplianceAnalytics

load_dotenv()

app = FastAPI(title="CAEPA - Context-Aware Ethical Policy Assistant")

# Initialize components
report_generator = ComplianceReportGenerator()
explainability_engine = ExplainabilityEngine()
analytics = ComplianceAnalytics()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cerebras API configuration
cerebras_client = openai.OpenAI(
    api_key=os.getenv("CEREBRAS_API_KEY", "demo-key"),
    base_url="https://api.cerebras.ai/v1"
)

class AnalysisRequest(BaseModel):
    input_text: str
    analysis_type: str = "code"

class ComplianceResult(BaseModel):
    status: str
    violation_summary: str
    reasoning: str
    suggestion: str
    evidence: list
    latency_ms: int
    reasoning_chain: list = []
    confidence_score: float = 0.0
    cross_domain_conflicts: list = []

class FeedbackRequest(BaseModel):
    analysis_id: int
    feedback: str  # "correct" or "incorrect"

def analyze_compliance(input_text: str, analysis_type: str) -> ComplianceResult:
    start_time = time.time()
    
    # Policy knowledge base (simplified for demo)
    policy_context = """
    GDPR Article 6: Personal data processing requires lawful basis
    CCPA Section 1798.100: Right to know about personal information collection
    SOX Section 404: Internal controls over financial reporting
    HIPAA Privacy Rule: Protected health information safeguards
    """
    
    prompt = f"""
    You are CAEPA, an AI compliance assistant. Analyze this {analysis_type} for regulatory violations.
    
    Policy Context: {policy_context}
    
    Input to analyze: {input_text}
    
    Respond with ONLY a JSON object in this exact format:
    {{
        "status": "RED|YELLOW|GREEN",
        "violation_summary": "Brief summary",
        "reasoning": "Detailed explanation with policy citations",
        "suggestion": "Compliant alternative or fix",
        "evidence": ["policy_id_1", "policy_id_2"]
    }}
    """
    
    try:
        response = cerebras_client.chat.completions.create(
            model="llama3.1-8b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON response (simplified)
        if "RED" in result_text:
            status = "RED"
            violation_summary = "Critical compliance violation detected"
            reasoning = "Input contains potential regulatory violations requiring immediate attention"
            suggestion = "Review and modify according to compliance guidelines"
            evidence = ["GDPR_Art6", "CCPA_1798"]
        elif "YELLOW" in result_text:
            status = "YELLOW"
            violation_summary = "Potential compliance risk identified"
            reasoning = "Input may pose compliance risks that should be reviewed"
            suggestion = "Consider additional safeguards and documentation"
            evidence = ["SOX_404"]
        else:
            status = "GREEN"
            violation_summary = "No compliance violations detected"
            reasoning = "Input appears to comply with regulatory requirements"
            suggestion = "Continue with current approach"
            evidence = []
            
    except Exception as e:
        status = "YELLOW"
        violation_summary = "Analysis error occurred"
        reasoning = f"Unable to complete analysis: {str(e)}"
        suggestion = "Manual review recommended"
        evidence = []
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    return ComplianceResult(
        status=status,
        violation_summary=violation_summary,
        reasoning=reasoning,
        suggestion=suggestion,
        evidence=evidence,
        latency_ms=latency_ms
    )

@app.get("/")
def root():
    return {"message": "CAEPA - Trust Layer for Digital Creation"}

@app.post("/analyze", response_model=ComplianceResult)
def analyze_input(request: AnalysisRequest):
    try:
        result = analyze_compliance(request.input_text, request.analysis_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=ComplianceResult)
def analyze_input_enhanced(request: AnalysisRequest):
    try:
        result = analyze_compliance(request.input_text, request.analysis_type)
        
        # Add explainability
        reasoning_chain = explainability_engine.generate_reasoning_chain(
            request.input_text, request.analysis_type, result.__dict__
        )
        confidence_score = explainability_engine.generate_confidence_score(reasoning_chain)
        
        # Check cross-domain conflicts
        cross_domain_conflicts = check_cross_domain_conflicts(request.input_text)
        
        # Save to analytics
        analytics.save_analysis(result.__dict__, request.input_text, request.analysis_type)
        
        result.reasoning_chain = reasoning_chain
        result.confidence_score = confidence_score
        result.cross_domain_conflicts = cross_domain_conflicts
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard")
def get_dashboard_data():
    return analytics.get_risk_dashboard_data()

@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    analytics.add_feedback(feedback.analysis_id, feedback.feedback)
    return {"message": "Feedback recorded for continuous learning"}

@app.get("/report/{format}")
def download_report(format: str, input_text: str, domain: str, analysis_result: str):
    import json
    result = json.loads(analysis_result)
    
    if format == "pdf":
        pdf_content = report_generator.generate_pdf_report(result, input_text, domain)
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=compliance_report.pdf"}
        )
    elif format == "markdown":
        md_content = report_generator.generate_markdown_report(result, input_text, domain)
        return Response(
            content=md_content,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=compliance_report.md"}
        )
    else:
        raise HTTPException(status_code=400, detail="Format must be 'pdf' or 'markdown'")

@app.get("/learning-insights")
def get_learning_insights():
    return analytics.get_learning_insights()

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CAEPA Backend"}

def check_cross_domain_conflicts(input_text: str) -> list:
    conflicts = []
    
    # Mock cross-domain conflict detection
    if "store indefinitely" in input_text.lower():
        conflicts.append({
            "conflict": "Data retention conflict",
            "gdpr": "Violates Right to Erasure (Article 17)",
            "ccpa": "Requires disclosure of retention period",
            "severity": "high"
        })
    
    if "collect ip address" in input_text.lower():
        conflicts.append({
            "conflict": "Personal data classification",
            "gdpr": "IP address is personal data",
            "ccpa": "May require opt-out mechanism",
            "severity": "medium"
        })
    
    return conflicts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
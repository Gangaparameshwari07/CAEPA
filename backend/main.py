from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CAEPA - Context-Aware Ethical Policy Assistant")

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

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CAEPA Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
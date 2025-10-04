from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from typing import Dict
from compliance_interceptor import ComplianceInterceptor

app = FastAPI(title="CAEPA MCP Gateway - Enterprise Compliance Firewall")

# Initialize compliance interceptor
interceptor = ComplianceInterceptor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service routing configuration
SERVICE_ROUTES = {
    "gdpr": "http://gdpr-service:8001",
    "hipaa": "http://hipaa-service:8002", 
    "sox": "http://sox-service:8003",
    "general": "http://backend:8000"
}

@app.get("/")
def gateway_info():
    return {
        "service": "CAEPA MCP Gateway",
        "available_domains": list(SERVICE_ROUTES.keys()),
        "routing": "Multi-tenant compliance analysis"
    }

@app.post("/analyze/{domain}")
async def route_analysis(domain: str, request: Request):
    if domain not in SERVICE_ROUTES:
        raise HTTPException(
            status_code=404, 
            detail=f"Domain '{domain}' not supported. Available: {list(SERVICE_ROUTES.keys())}"
        )
    
    request_body = await request.json()
    
    # 🛡️ COMPLIANCE INTERCEPTOR - Real-time regulatory firewall
    compliance_check = interceptor.intercept_request(request_body)
    
    if compliance_check["blocked"]:
        # Request blocked by compliance firewall
        raise HTTPException(
            status_code=403,
            detail={
                "error": "Compliance Violation Detected",
                "message": compliance_check["message"],
                "violations": compliance_check["violations"],
                "audit_id": compliance_check["audit_id"],
                "firewall_status": "BLOCKED"
            }
        )
    
    # Request approved - proceed to service
    target_url = SERVICE_ROUTES[domain]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{target_url}/analyze",
                json=request_body,
                timeout=30.0
            )
            
            result = response.json()
            result["routed_via"] = f"MCP Gateway -> {domain} service"
            result["service_endpoint"] = target_url
            result["compliance_audit_id"] = compliance_check["audit_id"]
            result["firewall_status"] = "APPROVED"
            
            return result
            
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Service {domain} unavailable: {str(e)}"
            )

@app.get("/audit-trail")
def get_audit_trail():
    return {
        "audit_trail": interceptor.get_audit_trail(),
        "compliance_report": interceptor.generate_compliance_report()
    }

@app.get("/compliance-stats")
def get_compliance_stats():
    return interceptor.generate_compliance_report()

@app.get("/health")
def gateway_health():
    return {
        "status": "healthy", 
        "gateway": "MCP routing active",
        "compliance_firewall": "ACTIVE",
        "interceptor_status": "MONITORING"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
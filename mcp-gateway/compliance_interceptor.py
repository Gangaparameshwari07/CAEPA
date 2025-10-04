import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

class ComplianceInterceptor:
    def __init__(self):
        self.blocked_patterns = [
            "us_client_id",
            "eu_personal_data", 
            "cross_border_transfer",
            "unauthorized_access"
        ]
        self.audit_log = []
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("ComplianceInterceptor")

    def intercept_request(self, request_data: Dict) -> Dict:
        """Real-time regulatory firewall for MCP Gateway"""
        
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{len(self.audit_log) + 1}",
            "action": "INTERCEPT_ANALYSIS",
            "status": "PENDING"
        }

        # Extract request content
        input_text = request_data.get("input_text", "").lower()
        domain = request_data.get("analysis_type", "general")
        
        # Check for regulatory violations
        violations = self.detect_violations(input_text, domain)
        
        if violations:
            # BLOCK REQUEST - Regulatory firewall activated
            audit_entry.update({
                "status": "BLOCKED",
                "reason": "REGULATORY_FIREWALL_TRIGGERED",
                "violations": violations,
                "blocked_patterns": [v["pattern"] for v in violations]
            })
            
            self.audit_log.append(audit_entry)
            self.logger.warning(f"🚫 BLOCKED REQUEST {audit_entry['request_id']}: {violations}")
            
            return {
                "blocked": True,
                "reason": "Regulatory compliance violation detected",
                "violations": violations,
                "audit_id": audit_entry["request_id"],
                "message": "Request blocked by MCP Compliance Interceptor"
            }
        
        else:
            # ALLOW REQUEST - Compliance check passed
            audit_entry.update({
                "status": "ALLOWED",
                "reason": "COMPLIANCE_CHECK_PASSED",
                "domain": domain
            })
            
            self.audit_log.append(audit_entry)
            self.logger.info(f"✅ ALLOWED REQUEST {audit_entry['request_id']}")
            
            return {
                "blocked": False,
                "audit_id": audit_entry["request_id"],
                "message": "Request approved by compliance firewall"
            }

    def detect_violations(self, input_text: str, domain: str) -> List[Dict]:
        violations = []
        
        # Data residency violations
        if "us_client" in input_text and domain == "gdpr":
            violations.append({
                "type": "DATA_RESIDENCY_VIOLATION",
                "pattern": "us_client_id",
                "severity": "CRITICAL",
                "regulation": "GDPR Article 44 - International Transfers",
                "description": "US client data cannot be processed under GDPR without adequacy decision"
            })
        
        # Cross-border transfer violations
        if "transfer to" in input_text and "non-eu" in input_text:
            violations.append({
                "type": "CROSS_BORDER_VIOLATION", 
                "pattern": "cross_border_transfer",
                "severity": "HIGH",
                "regulation": "GDPR Chapter V - Transfers",
                "description": "Cross-border data transfer requires appropriate safeguards"
            })
        
        # Unauthorized access patterns
        if "admin access" in input_text and "no approval" in input_text:
            violations.append({
                "type": "ACCESS_CONTROL_VIOLATION",
                "pattern": "unauthorized_access", 
                "severity": "HIGH",
                "regulation": "SOX Section 404 - Internal Controls",
                "description": "Administrative access requires proper authorization controls"
            })

        return violations

    def get_audit_trail(self) -> List[Dict]:
        """Enterprise audit trail for compliance reporting"""
        return self.audit_log

    def generate_compliance_report(self) -> Dict:
        """Generate compliance firewall statistics"""
        total_requests = len(self.audit_log)
        blocked_requests = len([log for log in self.audit_log if log["status"] == "BLOCKED"])
        
        return {
            "total_requests": total_requests,
            "blocked_requests": blocked_requests,
            "block_rate": f"{(blocked_requests/total_requests*100):.1f}%" if total_requests > 0 else "0%",
            "compliance_effectiveness": "HIGH" if blocked_requests > 0 else "MONITORING",
            "audit_entries": self.audit_log[-10:]  # Last 10 entries
        }
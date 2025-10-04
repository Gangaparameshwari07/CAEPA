from typing import List, Dict
import re

class ExplainabilityEngine:
    def __init__(self):
        self.policy_patterns = {
            'gdpr': {
                'personal_data': r'(email|phone|address|name|ip.?address|user.?id)',
                'consent': r'(consent|permission|agree|opt.?in)',
                'storage': r'(store|save|retain|keep|database)',
                'processing': r'(process|collect|gather|use)'
            },
            'hipaa': {
                'phi': r'(patient|medical|health|diagnosis|treatment)',
                'access_control': r'(login|auth|password|secure)',
                'encryption': r'(encrypt|secure|protect|hash)'
            },
            'sox': {
                'financial_data': r'(revenue|profit|financial|accounting|audit)',
                'controls': r'(control|verify|validate|approve)',
                'documentation': r'(document|record|log|trail)'
            }
        }

    def generate_reasoning_chain(self, input_text: str, domain: str, analysis_result: Dict) -> List[Dict]:
        reasoning_steps = []
        
        # Step 1: Input Classification
        reasoning_steps.append({
            "step": 1,
            "action": "Input Classification",
            "finding": f"Analyzing {len(input_text.split())} words for {domain.upper()} compliance",
            "confidence": 0.95
        })

        # Step 2: Pattern Detection
        patterns = self.policy_patterns.get(domain.lower(), {})
        detected_patterns = []
        
        for pattern_name, pattern_regex in patterns.items():
            matches = re.findall(pattern_regex, input_text.lower())
            if matches:
                detected_patterns.append({
                    "pattern": pattern_name,
                    "matches": matches,
                    "count": len(matches)
                })

        if detected_patterns:
            reasoning_steps.append({
                "step": 2,
                "action": "Pattern Detection",
                "finding": f"Detected {len(detected_patterns)} compliance-relevant patterns",
                "details": detected_patterns,
                "confidence": 0.88
            })

        # Step 3: Policy Mapping
        policy_violations = self.map_to_policies(detected_patterns, domain)
        if policy_violations:
            reasoning_steps.append({
                "step": 3,
                "action": "Policy Mapping",
                "finding": f"Mapped to {len(policy_violations)} potential policy violations",
                "details": policy_violations,
                "confidence": 0.82
            })

        # Step 4: Risk Assessment
        risk_level = self.calculate_risk_level(analysis_result['status'])
        reasoning_steps.append({
            "step": 4,
            "action": "Risk Assessment",
            "finding": f"Calculated risk level: {risk_level}",
            "confidence": 0.90
        })

        # Step 5: Final Decision
        reasoning_steps.append({
            "step": 5,
            "action": "Final Decision",
            "finding": f"Status: {analysis_result['status']} - {analysis_result['violation_summary']}",
            "confidence": 0.85
        })

        return reasoning_steps

    def map_to_policies(self, patterns: List[Dict], domain: str) -> List[Dict]:
        policy_mapping = {
            'gdpr': {
                'personal_data': 'GDPR Article 4 - Personal Data Definition',
                'consent': 'GDPR Article 6 - Lawful Basis for Processing',
                'storage': 'GDPR Article 5 - Data Minimization Principle'
            },
            'hipaa': {
                'phi': 'HIPAA Privacy Rule - Protected Health Information',
                'access_control': 'HIPAA Security Rule - Access Control',
                'encryption': 'HIPAA Security Rule - Encryption Standards'
            },
            'sox': {
                'financial_data': 'SOX Section 302 - Financial Disclosure',
                'controls': 'SOX Section 404 - Internal Controls',
                'documentation': 'SOX Section 409 - Real-time Disclosure'
            }
        }

        violations = []
        domain_policies = policy_mapping.get(domain.lower(), {})
        
        for pattern in patterns:
            policy = domain_policies.get(pattern['pattern'])
            if policy:
                violations.append({
                    "pattern": pattern['pattern'],
                    "policy": policy,
                    "severity": "high" if pattern['count'] > 2 else "medium"
                })

        return violations

    def calculate_risk_level(self, status: str) -> str:
        risk_mapping = {
            'RED': 'Critical Risk - Immediate Action Required',
            'YELLOW': 'Medium Risk - Review Recommended', 
            'GREEN': 'Low Risk - Compliant'
        }
        return risk_mapping.get(status, 'Unknown Risk Level')

    def generate_confidence_score(self, reasoning_steps: List[Dict]) -> float:
        if not reasoning_steps:
            return 0.0
        
        total_confidence = sum(step.get('confidence', 0.5) for step in reasoning_steps)
        return round(total_confidence / len(reasoning_steps), 2)
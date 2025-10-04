import openai
import os
from typing import Dict, List

class ProactivePolicyGenerator:
    def __init__(self):
        try:
            self.cerebras_client = openai.OpenAI(
                api_key=os.getenv("CEREBRAS_API_KEY", "demo-key"),
                base_url="https://api.cerebras.ai/v1"
            )
        except AttributeError:
            # Fallback for older OpenAI versions
            self.cerebras_client = None
            print("Using fallback mode - upgrade OpenAI: pip install openai>=1.0.0")

    def generate_compliant_policy(self, violation_text: str, domain: str) -> Dict:
        """Generate corrected policy text using Llama 3 via Cerebras"""
        
        policy_templates = {
            "gdpr": """
            GDPR-compliant policy template:
            - Explicit consent mechanisms
            - Data subject rights (access, rectification, erasure)
            - Lawful basis for processing
            - Data protection by design
            """,
            "hipaa": """
            HIPAA-compliant policy template:
            - Protected Health Information safeguards
            - Access controls and authentication
            - Audit logging requirements
            - Breach notification procedures
            """,
            "sox": """
            SOX-compliant policy template:
            - Internal controls over financial reporting
            - Management assessment requirements
            - Auditor attestation procedures
            - Documentation and retention standards
            """
        }

        template = policy_templates.get(domain, policy_templates["gdpr"])
        
        prompt = f"""
        You are a legal compliance expert. Generate a complete, compliant policy section to replace this problematic text.

        PROBLEMATIC TEXT: {violation_text}
        
        COMPLIANCE DOMAIN: {domain.upper()}
        
        TEMPLATE REQUIREMENTS: {template}
        
        Generate a complete, professional policy paragraph that:
        1. Addresses the specific violation
        2. Includes required legal language
        3. Provides clear implementation guidance
        4. Ensures full regulatory compliance
        
        Output ONLY the corrected policy text, no explanations.
        """

        try:
            if self.cerebras_client:
                response = self.cerebras_client.chat.completions.create(
                    model="llama3.1-8b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=400
                )
                generated_policy = response.choices[0].message.content.strip()
            else:
                # Fallback mode
                generated_policy = self.generate_fallback_policy(violation_text, domain)["generated_policy"]
            
            return {
                "original_text": violation_text,
                "generated_policy": generated_policy,
                "compliance_domain": domain.upper(),
                "generation_method": "Llama 3.1-8B via Cerebras API",
                "policy_improvements": self.analyze_improvements(violation_text, generated_policy)
            }
            
        except Exception as e:
            # Fallback policy generation
            return self.generate_fallback_policy(violation_text, domain)

    def analyze_improvements(self, original: str, generated: str) -> List[str]:
        """Analyze what improvements were made"""
        improvements = []
        
        if "consent" in generated.lower() and "consent" not in original.lower():
            improvements.append("Added explicit consent mechanism")
        
        if "data subject rights" in generated.lower():
            improvements.append("Included data subject rights provisions")
        
        if "audit" in generated.lower() and "audit" not in original.lower():
            improvements.append("Added audit trail requirements")
        
        if "encryption" in generated.lower():
            improvements.append("Specified data encryption standards")
        
        if "retention" in generated.lower():
            improvements.append("Defined data retention policies")
        
        return improvements if improvements else ["Enhanced regulatory compliance language"]

    def generate_fallback_policy(self, violation_text: str, domain: str) -> Dict:
        """Fallback policy generation for demo purposes"""
        
        fallback_policies = {
            "gdpr": """
            Data Processing Policy: We collect and process personal data only with explicit, informed consent from data subjects. 
            Users have the right to access, rectify, or erase their personal data at any time. 
            All data processing activities are conducted under lawful basis as defined in GDPR Article 6, 
            with appropriate technical and organizational measures to ensure data security and privacy by design.
            """,
            "hipaa": """
            Protected Health Information Policy: All PHI is safeguarded through role-based access controls, 
            encryption at rest and in transit, and comprehensive audit logging. 
            Access to PHI is granted only to authorized personnel on a need-to-know basis, 
            with regular access reviews and immediate revocation upon role changes.
            """,
            "sox": """
            Financial Controls Policy: All financial reporting processes include documented internal controls, 
            segregation of duties, and management oversight. 
            Financial data accuracy is ensured through automated controls, regular reconciliations, 
            and independent verification procedures with complete audit trails.
            """
        }
        
        return {
            "original_text": violation_text,
            "generated_policy": fallback_policies.get(domain, fallback_policies["gdpr"]).strip(),
            "compliance_domain": domain.upper(),
            "generation_method": "Fallback template (Cerebras unavailable)",
            "policy_improvements": ["Added comprehensive compliance framework"]
        }
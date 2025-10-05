from typing import Dict, List, Tuple
import re

class ComplianceGradingSystem:
    def __init__(self):
        self.violation_weights = {
            "CRITICAL": 25,
            "HIGH": 15, 
            "MEDIUM": 8,
            "LOW": 3
        }

    def calculate_compliance_grade(self, analysis_result: Dict, input_text: str) -> Dict:
        """Calculate letter grade (A-F) based on violations"""
        
        # Count specific violations by type
        violation_counts = self.count_violations(input_text, analysis_result.get("evidence", []))
        
        # Calculate total penalty points
        total_penalty = 0
        for violation_type, count in violation_counts.items():
            severity = self.get_violation_severity(violation_type)
            total_penalty += count * self.violation_weights.get(severity, 5)
        
        # Convert to letter grade
        letter_grade = self.penalty_to_grade(total_penalty)
        
        # Calculate percentage score
        max_possible_penalty = 100
        percentage_score = max(0, 100 - (total_penalty / max_possible_penalty * 100))
        
        return {
            "letter_grade": letter_grade,
            "percentage_score": round(percentage_score, 1),
            "total_violations": sum(violation_counts.values()),
            "violation_breakdown": violation_counts,
            "penalty_points": total_penalty,
            "grade_explanation": self.get_grade_explanation(letter_grade)
        }

    def count_violations(self, input_text: str, evidence: List[str]) -> Dict[str, int]:
        """Count specific violations by regulation"""
        violations = {
            "GDPR_violations": 0,
            "CCPA_violations": 0, 
            "HIPAA_violations": 0,
            "SOX_violations": 0
        }
        
        # Count violations from evidence
        for evidence_item in evidence:
            if "GDPR" in evidence_item or "Critical_violation" in evidence_item:
                violations["GDPR_violations"] += 1
            elif "HIPAA" in evidence_item:
                violations["HIPAA_violations"] += 1
            elif "SOX" in evidence_item:
                violations["SOX_violations"] += 1
            elif "Minor_issue" in evidence_item:
                violations["CCPA_violations"] += 1
        
        # If no evidence but input has issues, analyze text
        if not evidence or all(v == 0 for v in violations.values()):
            text_lower = input_text.lower().replace('_', ' ')
            
            if "email" in text_lower and "consent" not in text_lower:
                violations["GDPR_violations"] += 1
            if "forever" in text_lower or "permanent" in text_lower:
                violations["GDPR_violations"] += 1
            if "third party" in text_lower:
                violations["GDPR_violations"] += 1
            if "patient" in text_lower and "encrypt" not in text_lower:
                violations["HIPAA_violations"] += 1
        
        return violations

    def get_violation_severity(self, violation_type: str) -> str:
        """Determine severity based on violation type"""
        severity_map = {
            "GDPR_violations": "CRITICAL",
            "HIPAA_violations": "CRITICAL", 
            "SOX_violations": "HIGH",
            "CCPA_violations": "MEDIUM"
        }
        return severity_map.get(violation_type, "LOW")

    def penalty_to_grade(self, penalty_points: int) -> str:
        """Convert penalty points to letter grade"""
        if penalty_points == 0:
            return "A+"
        elif penalty_points <= 5:
            return "A"
        elif penalty_points <= 15:
            return "B"
        elif penalty_points <= 30:
            return "C"
        elif penalty_points <= 50:
            return "D"
        else:
            return "F"

    def get_grade_explanation(self, grade: str) -> str:
        """Provide explanation for the grade"""
        explanations = {
            "A+": "Perfect compliance - No violations detected",
            "A": "Excellent compliance - Minor issues only",
            "B": "Good compliance - Some improvements needed", 
            "C": "Fair compliance - Multiple issues require attention",
            "D": "Poor compliance - Significant violations present",
            "F": "Failing compliance - Critical violations require immediate action"
        }
        return explanations.get(grade, "Compliance assessment completed")

    def generate_fix_summary(self, violation_counts: Dict[str, int]) -> List[str]:
        """Generate summary of what the fix button will address"""
        fixes = []
        
        if violation_counts.get("GDPR_violations", 0) > 0:
            fixes.append(f"Fix {violation_counts['GDPR_violations']} GDPR violation(s)")
        
        if violation_counts.get("CCPA_violations", 0) > 0:
            fixes.append(f"Fix {violation_counts['CCPA_violations']} CCPA issue(s)")
        
        if violation_counts.get("HIPAA_violations", 0) > 0:
            fixes.append(f"Fix {violation_counts['HIPAA_violations']} HIPAA violation(s)")
        
        if violation_counts.get("SOX_violations", 0) > 0:
            fixes.append(f"Fix {violation_counts['SOX_violations']} SOX issue(s)")
        
        return fixes if fixes else ["No fixes needed - Document is compliant"]
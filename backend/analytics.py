from typing import List, Dict
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class ComplianceAnalytics:
    def __init__(self, data_file="compliance_history.json"):
        self.data_file = data_file
        self.history = self.load_history()

    def load_history(self) -> List[Dict]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_analysis(self, analysis_result: Dict, input_text: str, domain: str):
        record = {
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "status": analysis_result["status"],
            "violation_summary": analysis_result["violation_summary"],
            "evidence": analysis_result.get("evidence", []),
            "latency_ms": analysis_result["latency_ms"],
            "input_length": len(input_text),
            "feedback": None  # Will be updated when user provides feedback
        }
        
        self.history.append(record)
        
        # Keep only last 1000 records for demo
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
        
        with open(self.data_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def get_risk_dashboard_data(self) -> Dict:
        if not self.history:
            return self.get_mock_dashboard_data()

        # Status distribution
        status_counts = Counter(record["status"] for record in self.history)
        
        # Top violations
        violation_counts = Counter()
        for record in self.history:
            if record["status"] in ["RED", "YELLOW"]:
                violation_counts[record["violation_summary"]] += 1
        
        # Compliance score over time (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_records = [
            record for record in self.history 
            if datetime.fromisoformat(record["timestamp"]) > thirty_days_ago
        ]
        
        daily_scores = defaultdict(list)
        for record in recent_records:
            date = datetime.fromisoformat(record["timestamp"]).date()
            score = 100 if record["status"] == "GREEN" else 50 if record["status"] == "YELLOW" else 0
            daily_scores[date.isoformat()].append(score)
        
        # Average scores by day
        avg_daily_scores = {
            date: sum(scores) / len(scores) 
            for date, scores in daily_scores.items()
        }

        # Domain breakdown
        domain_stats = defaultdict(lambda: {"total": 0, "violations": 0})
        for record in self.history:
            domain_stats[record["domain"]]["total"] += 1
            if record["status"] in ["RED", "YELLOW"]:
                domain_stats[record["domain"]]["violations"] += 1

        return {
            "status_distribution": dict(status_counts),
            "top_violations": dict(violation_counts.most_common(5)),
            "compliance_trend": avg_daily_scores,
            "domain_breakdown": dict(domain_stats),
            "total_analyses": len(self.history),
            "avg_latency": sum(r["latency_ms"] for r in self.history) / len(self.history) if self.history else 0
        }

    def get_mock_dashboard_data(self) -> Dict:
        return {
            "status_distribution": {"GREEN": 45, "YELLOW": 23, "RED": 12},
            "top_violations": {
                "Missing consent mechanism": 8,
                "Inadequate data encryption": 6,
                "Insufficient access controls": 4,
                "Missing audit trail": 3,
                "Improper data retention": 2
            },
            "compliance_trend": {
                "2024-01-15": 85.2,
                "2024-01-16": 78.9,
                "2024-01-17": 92.1,
                "2024-01-18": 88.7,
                "2024-01-19": 91.3
            },
            "domain_breakdown": {
                "gdpr": {"total": 35, "violations": 8},
                "hipaa": {"total": 25, "violations": 5},
                "sox": {"total": 20, "violations": 2}
            },
            "total_analyses": 80,
            "avg_latency": 245
        }

    def add_feedback(self, analysis_id: int, feedback: str):
        if 0 <= analysis_id < len(self.history):
            self.history[analysis_id]["feedback"] = feedback
            with open(self.data_file, 'w') as f:
                json.dump(self.history, f, indent=2)

    def get_learning_insights(self) -> Dict:
        feedback_records = [r for r in self.history if r.get("feedback")]
        
        if not feedback_records:
            return {
                "total_feedback": 0,
                "accuracy_rate": 0.95,  # Mock data
                "improvement_areas": ["Data encryption patterns", "Consent mechanisms"]
            }

        correct_feedback = len([r for r in feedback_records if r["feedback"] == "correct"])
        accuracy_rate = correct_feedback / len(feedback_records) if feedback_records else 0

        return {
            "total_feedback": len(feedback_records),
            "accuracy_rate": accuracy_rate,
            "improvement_areas": ["Pattern recognition", "Context understanding"]
        }
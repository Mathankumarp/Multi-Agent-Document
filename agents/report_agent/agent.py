from typing import List, Dict, Any
from .tool import calculate_audit_summary

class ReportAgent:
    def execute(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        summary = calculate_audit_summary(changes)
        summary["changes"] = changes
        return summary

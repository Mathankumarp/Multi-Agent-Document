from typing import Dict, Any
from .agent import ReportAgent

def report_node(state: Dict[str, Any]) -> Dict[str, Any]:
    agent = ReportAgent()
    report = agent.execute(state.get("changes", []))
    return {"report": report}

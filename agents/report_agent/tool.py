from typing import List, Dict, Any
from ...models import Severity, RiskSignal

def calculate_audit_summary(changes: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = {Severity.CRITICAL: 0, Severity.MODERATE: 0, Severity.TRIVIAL: 0}
    
    for c in changes:
        sev = c.get("severity", "trivial")
        if sev in counts:
            counts[sev] += 1
        else:
            counts[Severity.TRIVIAL] += 1
            
    if counts[Severity.CRITICAL] > 0:
        signal = RiskSignal.REJECT
    elif counts[Severity.MODERATE] > 3:
        signal = RiskSignal.REVIEW
    else:
        signal = RiskSignal.PASS
        
    return {
        "total_changes": len(changes),
        "severity_breakdown": counts,
        "risk_signal": signal
    }

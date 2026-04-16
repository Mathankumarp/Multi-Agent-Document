from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "critical"
    MODERATE = "moderate"
    TRIVIAL = "trivial"

class RiskSignal(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    REJECT = "reject"

class ChangeType(str, Enum):
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"

class DocumentChange(BaseModel):
    field_path: str
    change_type: ChangeType
    old_value: Any = None
    new_value: Any = None
    severity: Optional[Severity] = None
    justification: Optional[str] = None

class AuditReport(BaseModel):
    total_changes: int
    severity_breakdown: Dict[Severity, int]
    changes: List[DocumentChange]
    risk_signal: RiskSignal

class CompareRequest(BaseModel):
    doc1: Dict[str, Any]
    doc2: Dict[str, Any]

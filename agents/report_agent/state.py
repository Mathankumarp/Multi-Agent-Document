from typing import Dict, Any, List
from pydantic import BaseModel

class ReportState(BaseModel):
    changes: List[Dict[str, Any]]
    report: Dict[str, Any] = {}

from typing import Dict, Any, List
from pydantic import BaseModel

class DiffState(BaseModel):
    doc1: Dict[str, Any]
    doc2: Dict[str, Any]
    changes: List[Dict[str, Any]] = []

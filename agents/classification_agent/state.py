from typing import Dict, Any, List
from pydantic import BaseModel

class ClassificationState(BaseModel):
    changes: List[Dict[str, Any]]

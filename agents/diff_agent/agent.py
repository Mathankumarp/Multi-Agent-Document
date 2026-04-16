from typing import Dict, Any, List
from .tool import recursive_diff

class DiffAgent:
    def execute(self, doc1: Dict[str, Any], doc2: Dict[str, Any]) -> List[Any]:
        changes = recursive_diff(doc1, doc2)
        return [c.model_dump() for c in changes]

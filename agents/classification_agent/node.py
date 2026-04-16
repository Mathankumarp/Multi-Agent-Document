from typing import Dict, Any
from .agent import ClassificationAgent

def classification_node(state: Dict[str, Any]) -> Dict[str, Any]:
    agent = ClassificationAgent()
    updated_changes = agent.execute(state.get("changes", []))
    return {"changes": updated_changes}

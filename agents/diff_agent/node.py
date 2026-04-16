from typing import Dict, Any
from .agent import DiffAgent

def diff_node(state: Dict[str, Any]) -> Dict[str, Any]:
    agent = DiffAgent()
    changes = agent.execute(state["doc1"], state["doc2"])
    return {"changes": changes}

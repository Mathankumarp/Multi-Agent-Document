from typing import List, Dict, Any
from .tool import call_groq_classifier
from .prompt import CLASSIFICATION_SYSTEM_PROMPT

class ClassificationAgent:
    def execute(self, changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not changes:
            return []
            
        try:
            classifications = call_groq_classifier(changes, CLASSIFICATION_SYSTEM_PROMPT)
            classification_map = {c["field_path"]: c for c in classifications}
            
            for c in changes:
                cls = classification_map.get(c["field_path"], {"severity": "moderate", "justification": "Defaulted."})
                c["severity"] = cls.get("severity", "moderate")
                c["justification"] = cls.get("justification", "No justification provided.")
            
            return changes
        except Exception as e:
            print(f"Classification error: {e}")
            for c in changes:
                c["severity"] = "moderate"
                c["justification"] = "Failed to classify via LLM."
            return changes

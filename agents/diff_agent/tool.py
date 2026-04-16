from typing import Dict, Any, List
from ...models import DocumentChange, ChangeType

def recursive_diff(doc1: Dict[str, Any], doc2: Dict[str, Any], path: str = "") -> List[DocumentChange]:
    changes = []
    all_keys = set(doc1.keys()) | set(doc2.keys())
    
    for key in all_keys:
        current_path = f"{path}.{key}" if path else key
        
        if key not in doc1:
            changes.append(DocumentChange(
                field_path=current_path,
                change_type=ChangeType.ADDED,
                new_value=doc2[key]
            ))
        elif key not in doc2:
            changes.append(DocumentChange(
                field_path=current_path,
                change_type=ChangeType.DELETED,
                old_value=doc1[key]
            ))
        else:
            val1 = doc1[key]
            val2 = doc2[key]
            
            if isinstance(val1, dict) and isinstance(val2, dict):
                changes.extend(recursive_diff(val1, val2, current_path))
            elif val1 != val2:
                changes.append(DocumentChange(
                    field_path=current_path,
                    change_type=ChangeType.MODIFIED,
                    old_value=val1,
                    new_value=val2
                ))
    return changes

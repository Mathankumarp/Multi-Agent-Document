import os
from typing import Dict, Any, TypedDict, List
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from .models import CompareRequest
from .agents.diff_agent.node import diff_node
from .agents.classification_agent.node import classification_node
from .agents.report_agent.node import report_node

load_dotenv()

class AgentState(TypedDict):
    doc1: Dict[str, Any]
    doc2: Dict[str, Any]
    changes: List[Dict[str, Any]]
    report: Dict[str, Any]

app = FastAPI(title="Multi-Agent Document Change Detection Pipeline")

def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("node_diff", diff_node)
    workflow.add_node("node_classification", classification_node)
    workflow.add_node("node_report", report_node)

    workflow.set_entry_point("node_diff")

    workflow.add_edge("node_diff", "node_classification")
    workflow.add_edge("node_classification", "node_report")
    workflow.add_edge("node_report", END)

    return workflow.compile()

graph = create_graph()

@app.post("/compare")
async def compare_documents(request: CompareRequest):
    if not request.doc1 or not request.doc2:
        raise HTTPException(status_code=400, detail="Invalid input documents.")

    initial_state = {
        "doc1": request.doc1,
        "doc2": request.doc2,
        "changes": [],
        "report": {}
    }
    
    try:
        final_state = await graph.ainvoke(initial_state)
        return final_state["report"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

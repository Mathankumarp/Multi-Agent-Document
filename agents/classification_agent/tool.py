import os
import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

def call_groq_classifier(changes_data: list, system_prompt: str) -> list:
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile",
        groq_api_key=os.environ.get("GROQ_API_KEY")
    )

    formatted_changes = json.dumps(changes_data, indent=2)
    human_msg = f"Classify the following document changes:\n\n{formatted_changes}"
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_msg)
    ])

    content = response.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)

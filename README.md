# Multi-Agent Document Change Detection Pipeline

An automated pipeline that detects, classifies, and reports changes between two versions of a product specification document using **LangGraph**, **FastAPI**, and **Groq LLMs**.

The system identifies document differences, evaluates their impact, and generates a structured audit report with a final **Risk Signal**.

---

# System Overview

The pipeline consists of **three specialized agents** orchestrated using **LangGraph**.

## 1. Diff Agent

A **programmatic comparison agent** that performs a recursive field-by-field comparison between two JSON documents.

It detects:

- Added fields  
- Deleted fields  
- Modified fields  

For each change it records:

- Field path
- Change type
- Old value
- New value

Using a programmatic approach ensures **accurate and deterministic change detection**.

---

## 2. Classification Agent

An **LLM-powered agent (Groq)** that evaluates each detected change and determines its **severity level**.

Severity categories:

- **Critical** – High impact on product functionality, safety, or compliance  
- **Moderate** – Feature-level or behavioral changes  
- **Trivial** – Minor wording or formatting changes  

Each classification includes a **short justification** explaining the reasoning.

---

## 3. Report Agent

The **report aggregation agent** compiles all classified changes into a structured **audit report**.

The report includes:

- Total number of changes
- Severity distribution
- Detailed list of changes
- Overall **Risk Signal**

Risk signal values:

- **Pass** – No significant issues detected  
- **Review** – Moderate changes that require verification  
- **Reject** – Critical changes that may affect product safety or compliance  

---

# Architecture

The pipeline is implemented as a **LangGraph StateGraph** with a linear workflow.

```
Diff Agent → Classification Agent → Report Agent
```

### Why This Design?

- **Decoupling** – Each node performs a single responsibility
- **Accuracy** – Diff detection is programmatic instead of LLM-based
- **Reasoning** – LLM evaluates the meaning and impact of changes
- **Standardized Output** – Report agent produces structured results for downstream systems

---

# Prerequisites

Before running the project, ensure you have:

- **Python 3.9 or higher**
- A **Groq API Key**

Get your key from:

https://console.groq.com/keys

---

# Installation

Clone the repository or navigate to the project directory.

```bash
git clone https://github.com/yourusername/multi-agent-document-change-detection.git
cd multi-agent-document-change-detection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the root directory.

```
GROQ_API_KEY=your_groq_api_key_here
```

---

# Running the Application

Start the FastAPI server:

```bash
python -m app.main
```

The API will be available at:

```
http://localhost:8000
```

---

# API Documentation

## POST `/compare`

Compares two document versions and generates a structured audit report.

### Request

```json
{
  "doc1": {},
  "doc2": {}
}
```

### Example Request

```json
{
  "doc1": {
    "product_name": "Phone X",
    "battery": "4500mAh",
    "charging": "45W"
  },
  "doc2": {
    "product_name": "Phone X",
    "battery": "5000mAh",
    "charging": "65W"
  }
}
```

---

### Response

```json
{
  "total_changes": 2,
  "severity_breakdown": {
    "critical": 0,
    "moderate": 2,
    "trivial": 0
  },
  "changes": [
    {
      "field_path": "battery",
      "change_type": "modified",
      "old_value": "4500mAh",
      "new_value": "5000mAh",
      "severity": "moderate",
      "justification": "Battery capacity increase impacts device performance."
    },
    {
      "field_path": "charging",
      "change_type": "modified",
      "old_value": "45W",
      "new_value": "65W",
      "severity": "moderate",
      "justification": "Charging speed improvement is a feature upgrade."
    }
  ],
  "risk_signal": "review"
}
```

---

# Project Structure

```
project-root
│
├── app
│   ├── agents
│   │   ├── diff_agent.py
│   │   ├── classification_agent.py
│   │   └── report_agent.py
│   │
│   ├── graph
│   │   └── pipeline_graph.py
│   │
│   ├── models
│   │   └── schemas.py
│   │
│   └── main.py
│
├── requirements.txt
├── README.md
└── .env
```

---

# Assumptions and Tradeoffs

### Linear Pipeline

The workflow is implemented as a **simple linear graph**.  
Future versions may support **parallel classification nodes** for different document sections.

### LLM Context Window

Currently, all detected changes are sent to the LLM at once.  
For **very large documents**, batching logic may be required.

### Risk Signal Logic

The **risk signal** is derived using simple rules:

- Any **critical change → Reject**
- Moderate changes → **Review**
- Only trivial changes → **Pass**

This logic can be modified in:

```
app/agents/report_agent.py
```

### Model Selection

The system uses:

```
llama-3.3-70b-versatile
```

via **Groq API** for strong reasoning performance.

---

# Future Improvements

Possible enhancements:

- Parallel LangGraph nodes for large documents
- Batch processing for large diffs
- Web dashboard for audit reports
- Support for PDF and DOCX document parsing
- Change visualization UI
- Historical change tracking

---


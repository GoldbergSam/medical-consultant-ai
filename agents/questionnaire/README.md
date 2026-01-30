### Questionnaire Agent
## Overview

The Questionnaire Agent is a conversational medical intake agent designed to collect structured, clinically relevant patient information before diagnosis.
It acts as the first-stage agent in a multi-agent medical AI system, responsible for:
- Conversational symptom intake
- Structured data extraction (OLDCARTS)
- Red-flag screening
- Clinical summarization
- Safe, schema-aligned handoff to the Diagnosis Agent

# Important:
This agent does not diagnose and does not provide medical advice.
It supports pre-diagnostic clinical decision-making only.

## Architecture Role

Patient
  ↓
Questionnaire Agent  ← (this module)
  ↓  structured, validated data
Diagnosis Agent
  ↓
Research / Recommendation Agents


The Questionnaire Agent ensures the Diagnosis Agent receives complete, structured, and validated inputs, minimizing hallucinations and re-questioning downstream.

## Core Responsibilities
# What the Questionnaire Agent DOES?
- Conducts a conversational medical intake
- Asks one question at a time
- Collects symptom history using OLDCARTS
- Identifies potential red flags
- Determines when enough information has been collected
- Produces a clinical summary (non-diagnostic)
- Outputs structured JSON aligned with the Diagnosis Agent schema

# What it DOES NOT do?
- Diagnose diseases
- Recommend treatments
- Replace clinical judgment
- Make final triage decisions

## Folder Structure
<img width="679" height="194" alt="image" src="https://github.com/user-attachments/assets/efce7f94-205f-45ff-8e79-9484d305bd59" />

agents/questionnaire/
├── logic.py        # Core agent orchestration & state
├── prompt.py       # Centralized prompt templates
├── validator.py    # Completion & urgency logic
├── schema.py       # Pydantic output schema
└── README.md       # This file

## Key Design Principles
1. Schema-Driven Completion (Not Fixed Question Count)
The agent does not stop after a fixed number of questions.
Instead, it continues asking questions until all required OLDCARTS fields are collected, ensuring the Diagnosis Agent has sufficient data.

2. OLDCARTS-Based Intake
The agent structures symptom history using the OLDCARTS framework:
- Onset
- Location
- Duration
- Character
- Aggravating factors
- Relieving factors
- Treatments tried
- Severity
This mirrors standard clinical practice and improves diagnostic reliability.

3. Unified LLM Call per Turn (Quota-Safe)
To operate safely within API limits (e.g., Gemini free tier), each patient interaction uses a single LLM call that performs:
- OLDCARTS extraction
- Red-flag detection
- Completion decision
- Next-question generation
This prevents rate-limit errors and improves efficiency.

4. Strict Separation of Concerns
# File and Responsibility
prompt.py	: Defines what the agent asks
logic.py	: Controls when and how questions are asked
validator.py	: Determines completeness & urgency
schema.py	: Enforces structured, validated output

This design improves maintainability, testing, and academic clarity.

# Output Format
When the questionnaire is complete, the agent returns a structured JSON object conforming to QuestionnaireOutput.

# Example Output (Simplified)
<img width="943" height="549" alt="image" src="https://github.com/user-attachments/assets/53fe0880-e685-4d59-81d8-6d9467d06de4" />

{
  "metadata": {
    "agent": "QuestionnaireAgent",
    "version": "3.0"
  },
  "chief_complaint": "Sore throat",
  "symptom_history": {
    "onset": "1 day ago",
    "location": "Throat",
    "duration": "Constant",
    "character": "Scratchy",
    "severity": "5/10"
  },
  "red_flag_summary": "No immediate red flags identified.",
  "urgency_hint": "non-urgent",
  "questionnaire_summary": "Patient reports a gradually worsening sore throat over one day with moderate severity and no associated systemic symptoms.",
  "ready_for_diagnosis": true
}

This output is directly consumable by the Diagnosis Agent.

## Integration with Diagnosis Agent
The Questionnaire Agent is designed to align with the following Diagnosis Agent requirements:

- chief_complaint
- symptom_history (OLDCARTS)
- urgency indicators
- clinical context summary
- No re-questioning is required downstream.

## Safety & Ethics
- No medical diagnosis is provided
- Language remains neutral and non-alarming
- Red flags are identified, not acted upon autonomously
- Includes disclaimers at later diagnostic stages

### How to Run (Local)
From the project root:

**python main.py**

The agent runs in an interactive CLI loop until questionnaire completion.

### Disclaimer
“A pre-diagnostic conversational agent that collects OLDCARTS-structured symptom data and performs red-flag screening before structured handoff to a diagnostic reasoning agent.”
This software is a research and educational prototype.
It is not a medical device and must not be used for clinical decision-making without professional supervision.

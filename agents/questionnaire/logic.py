import os
import time
import json
from dotenv import load_dotenv
from datetime import datetime

from google.genai import Client
from google.genai.errors import ClientError
from google.adk.agents import Agent

from agents.questionnaire.schema import QuestionnaireOutput, OLDCARTS
from agents.questionnaire.prompt import (
    INTAKE_STEP_PROMPT,
    SUMMARY_PROMPT,
)

from agents.questionnaire.validator import (
    is_oldcarts_complete,
    determine_urgency,
)

# ======================================================
# ENV SETUP
# ======================================================
load_dotenv()

MODEL_NAME = "models/gemini-flash-lite-latest"
genai_client = Client(api_key=os.getenv("GOOGLE_API_KEY"))

questionnaire_agent = Agent(
    name="QuestionnaireAgent",
    description="Schema-driven medical intake agent",
    model=MODEL_NAME
)

# ======================================================
# STATE (SESSION MEMORY)
# ======================================================
conversation_history: list[str] = []
oldcarts = OLDCARTS()
chief_complaint: str | None = None
red_flags: list[str] = []

# ======================================================
# MAIN ENTRY
# ======================================================
def run_questionnaire_agent(user_input: str):
    global conversation_history, oldcarts, chief_complaint, red_flags

    conversation_history.append(f"Patient: {user_input}")

    # --------------------------------------------------
    # Step 0: Capture chief complaint (first turn only)
    # --------------------------------------------------
    if chief_complaint is None:
        chief_complaint = user_input
        return "Thank you. When did this problem first start?"

    # --------------------------------------------------
    # Step 1: ONE unified Gemini call per turn
    # --------------------------------------------------
    step_prompt = INTAKE_STEP_PROMPT.format(
        conversation="\n".join(conversation_history),
        oldcarts=oldcarts.json()
    )

    try:
        response = genai_client.models.generate_content(
            model=MODEL_NAME,
            contents=step_prompt
        )
        step = json.loads(response.text.strip())

    except ClientError as e:
        if "RESOURCE_EXHAUSTED" in str(e):
            return (
                "I'm receiving many requests right now. "
                "Please wait about one minute and continue."
            )
        raise e

    except Exception:
        return "I'm having trouble understanding. Could you please rephrase that?"

    # --------------------------------------------------
    # Step 2: Update OLDCARTS incrementally
    # --------------------------------------------------
    extracted = step.get("extracted_oldcarts", {})
    for field in oldcarts.__fields__:
        if extracted.get(field) and not getattr(oldcarts, field):
            setattr(oldcarts, field, extracted[field])

    # --------------------------------------------------
    # Step 3: Capture red flags (if any)
    # --------------------------------------------------
    red_flag = step.get("red_flag")
    if red_flag and isinstance(red_flag, str) and red_flag.lower() != "none":
        red_flags.append(red_flag)

    # --------------------------------------------------
    # Step 4: STOP CONDITION (schema-driven)
    # --------------------------------------------------
    if step.get("complete") or is_oldcarts_complete(oldcarts):

        # ---- Summary generation (ONE final call) ----
        summary_prompt = SUMMARY_PROMPT.format(
            conversation="\n".join(conversation_history)
        )

        try:
            summary = genai_client.models.generate_content(
                model=MODEL_NAME,
                contents=summary_prompt
            ).text.strip()
        except Exception:
            summary = "Clinical summary could not be generated."

        output = QuestionnaireOutput(
            metadata={
                "agent": "QuestionnaireAgent",
                "version": "3.0"
            },
            patient_context={},
            chief_complaint=chief_complaint,
            symptom_history=oldcarts,
            red_flag_summary="; ".join(red_flags) or "No immediate red flags identified.",
            urgency_hint=determine_urgency(red_flags),
            questionnaire_summary=summary,
            ready_for_diagnosis=True,
            generated_at=datetime.utcnow().isoformat()
        )

        return output.model_dump()

    # --------------------------------------------------
    # Step 5: Ask next question
    # --------------------------------------------------
    next_question = step.get("next_question")

    if not next_question:
        next_question = "Could you tell me more about how this symptom feels?"

    conversation_history.append(f"Agent: {next_question}")

    # Slow down to avoid burst quota
    time.sleep(1.5)

    return next_question


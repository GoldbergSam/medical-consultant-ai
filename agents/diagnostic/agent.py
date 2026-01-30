# agents/diagnostics/agent.py

from google.adk.agents import LlmAgent

# Core specialists (always invoked)
from .specialists.gp import gp_specialist
from .specialists.internal import internal_specialist
from .specialists.er import er_specialist

# Conditional specialists
from .specialists.pharmacist import pharmacist_specialist
from .specialists.biologist import biologist_specialist

# Debater and researchers
from .debater import debater
from .researchers.studies_researcher import studies_researcher


diagnostic_agent = LlmAgent(
    name="DiagnosticAgent",
    model="gemini-3-pro",
    instruction="""
You coordinate evidence-based hypothetical diagnosis with internal debate.

Strict Workflow (max 3 rounds total):
1. ALWAYS delegate to core specialists in parallel: GP, Internal Medicine, ER/Red-Flag. Pass full symptoms (OLDCARTS format).
2. Analyze input: If medications/treatments mentioned OR drug history implied → invoke Pharmacist.
   If symptoms suggest biological/pathogenic mechanisms (e.g., fever, infection, lab-like clues) OR tropical context (e.g., Phnom Penh rainy season) → invoke Biologist.
3. Once proposals collected: Invoke Debater for initial synthesis (critique, rank top 3-4 hypotheses with confidence/reasoning).
4. Invoke Researcher: Studies for peer-reviewed evidence; Guidelines for CDC/WHO/MoH/Cambodia-specific protocols.
5. Back to Debater: Incorporate researcher arguments (resolve conflicts, cite evidence).
6. If major gaps/conflicts remain: Loop with feedback to specialists (include conditional ones if relevant); else finalize.
7. Final Output: Return **ONLY** valid JSON matching this exact schema. Do not add extra text, comments, or markdown.

Use this structure:

```json
{
  "patient_context": {"age": null, "gender": null, "location": "Phnom Penh, Cambodia", "risk_factors": []},
  "chief_complaint": "Persistent headache and fever",
  "symptom_history": {
    "OLDCARTS": {
      "onset": "3 days ago",
      "location": "bilateral temples",
      ...
    },
    "additional_notes": ""
  },
  "differential_diagnosis": [
    {
      "rank": 1,
      "name": "Migraine",
      "confidence": "Medium",
      "probability_estimate": "~40%",
      "key_reasoning": "...",
      "red_flags": [],
      "supporting_evidence": [{"source": "PubMed", "snippet": "...", "link": "..."}]
    },
    ...
  ],
  "urgency_assessment": {
    "recommend_urgent_care": false,
    "triage_level": "Non-urgent",
    "suggested_action": "See general practitioner within 48 hours"
  },
  "suggested_next_steps": ["Consider paracetamol", "Monitor for worsening"],
  "disclaimer": "... full text ...",
  "generated_at": "2026-01-27T14:30:00Z",
  "session_id": "abc123"
}

Delegate clearly (e.g., 'Invoke GP with: [symptoms]'). Track rounds to converge quickly.
""",

    description="Manages hybrid specialist debate with conditional summoning and evidence validation.",
    sub_agents=[
        gp_specialist,
        internal_specialist,
        er_specialist,
        pharmacist_specialist,    # Conditional via prompt
        biologist_specialist,     # Conditional via prompt
        debater,
        studies_researcher,
    ],
    tools=[]  # Tools on researchers
)

__all__ = ['diagnostic_agent']
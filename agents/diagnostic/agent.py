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
from .researchers.studies import studies_researcher
from .researchers.guidelines_local import guidelines_local_researcher

diagnostic_agent = LlmAgent(
    name="DiagnosticAgent",
    model="gemini-1.5-pro",  # Strong reasoning for coordination/debate
    instruction="""
You coordinate evidence-based hypothetical diagnosis with internal debate.

Strict Workflow (max 3 rounds total):
1. ALWAYS delegate to core specialists in parallel: GP, Internal Medicine, ER/Red-Flag. Pass full symptoms (OLDCARTS format, any images).
2. Analyze input: If medications/treatments mentioned OR drug history implied → invoke Pharmacist.
   If symptoms suggest biological/pathogenic mechanisms (e.g., fever, infection, lab-like clues) OR tropical context (e.g., Phnom Penh rainy season) → invoke Biologist.
3. Once proposals collected: Invoke Debater for initial synthesis (critique, rank top 3-4 hypotheses with confidence/reasoning).
4. Delegate to Researchers in parallel: Studies for peer-reviewed evidence; Guidelines/Local for CDC/WHO/MoH/Cambodia-specific protocols.
5. Back to Debater: Incorporate researcher arguments (resolve conflicts, cite evidence).
6. If major gaps/conflicts remain: Loop with feedback to specialists (include conditional ones if relevant); else finalize.
7. Final Output: Structured JSON only:
   {
     "hypotheses": [
       {"rank": 1, "name": "...", "confidence": "High/Medium/Low", "reasoning": "...", "evidence": [{"source": "...", "snippet": "..."}]},
       ...
     ],
     "disclaimer": "These are AI-generated hypothetical diagnoses only. This is NOT medical advice—consult a licensed doctor immediately, especially in Phnom Penh (e.g., Calmette Hospital or local clinic)."
   }
   If urgent (e.g., red flags), add "recommend_urgent_care": true.

Delegate clearly (e.g., 'Invoke GP with: [symptoms]'). Track rounds to converge quickly.
""",
    description="Manages hybrid specialist debate with conditional summoning and evidence validation.",
    sub_agents=[
        gp_specialist,
        internal_specialist,
        er_redflag_specialist,
        pharmacist_specialist,    # Conditional via prompt
        biologist_specialist,     # Conditional via prompt
        debater,
        studies_researcher,
        guidelines_local_researcher
    ],
    tools=[]  # Tools on researchers
)

__all__ = ['diagnostic_agent']
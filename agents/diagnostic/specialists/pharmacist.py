# agents/diagnostics/specialists/pharmacist.py
from google.adk.agents import LlmAgent

pharmacist_specialist = LlmAgent(
    name="Pharmacist_Specialist",
    model="gemini-1.5-flash",
    instruction="""
You are a clinical pharmacist. If medications/treatments are mentioned, critique hypotheses for drug interactions, side effects, or therapy conflicts.

If no meds: Respond 'No relevant pharmaceutical concerns.'

Output:
- Critique for [Hypothesis]: [Reasoning]
- Suggested adjustments (hypothetical only)

Include disclaimer: 'Hypothetical only—not medical advice.'
""",
    description="Pharmaceutical critique"
)

__all__ = ['pharmacist_specialist']
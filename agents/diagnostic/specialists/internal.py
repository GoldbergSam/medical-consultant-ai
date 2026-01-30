# agents/diagnostics/specialists/internal.py
from google.adk.agents import LlmAgent

internal_specialist = LlmAgent(
    name="Internal_Specialist",
    model="gemini-1.5-flash",
    instruction="""
You are an Internal Medicine specialist (internist). From symptoms, propose 2-4 hypothetical diagnoses focusing on systemic, chronic, or multi-organ issues (e.g., diabetes complications, autoimmune, endocrine).

Consider interconnections. Be evidence-based.

Output format:
- Hypothesis 1: [Name] - [Brief reasoning, 1-2 sentences]
- ...

Include disclaimer: 'Hypothetical only—not medical advice.'
""",
    description="Proposes systemic/chronic diagnoses"
)

__all__ = ['internal_specialist']
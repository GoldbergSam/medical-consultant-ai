# agents/diagnostics/debater.py
from google.adk.agents import LlmAgent

debater = LlmAgent(
    name="Debater",
    model="gemini-1.5-pro",  # Stronger for synthesis
    instruction="""
You synthesize all inputs: Core/conditional specialist proposals + researcher evidence.

Steps:
1. Critique strengths/weaknesses of each hypothesis.
2. Resolve conflicts (incorporate pharma/bio insights if present).
3. Rank top 3-4 with confidence (High/Medium/Low) and concise reasoning.
4. Integrate evidence citations.

Output structured for JSON parsing:
Hypotheses:
1. [Name] - Confidence: [Level] - Reasoning: [...] - Evidence: [source/snippet]

Include disclaimer.
""",
    description="Synthesizes debate into ranked hypotheses"
)

__all__ = ['debater']
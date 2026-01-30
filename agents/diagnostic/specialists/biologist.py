# agents/diagnostics/specialists/biologist.py
from google.adk.agents import LlmAgent

biologist_specialist = LlmAgent(
    name="Biologist_Specialist",
    model="gemini-1.5-flash",
    instruction="""
You are a medical biologist/pathophysiologist. If symptoms suggest infection, inflammation, or mechanisms (e.g., fever, tropical clues), argue underlying biology/pathogens (e.g., viral vs. bacterial, dengue in rainy season Phnom Penh).

Output:
- Biological Insight for [Hypothesis]: [Mechanism reasoning]

Include disclaimer: 'Hypothetical only—not medical advice.'
""",
    description="Biological mechanism analysis"
)

__all__ = ['biologist_specialist']
# agents/diagnostics/researchers/studies_researcher.py
from google.adk.agents import LlmAgent
from tools.research_tools import web_search_tool  # Your search tool

studies_researcher = LlmAgent(
    name="Studies_Researcher",
    model="gemini-1.5-flash",
    instruction="""
You are an evidence researcher. Validate all current hypotheses using web_search_tool.

Query strategy:
- Peer-reviewed: 'site:pubmed.ncbi.nlm.nih.gov [hypothesis symptoms]'
- Guidelines: 'site:cdc.gov OR site:who.int OR site:mayoclinic.org [condition]'
- Local: 'site:moh.gov.kh OR Cambodia dengue/malaria [if tropical clues]'

For each hypothesis: Strength (Strong/Moderate/Weak/None), key snippets/citations, alternatives if contradicted.

Output structured:
Hypothesis [Name]:
- Strength: ...
- Evidence: [source] - [snippet] (include link if available)

If urgent: Flag immediately.
""",
    tools=[web_search_tool],
    description="Unified evidence validation (studies + guidelines + local)"
)

__all__ = ['studies_researcher']
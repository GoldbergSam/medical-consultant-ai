from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class EvidenceItem(BaseModel):
    source: str = Field(..., description="Source name (e.g., PubMed, CDC, MoH Cambodia)")
    snippet: str = Field(..., description="Short relevant quote or summary")
    link: Optional[str] = Field(None, description="URL if available")

class Hypothesis(BaseModel):
    rank: int = Field(..., ge=1, description="Ranking position (1 = most likely)")
    name: str = Field(..., description="Diagnosis name (e.g., 'Migraine')")
    confidence: Literal["High", "Medium", "Low"] = Field(...)
    probability_estimate: Optional[str] = Field(None, description="e.g., '~60%'")
    key_reasoning: str = Field(...)
    red_flags: List[str] = Field(default_factory=list)
    supporting_evidence: List[EvidenceItem] = Field(default_factory=list)

class OLDCARTS(BaseModel):
    onset: str = Field(default="")
    location: str = Field(default="")
    duration: str = Field(default="")
    character: str = Field(default="")
    aggravating: str = Field(default="")
    alleviating: str = Field(default="")
    related_symptoms: str = Field(default="")
    treatments_tried: str = Field(default="")
    severity: str = Field(default="")

class SymptomHistory(BaseModel):
    oldcarts: OLDCARTS = Field(..., alias="OLDCARTS")  # lowercase field, uppercase JSON key
    additional_notes: str = Field(default="")
class UrgencyAssessment(BaseModel):
    recommend_urgent_care: bool = Field(...)
    triage_level: Optional[Literal["Emergent", "Urgent", "Semi-urgent", "Non-urgent"]] = None
    suggested_action: str = Field(default="")

class DiagnosticOutput(BaseModel):
    """Final structured output from the Diagnostic Agent for clinical handoff"""
    patient_context: dict = Field(
        default_factory=dict,
        description="age, gender, location, risk_factors (use null/empty if unknown)"
    )
    chief_complaint: str = Field(...)
    symptom_history: SymptomHistory = Field(...)
    differential_diagnosis: List[Hypothesis] = Field(..., min_length=1, max_length=5)
    urgency_assessment: UrgencyAssessment = Field(...)
    suggested_next_steps: List[str] = Field(default_factory=list)
    disclaimer: str = Field(
        default="These are AI-generated hypothetical diagnoses only. This is NOT medical advice. Consult a licensed doctor immediately, especially in Phnom Penh (e.g., Calmette Hospital or local clinic)."
    )
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    session_id: Optional[str] = None

# Export for easy imports
__all__ = ['DiagnosticOutput', 'Hypothesis', 'EvidenceItem', ...]
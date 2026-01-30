from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OLDCARTS(BaseModel):
    onset: str = ""
    location: str = ""
    duration: str = ""
    character: str = ""
    aggravating: str = ""
    alleviating: str = ""
    related_symptoms: str = ""
    treatments_tried: str = ""
    severity: str = ""

class QuestionnaireOutput(BaseModel):
    metadata: dict = Field(default_factory=dict)

    patient_context: dict = Field(
        default_factory=dict,
        description="age, gender, location, risk_factors (null if unknown)"
    )

    chief_complaint: str = Field(...)

    symptom_history: OLDCARTS = Field(...)

    red_flag_summary: str = Field(
        default="No immediate red flags identified."
    )

    urgency_hint: Optional[str] = Field(
        default=None,
        description="emergent | urgent | semi-urgent | non-urgent"
    )

    questionnaire_summary: str = Field(
        description="Concise clinical summary for the Diagnosis Agent"
    )

    ready_for_diagnosis: bool = Field(default=True)

    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

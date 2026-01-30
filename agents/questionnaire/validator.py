from agents.questionnaire.schema import OLDCARTS

REQUIRED_FIELDS = [
    "onset",
    "location",
    "duration",
    "character",
    "severity"
]

def is_oldcarts_complete(oldcarts: OLDCARTS) -> bool:
    """
    Determines whether enough symptom data is collected
    to safely proceed to diagnosis.
    """
    return all(
        getattr(oldcarts, field).strip()
        for field in REQUIRED_FIELDS
    )

def determine_urgency(red_flags: list[str]) -> str:
    """
    Maps red flags to urgency hints.
    """
    if not red_flags:
        return "non-urgent"

    emergency_keywords = [
        "chest pain",
        "shortness of breath",
        "bleeding",
        "loss of consciousness",
        "severe headache",
        "stroke"
    ]

    for flag in red_flags:
        for keyword in emergency_keywords:
            if keyword in flag.lower():
                return "emergent"

    return "urgent"

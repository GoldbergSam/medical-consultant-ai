from .specialists.gp import gp_specialist
from .specialists.internal import internal_specialist
from .specialists.er import er_specialist
from .specialists.pharmacist import pharmacist_specialist
from .specialists.biologist import biologist_specialist
from .debater import debater
from .agent import diagnostic_agent

__all__ = [
    'diagnostic_agent',
    'gp_specialist', 
    'internal_specialist',
    'er_specialist',
    'pharmacist_specialist', 
    'biologist_specialist',
    'debater'
]

"""
QCTD-QDS: Quantum-Inspired Cyber Threat Detection Framework
for Teleportation-Based Quantum Digital Signature Protocols

SIH Problem Statement 141

A deterministic quantum-inspired security framework that simulates
teleportation-based QDS, performs Pauli-basis projective measurements,
statistically analyses measurement outcomes, and applies mathematically
defined thresholds to detect forgery, impersonation, replay, and
quantum-channel manipulation.
"""

from .signature import QuantumSignature
from .teleportation import TeleportationEngine
from .measurement import ProjectiveMeasurement
from .statistics import StatisticalAnalyzer
from .attacks import AttackSimulator
from .decision_engine import DecisionEngine
from .session_manager import SessionManager
from .forgery_analysis import ForgeryAnalyzer
from .evaluation import FrameworkEvaluator

__version__ = "1.0.0"
__all__ = [
    "QuantumSignature",
    "TeleportationEngine",
    "ProjectiveMeasurement",
    "StatisticalAnalyzer",
    "AttackSimulator",
    "DecisionEngine",
    "SessionManager",
    "ForgeryAnalyzer",
    "FrameworkEvaluator",
]

"""
QCTD-QDS Configuration
Centralised constants, thresholds, and Pauli eigenstate definitions.
"""

import numpy as np

# ── Security Thresholds ───────────────────────────────────────────────
# Decision boundaries for the threshold-based threat detection engine.
# Adapted from QBER analysis in BB84-style protocols for QDS verification.
#
#   ACCEPT : E ≤ accept_threshold    → legitimate signature
#   FLAG   : accept < E ≤ reject     → elevated noise, needs review
#   REJECT : E > reject_threshold    → consistent with attack / forgery

THRESHOLDS = {
    "accept": 0.05,
    "reject": 0.15,
}

# ── Simulation Defaults ──────────────────────────────────────────────
DEFAULT_SIGNATURE_BITS = 8        # bits of message digest encoded
DEFAULT_TRIALS_PER_BIT = 100      # repeated measurements per signature qubit
DEFAULT_FORGERY_ATTEMPTS = 50     # Monte-Carlo forgery estimation rounds
DEFAULT_SECURITY_EVAL_RUNS = 20   # runs per scenario in full evaluation

# ── Pauli Eigenstates ─────────────────────────────────────────────────
# Z-basis : |0⟩, |1⟩        eigen-states of σ_z
# X-basis : |+⟩, |−⟩        eigen-states of σ_x
# Y-basis : |+i⟩, |−i⟩      eigen-states of σ_y

PAULI_EIGENSTATES = {
    "Z": {
        0: np.array([1, 0], dtype=complex),                     # |0⟩
        1: np.array([0, 1], dtype=complex),                     # |1⟩
    },
    "X": {
        0: np.array([1, 1], dtype=complex) / np.sqrt(2),       # |+⟩
        1: np.array([1, -1], dtype=complex) / np.sqrt(2),      # |−⟩
    },
    "Y": {
        0: np.array([1, 1j], dtype=complex) / np.sqrt(2),      # |+i⟩
        1: np.array([1, -1j], dtype=complex) / np.sqrt(2),     # |−i⟩
    },
}

# ── Noise Presets ─────────────────────────────────────────────────────
NOISE_PRESETS = {
    "none":     {"bit_flip_prob": 0.00, "phase_flip_prob": 0.00, "depolarizing_prob": 0.00},
    "low":      {"bit_flip_prob": 0.02, "phase_flip_prob": 0.01, "depolarizing_prob": 0.00},
    "moderate": {"bit_flip_prob": 0.05, "phase_flip_prob": 0.03, "depolarizing_prob": 0.00},
    "high":     {"bit_flip_prob": 0.10, "phase_flip_prob": 0.05, "depolarizing_prob": 0.00},
    "severe":   {"bit_flip_prob": 0.00, "phase_flip_prob": 0.00, "depolarizing_prob": 0.20},
}

# ── Database ──────────────────────────────────────────────────────────
DATABASE_PATH = "qctd_sessions.db"

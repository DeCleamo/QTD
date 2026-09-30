"""
Phase 5 – Attack Simulation Module
Provides pluggable attack operations for all four threat categories:
    A. Signature Forgery
    B. Impersonation
    C. Replay Attack
    D. Quantum Channel Manipulation
"""

import numpy as np
from .signature import QuantumSignature
from .config import PAULI_EIGENSTATES


class AttackSimulator:
    """
    Factory for attack-operation dicts that can be injected into the
    teleportation engine's ``build_circuit`` method.

    Each attack method returns either:
      • a dict  {"pre_teleport": fn, "post_teleport": fn}  that mutates
        the QuantumCircuit, OR
      • a modified QuantumSignature object (impersonation / replay).
    """

    # ── A. Signature Forgery ──────────────────────────────────────────

    @staticmethod
    def forgery_attack():
        """
        Random forgery: attacker applies a random Pauli / Hadamard gate
        to the message qubit *before* teleportation, without knowing the
        correct state.
        """
        def pre_teleport(qc):
            gate = np.random.choice(["x", "y", "z", "h"])
            getattr(qc, gate)(0)
        return {"pre_teleport": pre_teleport, "post_teleport": None}

    @staticmethod
    def targeted_forgery_attack():
        """
        Targeted forgery: attacker always applies X (bit-flip) to forge
        the signature.  Maximally damaging against Z-basis states.
        """
        def pre_teleport(qc):
            qc.x(0)
        return {"pre_teleport": pre_teleport, "post_teleport": None}

    @staticmethod
    def phase_forgery_attack():
        """
        Phase forgery: attacker applies Z (phase-flip).
        Maximally damaging against X-basis states, invisible to Z-basis.
        """
        def pre_teleport(qc):
            qc.z(0)
        return {"pre_teleport": pre_teleport, "post_teleport": None}

    # ── B. Impersonation ──────────────────────────────────────────────

    @staticmethod
    def impersonation_attack(original_signature):
        """
        The attacker creates a signature for the *same* message but
        without knowing the signer's basis choices.  The attacker picks
        random bases, producing states that are generally incompatible
        with the verifier's expected measurement outcomes.

        Returns
        -------
        QuantumSignature  –  a "forged" signature with wrong bases.
        """
        fake = QuantumSignature(
            original_signature.message,
            original_signature.num_signature_bits,
            signer_id="Eve_Impersonator",
        )
        # Force bases to differ from the original signer's choices
        fake.bases = [
            np.random.choice([b for b in ("X", "Y", "Z") if b != ob])
            for ob in original_signature.bases
        ]
        fake.states = [
            PAULI_EIGENSTATES[basis][bit].copy()
            for bit, basis in zip(fake.signature_bits, fake.bases)
        ]
        return fake

    # ── C. Replay Attack ──────────────────────────────────────────────

    @staticmethod
    def replay_attack(original_signature):
        """
        The attacker captures a previously valid signature and attempts
        to reuse it verbatim.  Detection relies on the SessionManager
        recognising the duplicate ``signature_id``.

        Returns the *same* signature object.
        """
        return original_signature

    # ── D. Quantum Channel Manipulation ───────────────────────────────

    @staticmethod
    def channel_manipulation_attack(attack_type="depolarizing"):
        """
        The attacker (or an adversarial channel) injects noise *after*
        teleportation completes.

        Supported attack_types
        ----------------------
        depolarizing      – random Pauli with probability 0.75
        bit_flip          – deterministic X gate on verifier qubit
        phase_flip        – deterministic Z gate on verifier qubit
        intercept_resend  – random Pauli (models measure-and-resend)
        """
        if attack_type == "depolarizing":
            def post_teleport(qc):
                r = np.random.rand()
                if r < 0.25:
                    qc.x(2)
                elif r < 0.50:
                    qc.y(2)
                elif r < 0.75:
                    qc.z(2)
            return {"pre_teleport": None, "post_teleport": post_teleport}

        elif attack_type == "bit_flip":
            def post_teleport(qc):
                qc.x(2)
            return {"pre_teleport": None, "post_teleport": post_teleport}

        elif attack_type == "phase_flip":
            def post_teleport(qc):
                qc.z(2)
            return {"pre_teleport": None, "post_teleport": post_teleport}

        elif attack_type == "intercept_resend":
            def post_teleport(qc):
                gate = np.random.choice(["x", "y", "z"])
                getattr(qc, gate)(2)
            return {"pre_teleport": None, "post_teleport": post_teleport}

        else:
            raise ValueError(f"Unknown channel attack type: {attack_type}")

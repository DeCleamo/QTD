"""
Phase 2 – Bell-State Entanglement & Quantum Teleportation
Builds teleportation circuits with Pauli corrections and optional
noise / attack injection points.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


class TeleportationEngine:
    """
    Teleports a single-qubit quantum state from Signer to Verifier
    via a shared Bell pair, applying Pauli corrections classically.

    Circuit layout
    ──────────────
        q0 : message qubit (signature state)
        q1 : Signer's half of the Bell pair
        q2 : Verifier's half of the Bell pair
    """

    def __init__(self):
        self.simulator = AerSimulator()

    # ── circuit construction ──────────────────────────────────────────

    def build_circuit(self, message_state, measurement_basis="Z",
                      noise_model=None, attack_operation=None):
        """
        Build a 3-qubit teleportation circuit.

        Parameters
        ----------
        message_state : array-like
            Two-element statevector for the message qubit.
        measurement_basis : str  {"X", "Y", "Z"}
            Pauli basis in which the verifier performs the final measurement.
        noise_model : dict | None
            Keys: bit_flip_prob, phase_flip_prob, depolarizing_prob.
        attack_operation : dict | None
            Keys: "pre_teleport" and/or "post_teleport", each a callable
            that receives the QuantumCircuit and mutates it in-place.
        """
        qc = QuantumCircuit(3, 3)

        # Prepare the message qubit
        qc.initialize(message_state, 0)

        # ── pre-teleportation attack (e.g. forgery) ───────────────────
        if attack_operation and attack_operation.get("pre_teleport"):
            attack_operation["pre_teleport"](qc)

        # ── Bell pair (q1, q2) ────────────────────────────────────────
        qc.h(1)
        qc.cx(1, 2)
        qc.barrier()

        # ── Bell-basis measurement on (q0, q1) ───────────────────────
        qc.cx(0, 1)
        qc.h(0)
        qc.measure(0, 0)
        qc.measure(1, 1)

        # ── Pauli corrections on q2 ──────────────────────────────────
        with qc.if_test((1, 1)):
            qc.x(2)
        with qc.if_test((0, 1)):
            qc.z(2)

        # ── post-teleportation attack (e.g. channel manipulation) ────
        if attack_operation and attack_operation.get("post_teleport"):
            attack_operation["post_teleport"](qc)

        # ── channel noise (physical, not adversarial) ─────────────────
        self._inject_noise(qc, noise_model)

        # ── basis rotation + final measurement on q2 ─────────────────
        if measurement_basis == "X":
            qc.h(2)
        elif measurement_basis == "Y":
            qc.sdg(2)
            qc.h(2)
        # Z basis → no rotation

        qc.measure(2, 2)
        return qc

    # ── execution ─────────────────────────────────────────────────────

    def execute_circuit(self, qc, shots=1):
        """Transpile and run, returning raw counts dict."""
        tqc = transpile(qc, self.simulator)
        result = self.simulator.run(tqc, shots=shots).result()
        return result.get_counts()

    def teleport_and_measure(self, message_state, measurement_basis="Z",
                              noise_model=None, attack_operation=None):
        """
        End-to-end: teleport → measure → return the verifier's single bit.
        """
        qc = self.build_circuit(message_state, measurement_basis,
                                noise_model, attack_operation)
        counts = self.execute_circuit(qc, shots=1)
        bitstring = list(counts.keys())[0]
        # Qiskit bit-ordering: bitstring is c2 c1 c0 (MSB first)
        verifier_bit = int(bitstring[0])
        return verifier_bit

    # ── private ───────────────────────────────────────────────────────

    @staticmethod
    def _inject_noise(qc, noise_model):
        """Probabilistically apply noise gates on q2."""
        if noise_model is None:
            return
        if noise_model.get("bit_flip_prob", 0) > 0:
            if np.random.rand() < noise_model["bit_flip_prob"]:
                qc.x(2)
        if noise_model.get("phase_flip_prob", 0) > 0:
            if np.random.rand() < noise_model["phase_flip_prob"]:
                qc.z(2)
        if noise_model.get("depolarizing_prob", 0) > 0:
            p = noise_model["depolarizing_prob"]
            r = np.random.rand()
            if r < p / 3:
                qc.x(2)
            elif r < 2 * p / 3:
                qc.y(2)
            elif r < p:
                qc.z(2)

"""
Phase 1 – Quantum Signature Generation
Encodes a message digest into Pauli eigenstates with randomly chosen bases.
"""

import hashlib
import numpy as np
from .config import PAULI_EIGENSTATES


class QuantumSignature:
    """
    Generates a quantum digital signature from an arbitrary message.

    Workflow
    --------
    1. SHA-256 hash the message to produce a fixed-length digest.
    2. Extract *n* bits from the digest.
    3. For each bit, randomly choose a Pauli basis (X, Y, or Z).
    4. Encode the bit as the corresponding eigenstate.

    The basis choices form part of the signing key and are shared with the
    verifier over an authenticated classical channel.
    """

    def __init__(self, message: str, num_signature_bits: int = 8,
                 signer_id: str = "Alice"):
        self.message = message
        self.signer_id = signer_id
        self.num_signature_bits = num_signature_bits

        # Hash → bits
        self.digest = hashlib.sha256(message.encode()).hexdigest()
        self.signature_bits = self._extract_bits(self.digest, num_signature_bits)

        # Signing key: random basis per bit
        self.bases = [np.random.choice(["X", "Y", "Z"])
                      for _ in range(num_signature_bits)]

        # Prepare quantum states
        self.states = [
            PAULI_EIGENSTATES[basis][bit].copy()
            for bit, basis in zip(self.signature_bits, self.bases)
        ]

        # Unique signature identifier
        self.signature_id = hashlib.sha256(
            f"{message}|{signer_id}|{np.random.randint(0, 2**32)}".encode()
        ).hexdigest()[:16]

    # ── helpers ────────────────────────────────────────────────────────
    @staticmethod
    def _extract_bits(hex_digest: str, n_bits: int) -> list:
        """Extract the first *n_bits* from a hex digest."""
        binary = bin(int(hex_digest, 16))[2:].zfill(256)
        return [int(b) for b in binary[:n_bits]]

    def get_verification_info(self) -> dict:
        """
        Information sent to the verifier over the authenticated classical
        channel: bases, expected bits, and signature metadata.
        """
        return {
            "signature_id": self.signature_id,
            "signer_id": self.signer_id,
            "bases": list(self.bases),
            "expected_bits": list(self.signature_bits),
            "num_bits": self.num_signature_bits,
            "message_hash": self.digest,
        }

    def state_label(self, index: int) -> str:
        """Human-readable label for a signature qubit."""
        basis = self.bases[index]
        bit = self.signature_bits[index]
        labels = {
            ("Z", 0): "|0⟩", ("Z", 1): "|1⟩",
            ("X", 0): "|+⟩", ("X", 1): "|−⟩",
            ("Y", 0): "|+i⟩", ("Y", 1): "|−i⟩",
        }
        return labels.get((basis, bit), "?")

    def __repr__(self):
        return (f"QuantumSignature(signer='{self.signer_id}', "
                f"id='{self.signature_id}', bits={self.num_signature_bits})")

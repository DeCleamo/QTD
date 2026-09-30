"""
Phase 3 – Projective Measurements
Runs repeated teleport-and-measure trials on each signature qubit and
collects per-bit and aggregate statistics.
"""

from .teleportation import TeleportationEngine


class ProjectiveMeasurement:
    """
    Verifier-side projective measurement engine.

    For each signature qubit the engine:
      1. Teleports the state from Signer → Verifier.
      2. Measures in the agreed Pauli basis (X / Y / Z).
      3. Repeats for *n_trials* to build measurement statistics.
      4. Compares observed outcomes to the expected honest-run outcome.
    """

    def __init__(self):
        self.engine = TeleportationEngine()

    # ── single-bit measurement ────────────────────────────────────────

    def measure_signature_bit(self, state, basis, n_trials,
                               noise_model=None, attack_operation=None):
        """
        Teleport + measure a single qubit *n_trials* times.

        Returns
        -------
        dict  with keys: outcomes, count_0, count_1, prob_0, prob_1, n_trials
        """
        outcomes = []
        for _ in range(n_trials):
            bit = self.engine.teleport_and_measure(
                state, basis, noise_model, attack_operation
            )
            outcomes.append(bit)

        c0 = outcomes.count(0)
        c1 = outcomes.count(1)
        return {
            "outcomes": outcomes,
            "count_0": c0,
            "count_1": c1,
            "prob_0": c0 / n_trials,
            "prob_1": c1 / n_trials,
            "n_trials": n_trials,
        }

    # ── full signature verification ───────────────────────────────────

    def verify_signature(self, signature, verification_info, n_trials_per_bit,
                          noise_model=None, attack_operation=None):
        """
        Verify an entire quantum signature.

        For each bit, the state is teleported *n_trials_per_bit* times and
        outcomes are compared against the expected bit.

        Parameters
        ----------
        signature : QuantumSignature
            The signature object whose `states` are teleported.
        verification_info : dict
            From ``signature.get_verification_info()``.
        n_trials_per_bit : int
            Measurement repetitions per qubit.
        noise_model, attack_operation : optional
            Passed through to the teleportation engine.

        Returns
        -------
        dict  with per_bit_results, aggregate_error_rate, totals, etc.
        """
        per_bit = []
        total_mismatches = 0
        total_measurements = 0

        for idx, (state, basis, expected_bit) in enumerate(zip(
            signature.states,
            verification_info["bases"],
            verification_info["expected_bits"],
        )):
            meas = self.measure_signature_bit(
                state, basis, n_trials_per_bit,
                noise_model, attack_operation,
            )

            mismatches = sum(1 for o in meas["outcomes"] if o != expected_bit)

            meas.update({
                "bit_index": idx,
                "basis": basis,
                "expected_bit": expected_bit,
                "mismatches": mismatches,
                "error_rate": mismatches / n_trials_per_bit,
            })

            per_bit.append(meas)
            total_mismatches += mismatches
            total_measurements += n_trials_per_bit

        agg_error = (total_mismatches / total_measurements
                     if total_measurements else 0.0)

        return {
            "per_bit_results": per_bit,
            "total_mismatches": total_mismatches,
            "total_measurements": total_measurements,
            "aggregate_error_rate": agg_error,
            "signature_id": verification_info["signature_id"],
            "signer_id": verification_info["signer_id"],
        }

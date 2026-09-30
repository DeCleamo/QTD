"""
Phase 7 – Forgery Probability Analysis
Monte-Carlo estimation of forgery success rates across attack types.
"""

import numpy as np
from .signature import QuantumSignature
from .measurement import ProjectiveMeasurement
from .statistics import StatisticalAnalyzer
from .decision_engine import DecisionEngine
from .attacks import AttackSimulator
from .config import DEFAULT_FORGERY_ATTEMPTS


class ForgeryAnalyzer:
    """
    Runs repeated simulated attacks and computes the empirical
    probability that a forged signature passes verification.

    For each attack type:
        P_forge = (successful forgeries) / (total attempts)
    """

    def __init__(self, decision_engine=None):
        self.measurement = ProjectiveMeasurement()
        self.analyzer = StatisticalAnalyzer()
        self.engine = decision_engine or DecisionEngine()

    # ── main API ──────────────────────────────────────────────────────

    def estimate_forgery_probability(
        self,
        message: str = "test",
        n_attempts: int = None,
        n_trials_per_bit: int = 30,
        n_signature_bits: int = 4,
        attack_type: str = "random_forgery",
        progress_callback=None,
    ) -> dict:
        """
        Parameters
        ----------
        message            : message to sign
        n_attempts         : Monte-Carlo rounds (default from config)
        n_trials_per_bit   : measurement repetitions per qubit per round
        n_signature_bits   : number of digest bits encoded
        attack_type        : one of
            random_forgery, targeted_forgery, phase_forgery,
            channel_depolarizing, channel_bit_flip, channel_intercept_resend
        progress_callback  : optional callable(attempt_index, n_attempts)

        Returns
        -------
        dict  with forgery_rate, mean/std/min/max error rates, counts
        """
        n_attempts = n_attempts or DEFAULT_FORGERY_ATTEMPTS
        successes = 0
        error_rates = []

        for i in range(n_attempts):
            if progress_callback:
                progress_callback(i, n_attempts)

            sig = QuantumSignature(message, n_signature_bits)
            vinfo = sig.get_verification_info()

            attack_op = self._get_attack(attack_type)

            result = self.measurement.verify_signature(
                sig, vinfo, n_trials_per_bit, attack_operation=attack_op,
            )
            metrics = self.analyzer.compute_error_metrics(result)
            verdict = self.engine.evaluate(metrics)

            error_rates.append(metrics["error_rate"])
            if verdict["verdict"] == "ACCEPT":
                successes += 1

        return {
            "attack_type":          attack_type,
            "n_attempts":           n_attempts,
            "successful_forgeries": successes,
            "forgery_rate":         successes / n_attempts,
            "mean_error_rate":      float(np.mean(error_rates)),
            "std_error_rate":       float(np.std(error_rates)),
            "min_error_rate":       float(np.min(error_rates)),
            "max_error_rate":       float(np.max(error_rates)),
        }

    # ── convenience: run all attack types ─────────────────────────────

    def run_full_analysis(self, message="test", n_attempts=None,
                           n_trials_per_bit=30, n_signature_bits=4,
                           progress_callback=None):
        """
        Run forgery analysis for every supported attack type and return
        a summary table as a list of dicts.
        """
        attack_types = [
            "random_forgery",
            "targeted_forgery",
            "phase_forgery",
            "channel_depolarizing",
            "channel_bit_flip",
            "channel_intercept_resend",
        ]
        results = []
        for at in attack_types:
            r = self.estimate_forgery_probability(
                message, n_attempts, n_trials_per_bit, n_signature_bits,
                at, progress_callback,
            )
            results.append(r)
        return results

    # ── internal ──────────────────────────────────────────────────────

    @staticmethod
    def _get_attack(attack_type):
        if attack_type == "random_forgery":
            return AttackSimulator.forgery_attack()
        if attack_type == "targeted_forgery":
            return AttackSimulator.targeted_forgery_attack()
        if attack_type == "phase_forgery":
            return AttackSimulator.phase_forgery_attack()
        if attack_type == "channel_depolarizing":
            return AttackSimulator.channel_manipulation_attack("depolarizing")
        if attack_type == "channel_bit_flip":
            return AttackSimulator.channel_manipulation_attack("bit_flip")
        if attack_type == "channel_intercept_resend":
            return AttackSimulator.channel_manipulation_attack("intercept_resend")
        raise ValueError(f"Unknown attack type: {attack_type}")

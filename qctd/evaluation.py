"""
Phase 8 – Security & Performance Evaluation
End-to-end assessment of detection rates, false-accept / false-reject
rates, and computational performance of the QCTD-QDS framework.
"""

import time
import numpy as np
from .signature import QuantumSignature
from .measurement import ProjectiveMeasurement
from .statistics import StatisticalAnalyzer
from .decision_engine import DecisionEngine
from .attacks import AttackSimulator
from .config import DEFAULT_SECURITY_EVAL_RUNS, NOISE_PRESETS


class FrameworkEvaluator:
    """
    Runs the complete verification pipeline under multiple scenarios
    (honest, noisy, and each attack type) and computes aggregate
    security and performance metrics.
    """

    SCENARIOS = ("honest", "noisy", "forgery", "targeted_forgery",
                 "impersonation", "channel_depolarizing",
                 "channel_bit_flip")

    def __init__(self):
        self.measurement = ProjectiveMeasurement()
        self.analyzer = StatisticalAnalyzer()
        self.engine = DecisionEngine()

    # ── security evaluation ───────────────────────────────────────────

    def evaluate_security(self, message="test", n_runs=None,
                           n_trials_per_bit=50, n_signature_bits=4,
                           progress_callback=None):
        """
        Run *n_runs* verification rounds per scenario and compute
        detection / false-accept / false-reject rates.
        """
        n_runs = n_runs or DEFAULT_SECURITY_EVAL_RUNS
        counts = {s: {"ACCEPT": 0, "FLAG": 0, "REJECT": 0}
                  for s in self.SCENARIOS}

        for run_idx in range(n_runs):
            if progress_callback:
                progress_callback(run_idx, n_runs)

            sig = QuantumSignature(message, n_signature_bits)
            vinfo = sig.get_verification_info()

            for scenario in self.SCENARIOS:
                noise, attack, test_sig = self._scenario_params(scenario, sig)
                r = self.measurement.verify_signature(
                    test_sig, vinfo, n_trials_per_bit,
                    noise_model=noise, attack_operation=attack,
                )
                m = self.analyzer.compute_error_metrics(r)
                v = self.engine.evaluate(m)
                counts[scenario][v["verdict"]] += 1

        # compute rates
        per_scenario = {}
        for s, c in counts.items():
            total = sum(c.values())
            per_scenario[s] = {
                "accept_rate": c["ACCEPT"] / total,
                "flag_rate":   c["FLAG"]   / total,
                "reject_rate": c["REJECT"] / total,
                "total_runs":  total,
            }

        attack_scenarios = [s for s in self.SCENARIOS if s != "honest"]
        detection_rates = {
            s: 1 - per_scenario[s]["accept_rate"] for s in attack_scenarios
        }
        avg_detection = float(np.mean(list(detection_rates.values())))

        security_metrics = {
            "per_attack_detection_rate":     detection_rates,
            "average_detection_rate":        avg_detection,
            "false_rejection_rate":          per_scenario["honest"]["reject_rate"],
            "false_flag_rate":               per_scenario["honest"]["flag_rate"],
            "honest_acceptance_rate":        per_scenario["honest"]["accept_rate"],
        }

        return {
            "per_scenario":   per_scenario,
            "security_metrics": security_metrics,
            "n_runs":         n_runs,
        }

    # ── performance evaluation ────────────────────────────────────────

    def evaluate_performance(self, message="test",
                              n_signature_bits=4, n_trials_per_bit=50):
        """
        Time each phase of the pipeline and return a breakdown.
        """
        # Phase 1: signature generation
        t0 = time.perf_counter()
        sig = QuantumSignature(message, n_signature_bits)
        t_sig = time.perf_counter() - t0

        vinfo = sig.get_verification_info()

        # Phases 2-3: teleportation + measurement
        t0 = time.perf_counter()
        result = self.measurement.verify_signature(sig, vinfo, n_trials_per_bit)
        t_verify = time.perf_counter() - t0

        # Phase 4: statistical analysis
        t0 = time.perf_counter()
        metrics = self.analyzer.compute_error_metrics(result)
        t_stats = time.perf_counter() - t0

        # Phase 6: decision
        t0 = time.perf_counter()
        self.engine.evaluate(metrics)
        t_decision = time.perf_counter() - t0

        total_circuits = n_signature_bits * n_trials_per_bit

        return {
            "signature_generation_ms": t_sig * 1000,
            "verification_ms":         t_verify * 1000,
            "statistical_analysis_ms": t_stats * 1000,
            "decision_ms":             t_decision * 1000,
            "total_ms":                (t_sig + t_verify + t_stats + t_decision) * 1000,
            "circuits_executed":       total_circuits,
            "time_per_circuit_ms":     (t_verify * 1000 / total_circuits
                                        if total_circuits else 0),
            "n_signature_bits":        n_signature_bits,
            "n_trials_per_bit":        n_trials_per_bit,
            "total_quantum_ops":       total_circuits * 7,  # ~7 gates/circuit
        }

    # ── private ───────────────────────────────────────────────────────

    @staticmethod
    def _scenario_params(scenario, sig):
        """Return (noise_model, attack_operation, signature) for a scenario."""
        if scenario == "honest":
            return None, None, sig
        if scenario == "noisy":
            return NOISE_PRESETS["moderate"], None, sig
        if scenario == "forgery":
            return None, AttackSimulator.forgery_attack(), sig
        if scenario == "targeted_forgery":
            return None, AttackSimulator.targeted_forgery_attack(), sig
        if scenario == "impersonation":
            fake = AttackSimulator.impersonation_attack(sig)
            return None, None, fake
        if scenario == "channel_depolarizing":
            return None, AttackSimulator.channel_manipulation_attack("depolarizing"), sig
        if scenario == "channel_bit_flip":
            return None, AttackSimulator.channel_manipulation_attack("bit_flip"), sig
        raise ValueError(scenario)

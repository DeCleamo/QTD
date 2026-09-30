"""
Phase 6 – Threshold-Based Decision Engine
Deterministic accept / flag / reject based on statistical metrics.
"""

from .config import THRESHOLDS


class DecisionEngine:
    """
    Converts the statistical-analysis output into a structured
    security verdict.  No AI/ML — purely threshold-based.

    Decision rule
    ─────────────
        E ≤ T_accept               → ACCEPT  (legitimate signature)
        T_accept < E ≤ T_reject    → FLAG    (elevated error, review)
        E > T_reject               → REJECT  (attack / forgery)
    """

    def __init__(self, thresholds=None):
        self.thresholds = dict(thresholds or THRESHOLDS)

    # ── main entry point ──────────────────────────────────────────────

    def evaluate(self, statistical_metrics: dict,
                 replay_detected: bool = False) -> dict:
        """
        Produce a verdict from statistical metrics.

        Parameters
        ----------
        statistical_metrics : dict
            Output of ``StatisticalAnalyzer.compute_error_metrics()``.
        replay_detected : bool
            True if the SessionManager flagged a duplicate signature_id.

        Returns
        -------
        dict  with verdict, threat_type, confidence, evidence, recommendation
        """
        e   = statistical_metrics["error_rate"]
        ci  = statistical_metrics["confidence_interval"]
        agr = statistical_metrics["measurement_agreement_rate"]

        # ── replay takes priority ─────────────────────────────────────
        if replay_detected:
            return self._make_verdict(
                "REJECT", "REPLAY_ATTACK", 1.0, e,
                "Duplicate signature ID detected — previously verified.",
                "Reject and log.  Investigate the source of the replayed signature.",
            )

        accept_t = self.thresholds["accept"]
        reject_t = self.thresholds["reject"]

        if e <= accept_t:
            return self._make_verdict(
                "ACCEPT", None,
                self._confidence(e), e,
                f"Error rate {e:.4f} ≤ {accept_t:.2f}. "
                f"Agreement {agr:.2%}.  95 % CI [{ci[0]:.4f}, {ci[1]:.4f}].",
                "Signature is statistically consistent with legitimate signing.",
            )

        if e <= reject_t:
            return self._make_verdict(
                "FLAG", "ELEVATED_ERROR",
                0.5, e,
                f"Error rate {e:.4f} is between accept ({accept_t:.2f}) and "
                f"reject ({reject_t:.2f}) thresholds.  "
                f"95 % CI [{ci[0]:.4f}, {ci[1]:.4f}].",
                "Flag for review.  Consider re-verification on a cleaner channel.",
            )

        # E > reject threshold
        threat = self._classify_threat(statistical_metrics)
        return self._make_verdict(
            "REJECT", threat,
            self._confidence(e), e,
            f"Error rate {e:.4f} > {reject_t:.2f}.  "
            f"Agreement {agr:.2%}.  95 % CI [{ci[0]:.4f}, {ci[1]:.4f}].  "
            f"χ² p = {statistical_metrics['chi_squared_p_value']:.4f}.",
            f"Reject — consistent with {threat}.  Log and alert.",
        )

    # ── threat classification ─────────────────────────────────────────

    @staticmethod
    def _classify_threat(metrics):
        """
        Heuristic threat-type labelling based on the shape of the error
        distribution.  Not a trained classifier — just structured rules.
        """
        e       = metrics["error_rate"]
        chi2_p  = metrics["chi_squared_p_value"]
        e_std   = metrics["error_std"]

        if e >= 0.90:
            return "TARGETED_FORGERY"
        if e >= 0.60:
            return "FORGERY_OR_IMPERSONATION"
        if chi2_p < 0.05 and e_std > 0.20:
            return "SELECTIVE_CHANNEL_MANIPULATION"
        return "GENERAL_ATTACK"

    # ── helpers ───────────────────────────────────────────────────────

    def _confidence(self, e):
        """Confidence ∈ [0.5, 1.0] — higher when *far* from thresholds."""
        t_a = self.thresholds["accept"]
        t_r = self.thresholds["reject"]
        if e <= t_a:
            return min(1.0, (1 - e / t_a) * 0.5 + 0.5)
        if e > t_r:
            excess = min(e - t_r, 1 - t_r)
            return min(1.0, excess / max(1 - t_r, 1e-9) * 0.5 + 0.5)
        return 0.5  # FLAG zone

    @staticmethod
    def _make_verdict(verdict, threat_type, confidence, error_rate,
                      evidence, recommendation):
        return {
            "verdict":        verdict,
            "threat_type":    threat_type,
            "confidence":     confidence,
            "error_rate":     error_rate,
            "evidence":       evidence,
            "recommendation": recommendation,
        }

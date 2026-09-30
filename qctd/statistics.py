"""
Phase 4 – Statistical Threat Detection
Computes error metrics, confidence intervals, chi-squared uniformity
tests, and derived quantities used by the decision engine.
"""

import numpy as np
from scipy import stats as sp_stats


class StatisticalAnalyzer:
    """
    Converts raw verification results into a rich set of statistical
    metrics that the threshold-based decision engine consumes.

    All methods are stateless (static / class-level); no simulator is
    needed at this stage.
    """

    @staticmethod
    def compute_error_metrics(verification_result: dict) -> dict:
        """
        Compute comprehensive statistics from a verification result.

        Returns
        -------
        dict with keys:
            error_rate, confidence_interval, per_bit_error_rates,
            error_std, chi_squared, chi_squared_p_value,
            deviation_sigma, measurement_agreement_rate,
            estimated_forgery_probability, verification_confidence,
            total_mismatches, total_measurements, anomalous_bits
        """
        e   = verification_result["aggregate_error_rate"]
        n   = verification_result["total_measurements"]
        k   = verification_result["total_mismatches"]
        pbr = verification_result["per_bit_results"]

        # ── Wilson-score 95 % confidence interval ─────────────────────
        ci_lo, ci_hi = StatisticalAnalyzer._wilson_ci(e, n)

        # ── per-bit error rates ───────────────────────────────────────
        per_bit_errors = [r["error_rate"] for r in pbr]
        error_std = float(np.std(per_bit_errors)) if len(per_bit_errors) > 1 else 0.0

        # ── chi-squared test for uniform error distribution ───────────
        per_bit_mm = [r["mismatches"] for r in pbr]
        chi2, chi2_p = StatisticalAnalyzer._chi_squared(per_bit_mm)

        # ── deviation from honest (expected 0 errors) ─────────────────
        #    Under honest run the expected error rate is 0; we measure
        #    deviation in units of the binomial standard deviation.
        se = np.sqrt(0.5 * 0.5 / n) if n > 0 else 1.0
        deviation_sigma = e / se

        # ── anomalous bits (error > 2× aggregate) ────────────────────
        threshold_anom = max(e * 2, 0.10)
        anomalous = [r["bit_index"] for r in pbr
                     if r["error_rate"] > threshold_anom]

        return {
            "error_rate":                    e,
            "confidence_interval":           (ci_lo, ci_hi),
            "confidence_level":              0.95,
            "per_bit_error_rates":           per_bit_errors,
            "error_std":                     error_std,
            "chi_squared":                   chi2,
            "chi_squared_p_value":           chi2_p,
            "deviation_sigma":               deviation_sigma,
            "total_mismatches":              k,
            "total_measurements":            n,
            "measurement_agreement_rate":    1.0 - e,
            "estimated_forgery_probability": min(1.0, e * 2),
            "verification_confidence":       max(0.0, 1.0 - e),
            "anomalous_bits":                anomalous,
        }

    # ── private helpers ───────────────────────────────────────────────

    @staticmethod
    def _wilson_ci(p, n, z=1.96):
        """Wilson score confidence interval for a proportion."""
        if n == 0:
            return (0.0, 0.0)
        denom = 1 + z ** 2 / n
        centre = (p + z ** 2 / (2 * n)) / denom
        margin = (z * np.sqrt((p * (1 - p) + z ** 2 / (4 * n)) / n)) / denom
        return (max(0.0, centre - margin), min(1.0, centre + margin))

    @staticmethod
    def _chi_squared(per_bit_mismatches):
        """Chi-squared goodness-of-fit test for uniform error spread."""
        n_bits = len(per_bit_mismatches)
        total = sum(per_bit_mismatches)
        if n_bits < 2 or total == 0:
            return 0.0, 1.0
        expected = total / n_bits
        if expected == 0:
            return 0.0, 1.0
        chi2, p = sp_stats.chisquare(per_bit_mismatches)
        return float(chi2), float(p)

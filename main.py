#!/usr/bin/env python3
"""
QCTD-QDS  —  Quantum-Inspired Cyber Threat Detection Framework
Teleportation-Based Quantum Digital Signature Protocols
SIH Problem Statement 141

Full end-to-end CLI demonstration of all eight phases.
"""

import sys
import time
import numpy as np

from qctd.signature import QuantumSignature
from qctd.measurement import ProjectiveMeasurement
from qctd.statistics import StatisticalAnalyzer
from qctd.attacks import AttackSimulator
from qctd.decision_engine import DecisionEngine
from qctd.session_manager import SessionManager
from qctd.forgery_analysis import ForgeryAnalyzer
from qctd.evaluation import FrameworkEvaluator
from qctd.config import NOISE_PRESETS

# ── ANSI helpers ──────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def verdict_colour(v):
    return {
        "ACCEPT": GREEN,
        "FLAG":   YELLOW,
        "REJECT": RED,
    }.get(v, "")

def header(title):
    w = 70
    print(f"\n{CYAN}{BOLD}{'─' * w}{RESET}")
    print(f"{CYAN}{BOLD}  {title}{RESET}")
    print(f"{CYAN}{BOLD}{'─' * w}{RESET}")

def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   QCTD-QDS : Quantum-Inspired Cyber Threat Detection Framework      ║
║   Teleportation-Based Quantum Digital Signature Protocols            ║
║   SIH Problem Statement 141                                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")


# ═══════════════════════════════════════════════════════════════════════
#  CONFIGURATION (adjust for speed vs. statistical strength)
# ═══════════════════════════════════════════════════════════════════════
MESSAGE            = "Quantum Digital Signature — SIH PS 141 Demo"
N_SIGNATURE_BITS   = 8
N_TRIALS_PER_BIT   = 50
FORGERY_ATTEMPTS   = 25
SECURITY_RUNS      = 10


def main():
    banner()
    total_start = time.perf_counter()

    # ── shared objects ────────────────────────────────────────────────
    meas    = ProjectiveMeasurement()
    stats   = StatisticalAnalyzer()
    engine  = DecisionEngine()
    session = SessionManager(db_path="qctd_demo.db")
    session.clear_history()  # fresh demo

    # ==================================================================
    #  PHASE 1: Quantum Signature Generation
    # ==================================================================
    header("Phase 1 — Quantum Signature Generation")

    sig   = QuantumSignature(MESSAGE, N_SIGNATURE_BITS, signer_id="Alice")
    vinfo = sig.get_verification_info()

    print(f"  Message      : {MESSAGE}")
    print(f"  Signer       : {sig.signer_id}")
    print(f"  Signature ID : {sig.signature_id}")
    print(f"  Digest (SHA) : {sig.digest[:32]}…")
    print(f"  Bits encoded : {N_SIGNATURE_BITS}")
    print()
    print(f"  {'Bit':>4}  {'Basis':>6}  {'Value':>6}  {'State':>6}")
    print(f"  {'────':>4}  {'─────':>6}  {'─────':>6}  {'─────':>6}")
    for i in range(N_SIGNATURE_BITS):
        print(f"  {i:>4}  {sig.bases[i]:>6}  {sig.signature_bits[i]:>6}  "
              f"{sig.state_label(i):>6}")

    # ==================================================================
    #  PHASE 2: Entanglement & Teleportation (info only)
    # ==================================================================
    header("Phase 2 — Bell-State Entanglement & Teleportation")
    print(f"  Bell pairs created    : {N_SIGNATURE_BITS}")
    print(f"  Entangled state       : |Φ⁺⟩ = (|00⟩ + |11⟩) / √2")
    print(f"  Protocol              : Standard quantum teleportation")
    print(f"  Pauli corrections     : Classically conditioned X, Z")
    print(f"  Trials per qubit      : {N_TRIALS_PER_BIT}")
    print(f"  Total circuits to run : {N_SIGNATURE_BITS * N_TRIALS_PER_BIT}")

    # ==================================================================
    #  PHASE 3: Projective Measurement Verification (honest run)
    # ==================================================================
    header("Phase 3 — Projective Measurement (Honest Run)")

    t0 = time.perf_counter()
    honest_result = meas.verify_signature(sig, vinfo, N_TRIALS_PER_BIT)
    t_honest = time.perf_counter() - t0
    honest_metrics = stats.compute_error_metrics(honest_result)

    print(f"\n  {'Bit':>4}  {'Basis':>6}  {'Expect':>7}  {'Errors':>7}  "
          f"{'ErrorRate':>10}  {'Status':>10}")
    print(f"  {'────':>4}  {'─────':>6}  {'──────':>7}  {'──────':>7}  "
          f"{'─────────':>10}  {'──────':>10}")
    for r in honest_result["per_bit_results"]:
        status = f"{GREEN}✓ Match{RESET}" if r["error_rate"] == 0 else f"{RED}✗ Error{RESET}"
        print(f"  {r['bit_index']:>4}  {r['basis']:>6}  {r['expected_bit']:>7}  "
              f"{r['mismatches']:>7}  {r['error_rate']:>10.4f}  {status:>10}")

    print(f"\n  Aggregate error rate : {honest_metrics['error_rate']:.4f}")
    print(f"  Measurement time     : {t_honest*1000:.1f} ms")

    # ==================================================================
    #  PHASE 4: Statistical Analysis
    # ==================================================================
    header("Phase 4 — Statistical Analysis (Honest Run)")

    m = honest_metrics
    print(f"  Error rate               : {m['error_rate']:.4f}")
    print(f"  95% Confidence interval  : [{m['confidence_interval'][0]:.4f}, "
          f"{m['confidence_interval'][1]:.4f}]")
    print(f"  Measurement agreement    : {m['measurement_agreement_rate']:.2%}")
    print(f"  Error std (per-bit)      : {m['error_std']:.4f}")
    print(f"  χ² statistic             : {m['chi_squared']:.4f}")
    print(f"  χ² p-value               : {m['chi_squared_p_value']:.4f}")
    print(f"  Deviation (σ)            : {m['deviation_sigma']:.2f}")
    print(f"  Est. forgery probability : {m['estimated_forgery_probability']:.4f}")
    print(f"  Verification confidence  : {m['verification_confidence']:.4f}")
    print(f"  Anomalous bits           : {m['anomalous_bits'] or 'None'}")

    # ==================================================================
    #  PHASE 5: Attack Simulation
    # ==================================================================
    header("Phase 5 — Attack Simulation")

    attacks = [
        ("A. Random Forgery",         None, AttackSimulator.forgery_attack(),                     sig),
        ("B. Targeted Forgery (X)",    None, AttackSimulator.targeted_forgery_attack(),            sig),
        ("C. Phase Forgery (Z)",       None, AttackSimulator.phase_forgery_attack(),               sig),
        ("D. Channel Depolarizing",    None, AttackSimulator.channel_manipulation_attack("depolarizing"), sig),
        ("E. Channel Bit-Flip",        None, AttackSimulator.channel_manipulation_attack("bit_flip"),     sig),
        ("F. Channel Intercept-Resend",None, AttackSimulator.channel_manipulation_attack("intercept_resend"), sig),
    ]

    # Impersonation uses a different signature
    fake_sig = AttackSimulator.impersonation_attack(sig)
    attacks.append(("G. Impersonation", None, None, fake_sig))

    attack_verdicts = []
    for label, noise, attack_op, test_sig in attacks:
        r = meas.verify_signature(test_sig, vinfo, N_TRIALS_PER_BIT,
                                   noise_model=noise, attack_operation=attack_op)
        met = stats.compute_error_metrics(r)
        vrd = engine.evaluate(met)

        vc = verdict_colour(vrd["verdict"])
        print(f"\n  {BOLD}{label}{RESET}")
        print(f"    Error rate  : {met['error_rate']:.4f}")
        print(f"    Verdict     : {vc}{BOLD}{vrd['verdict']}{RESET}"
              f"  ({vrd['threat_type'] or 'legitimate'})")
        print(f"    Confidence  : {vrd['confidence']:.2f}")
        attack_verdicts.append((label, met, vrd))

    # Noisy channel (not adversarial)
    print(f"\n  {BOLD}H. Noisy Channel (moderate){RESET}")
    r = meas.verify_signature(sig, vinfo, N_TRIALS_PER_BIT,
                               noise_model=NOISE_PRESETS["moderate"])
    met = stats.compute_error_metrics(r)
    vrd = engine.evaluate(met)
    vc = verdict_colour(vrd["verdict"])
    print(f"    Error rate  : {met['error_rate']:.4f}")
    print(f"    Verdict     : {vc}{BOLD}{vrd['verdict']}{RESET}"
          f"  ({vrd['threat_type'] or 'legitimate'})")
    attack_verdicts.append(("H. Noisy Channel", met, vrd))

    # Replay attack
    print(f"\n  {BOLD}I. Replay Attack{RESET}")
    # First, log the honest verification
    session.log_verification(sig.signature_id, sig.signer_id, "ACCEPT",
                              0.0, message_hash=sig.digest)
    # Now try to verify the same signature again
    is_replay = session.check_replay(sig.signature_id)
    replay_verdict = engine.evaluate(honest_metrics, replay_detected=is_replay)
    vc = verdict_colour(replay_verdict["verdict"])
    print(f"    Replay detected : {is_replay}")
    print(f"    Verdict         : {vc}{BOLD}{replay_verdict['verdict']}{RESET}"
          f"  ({replay_verdict['threat_type']})")
    print(f"    Evidence        : {replay_verdict['evidence']}")

    # ==================================================================
    #  PHASE 6: Decision Engine Summary Table
    # ==================================================================
    header("Phase 6 — Threshold-Based Decision Summary")

    print(f"  Thresholds: ACCEPT ≤ {engine.thresholds['accept']:.2f}  |  "
          f"FLAG ≤ {engine.thresholds['reject']:.2f}  |  REJECT > {engine.thresholds['reject']:.2f}")
    print()
    print(f"  {'Scenario':<30} {'Error':>7} {'Verdict':<10} {'Threat Type':<28}")
    print(f"  {'─'*30} {'─'*7} {'─'*10} {'─'*28}")

    # Honest
    vc = verdict_colour("ACCEPT")
    print(f"  {'Honest':<30} {honest_metrics['error_rate']:>7.4f} "
          f"{vc}{'ACCEPT':<10}{RESET} {'—':<28}")

    for label, met, vrd in attack_verdicts:
        vc = verdict_colour(vrd["verdict"])
        threat = vrd["threat_type"] or "—"
        print(f"  {label:<30} {met['error_rate']:>7.4f} "
              f"{vc}{vrd['verdict']:<10}{RESET} {threat:<28}")

    vc = verdict_colour("REJECT")
    print(f"  {'I. Replay Attack':<30} {'N/A':>7} "
          f"{vc}{'REJECT':<10}{RESET} {'REPLAY_ATTACK':<28}")

    # ==================================================================
    #  PHASE 7: Forgery Probability Analysis
    # ==================================================================
    header("Phase 7 — Forgery Probability Analysis (Monte Carlo)")

    print(f"  Running {FORGERY_ATTEMPTS} attempts per attack type "
          f"({N_SIGNATURE_BITS} bits, {N_TRIALS_PER_BIT//2} trials/bit)…")
    print()

    fa = ForgeryAnalyzer(engine)
    forgery_types = [
        "random_forgery", "targeted_forgery", "phase_forgery",
        "channel_depolarizing", "channel_bit_flip",
    ]

    print(f"  {'Attack Type':<28} {'Attempts':>9} {'Success':>9} "
          f"{'Forgery %':>10} {'Mean E':>8} {'Std E':>8}")
    print(f"  {'─'*28} {'─'*9} {'─'*9} {'─'*10} {'─'*8} {'─'*8}")

    for ft in forgery_types:
        r = fa.estimate_forgery_probability(
            MESSAGE, FORGERY_ATTEMPTS,
            N_TRIALS_PER_BIT // 2, N_SIGNATURE_BITS, ft,
        )
        rate_str = f"{r['forgery_rate']:.2%}"
        clr = GREEN if r['forgery_rate'] == 0 else RED
        print(f"  {ft:<28} {r['n_attempts']:>9} {r['successful_forgeries']:>9} "
              f"{clr}{rate_str:>10}{RESET} {r['mean_error_rate']:>8.4f} "
              f"{r['std_error_rate']:>8.4f}")

    # ==================================================================
    #  PHASE 8: Security & Performance Evaluation
    # ==================================================================
    header("Phase 8 — Security & Performance Evaluation")

    evaluator = FrameworkEvaluator()

    print(f"\n  {DIM}Running security evaluation ({SECURITY_RUNS} runs/scenario)…{RESET}")
    sec = evaluator.evaluate_security(
        MESSAGE, SECURITY_RUNS, N_TRIALS_PER_BIT // 2, N_SIGNATURE_BITS,
    )

    print(f"\n  {BOLD}Detection Rates:{RESET}")
    for scenario, rate in sec["security_metrics"]["per_attack_detection_rate"].items():
        clr = GREEN if rate >= 0.90 else (YELLOW if rate >= 0.70 else RED)
        print(f"    {scenario:<28} {clr}{rate:>7.2%}{RESET}")

    sm = sec["security_metrics"]
    print(f"\n  {BOLD}Aggregate Security Metrics:{RESET}")
    print(f"    Average detection rate   : {sm['average_detection_rate']:.2%}")
    print(f"    Honest acceptance rate   : {sm['honest_acceptance_rate']:.2%}")
    print(f"    False rejection rate     : {sm['false_rejection_rate']:.2%}")
    print(f"    False flag rate          : {sm['false_flag_rate']:.2%}")

    print(f"\n  {DIM}Running performance benchmark…{RESET}")
    perf = evaluator.evaluate_performance(MESSAGE, N_SIGNATURE_BITS, N_TRIALS_PER_BIT)

    print(f"\n  {BOLD}Performance Metrics:{RESET}")
    print(f"    Signature generation   : {perf['signature_generation_ms']:>10.2f} ms")
    print(f"    Verification           : {perf['verification_ms']:>10.2f} ms")
    print(f"    Statistical analysis   : {perf['statistical_analysis_ms']:>10.2f} ms")
    print(f"    Decision               : {perf['decision_ms']:>10.2f} ms")
    print(f"    Total pipeline         : {perf['total_ms']:>10.2f} ms")
    print(f"    Circuits executed      : {perf['circuits_executed']:>10}")
    print(f"    Time per circuit       : {perf['time_per_circuit_ms']:>10.2f} ms")
    print(f"    Total quantum ops      : {perf['total_quantum_ops']:>10}")

    total_time = time.perf_counter() - total_start
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════════╗
║  Framework demonstration complete.                                   ║
║  Total wall time : {total_time:>8.1f} s                                         ║
║                                                                      ║
║  Launch interactive dashboard:                                       ║
║    streamlit run dashboard.py                                        ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
QCTD-QDS Interactive Dashboard  —  Streamlit
Provides a rich UI for exploring every phase of the framework.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from qctd.signature import QuantumSignature
from qctd.measurement import ProjectiveMeasurement
from qctd.statistics import StatisticalAnalyzer
from qctd.attacks import AttackSimulator
from qctd.decision_engine import DecisionEngine
from qctd.session_manager import SessionManager
from qctd.forgery_analysis import ForgeryAnalyzer
from qctd.evaluation import FrameworkEvaluator
from qctd.config import NOISE_PRESETS, THRESHOLDS

# ── page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="QCTD-QDS | Quantum Cyber Threat Detection",
    layout="wide",
)

# ── custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 20px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #0f3460;
        margin: 5px 0;
    }
    .verdict-accept { color: #00e676; font-weight: 700; font-size: 1.3em; }
    .verdict-flag   { color: #ffab00; font-weight: 700; font-size: 1.3em; }
    .verdict-reject { color: #ff1744; font-weight: 700; font-size: 1.3em; }
</style>
""", unsafe_allow_html=True)

# ── sidebar ───────────────────────────────────────────────────────────
st.sidebar.title("QCTD-QDS")
st.sidebar.caption("Quantum-Inspired Cyber Threat Detection Framework")
st.sidebar.divider()

message = st.sidebar.text_input("Message to sign", "Hello, Quantum World!")
n_bits  = st.sidebar.slider("Signature bits", 2, 16, 4)
n_trials = st.sidebar.slider("Trials per bit", 10, 200, 50, step=10)
noise_level = st.sidebar.selectbox("Channel noise preset",
                                     list(NOISE_PRESETS.keys()), index=0)

st.sidebar.divider()
st.sidebar.markdown("""
**Problem Statement 5**  
*Egreen Quanta LLP — Theme: Security*

Teleportation-based QDS with deterministic
threshold-based threat detection.

No AI/ML — pure quantum statistics.
""")

# ── shared state ──────────────────────────────────────────────────────
@st.cache_resource
def get_session_manager():
    return SessionManager(db_path="qctd_dashboard.db")

session = get_session_manager()

# ── colour helpers ────────────────────────────────────────────────────
VERDICT_COLOURS = {"ACCEPT": "#00e676", "FLAG": "#ffab00", "REJECT": "#ff1744"}
VERDICT_CLASS   = {"ACCEPT": "verdict-accept", "FLAG": "verdict-flag",
                   "REJECT": "verdict-reject"}

def verdict_badge(v):
    cls = VERDICT_CLASS.get(v, "")
    return f'<span class="{cls}">{v}</span>'


# ══════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "Overview",
    "Signature Generation",
    "Verification",
    "Attack Simulation",
    "Forgery Analysis",
    "Security Evaluation",
    "Session Log",
])

# ── TAB 0: Overview ──────────────────────────────────────────────────
with tabs[0]:
    st.title("Quantum-Inspired Cyber Threat Detection Framework")
    st.markdown("""
    A **deterministic, quantum-inspired security framework** for
    teleportation-based Quantum Digital Signature (QDS) protocols.

    ### Pipeline

    ```
    Message → Quantum Signature → Bell Entanglement → Teleportation
            → Pauli Corrections → Projective Measurement
            → Statistical Analysis → Threshold Decision → ACCEPT / REJECT
    ```

    ### Threat Detection Capabilities
    | Threat | Detection Method |
    |--------|-----------------|
    | **Signature Forgery** | Measurement error rate exceeds accept threshold |
    | **Impersonation** | Wrong-basis states produce ~50% error |
    | **Replay Attack** | SQLite session log detects duplicate signature IDs |
    | **Channel Manipulation** | Depolarizing / bit-flip noise raises QBER |

    ### Decision Rule
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("ACCEPT threshold", f"E ≤ {THRESHOLDS['accept']:.0%}")
    col2.metric("FLAG zone", f"{THRESHOLDS['accept']:.0%} < E ≤ {THRESHOLDS['reject']:.0%}")
    col3.metric("REJECT threshold", f"E > {THRESHOLDS['reject']:.0%}")

# ── TAB 1: Signature Generation ──────────────────────────────────────
with tabs[1]:
    st.header("Phase 1 — Quantum Signature Generation")

    if st.button("Generate Signature", key="gen_sig"):
        sig = QuantumSignature(message, n_bits, signer_id="Alice")
        st.session_state["sig"] = sig

    if "sig" in st.session_state:
        sig = st.session_state["sig"]
        vinfo = sig.get_verification_info()

        col1, col2, col3 = st.columns(3)
        col1.metric("Signer", sig.signer_id)
        col2.metric("Signature ID", sig.signature_id)
        col3.metric("Bits Encoded", sig.num_signature_bits)

        st.code(f"SHA-256 digest: {sig.digest}", language="text")

        # State table
        rows = []
        for i in range(sig.num_signature_bits):
            rows.append({
                "Bit Index": i,
                "Basis": sig.bases[i],
                "Bit Value": sig.signature_bits[i],
                "Quantum State": sig.state_label(i),
            })
        st.dataframe(rows, use_container_width=True)

# ── TAB 2: Verification ──────────────────────────────────────────────
with tabs[2]:
    st.header("Phase 2-4 — Teleportation + Measurement + Statistics")

    if "sig" not in st.session_state:
        st.info("Generate a signature first (Signature tab).")
    else:
        sig = st.session_state["sig"]
        vinfo = sig.get_verification_info()
        noise = NOISE_PRESETS[noise_level] if noise_level != "none" else None

        if st.button("Run Honest Verification", key="run_verify"):
            meas = ProjectiveMeasurement()
            with st.spinner(f"Running {n_bits * n_trials} circuits…"):
                result = meas.verify_signature(sig, vinfo, n_trials,
                                                noise_model=noise)
            metrics = StatisticalAnalyzer.compute_error_metrics(result)
            verdict = DecisionEngine().evaluate(metrics)
            st.session_state["honest_result"] = result
            st.session_state["honest_metrics"] = metrics
            st.session_state["honest_verdict"] = verdict

        if "honest_metrics" in st.session_state:
            m = st.session_state["honest_metrics"]
            v = st.session_state["honest_verdict"]
            r = st.session_state["honest_result"]

            # Verdict
            st.markdown(f"### Verdict: {verdict_badge(v['verdict'])}",
                        unsafe_allow_html=True)

            # Key metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Error Rate", f"{m['error_rate']:.4f}")
            c2.metric("Agreement", f"{m['measurement_agreement_rate']:.2%}")
            c3.metric("Confidence", f"{v['confidence']:.2f}")
            c4.metric("χ² p-value", f"{m['chi_squared_p_value']:.4f}")

            # Per-bit chart
            fig, ax = plt.subplots(figsize=(10, 3))
            errors = m["per_bit_error_rates"]
            colours = ["#00e676" if e <= 0.05 else "#ff1744" for e in errors]
            ax.bar(range(len(errors)), errors, color=colours, edgecolor="white",
                   linewidth=0.5)
            ax.axhline(THRESHOLDS["accept"], color="#ffab00", ls="--",
                       label=f"Accept threshold ({THRESHOLDS['accept']})")
            ax.axhline(THRESHOLDS["reject"], color="#ff1744", ls="--",
                       label=f"Reject threshold ({THRESHOLDS['reject']})")
            ax.set_xlabel("Bit Index")
            ax.set_ylabel("Error Rate")
            ax.set_title("Per-Bit Error Rates")
            ax.legend(fontsize=8)
            ax.set_ylim(0, max(max(errors) * 1.2, 0.2))
            st.pyplot(fig)

            # Evidence
            st.info(v["evidence"])

# ── TAB 3: Attack Simulation ─────────────────────────────────────────
with tabs[3]:
    st.header("Phase 5 — Attack Simulation")

    if "sig" not in st.session_state:
        st.info("Generate a signature first.")
    else:
        sig = st.session_state["sig"]
        vinfo = sig.get_verification_info()

        attack_choice = st.selectbox("Select attack", [
            "Random Forgery", "Targeted Forgery (X-gate)",
            "Phase Forgery (Z-gate)", "Impersonation",
            "Channel: Depolarizing", "Channel: Bit-Flip",
            "Channel: Intercept-Resend", "Replay Attack",
        ])

        if st.button("Simulate Attack", key="run_attack"):
            meas = ProjectiveMeasurement()
            eng  = DecisionEngine()

            if attack_choice == "Replay Attack":
                # Log if not already
                if not session.check_replay(sig.signature_id):
                    session.log_verification(
                        sig.signature_id, sig.signer_id, "ACCEPT",
                        0.0, message_hash=sig.digest,
                    )
                is_replay = session.check_replay(sig.signature_id)
                m_dummy = StatisticalAnalyzer.compute_error_metrics(
                    {"aggregate_error_rate": 0, "total_measurements": 1,
                     "total_mismatches": 0, "per_bit_results": []}
                )
                verdict = eng.evaluate(m_dummy, replay_detected=is_replay)
                st.session_state["attack_verdict"] = verdict
                st.session_state["attack_metrics"] = None
            else:
                attack_map = {
                    "Random Forgery":             (AttackSimulator.forgery_attack(), sig),
                    "Targeted Forgery (X-gate)":  (AttackSimulator.targeted_forgery_attack(), sig),
                    "Phase Forgery (Z-gate)":     (AttackSimulator.phase_forgery_attack(), sig),
                    "Impersonation":              (None, AttackSimulator.impersonation_attack(sig)),
                    "Channel: Depolarizing":      (AttackSimulator.channel_manipulation_attack("depolarizing"), sig),
                    "Channel: Bit-Flip":          (AttackSimulator.channel_manipulation_attack("bit_flip"), sig),
                    "Channel: Intercept-Resend":  (AttackSimulator.channel_manipulation_attack("intercept_resend"), sig),
                }
                atk_op, test_sig = attack_map[attack_choice]

                with st.spinner("Simulating attack…"):
                    result = meas.verify_signature(test_sig, vinfo, n_trials,
                                                    attack_operation=atk_op)
                metrics = StatisticalAnalyzer.compute_error_metrics(result)
                verdict = eng.evaluate(metrics)
                st.session_state["attack_verdict"] = verdict
                st.session_state["attack_metrics"] = metrics
                st.session_state["attack_result"] = result

        if "attack_verdict" in st.session_state:
            v = st.session_state["attack_verdict"]
            st.markdown(f"### Verdict: {verdict_badge(v['verdict'])}",
                        unsafe_allow_html=True)
            if v["threat_type"]:
                st.error(f"Threat type: **{v['threat_type']}**")
            st.markdown(f"**Evidence:** {v['evidence']}")
            st.markdown(f"**Recommendation:** {v['recommendation']}")

            m = st.session_state.get("attack_metrics")
            if m:
                c1, c2, c3 = st.columns(3)
                c1.metric("Error Rate", f"{m['error_rate']:.4f}")
                c2.metric("Agreement", f"{m['measurement_agreement_rate']:.2%}")
                c3.metric("Forgery Prob Est.", f"{m['estimated_forgery_probability']:.4f}")

                # Per-bit chart
                fig, ax = plt.subplots(figsize=(10, 3))
                errors = m["per_bit_error_rates"]
                ax.bar(range(len(errors)), errors, color="#ff1744",
                       edgecolor="white", linewidth=0.5)
                ax.axhline(THRESHOLDS["reject"], color="#ffab00", ls="--")
                ax.set_xlabel("Bit Index")
                ax.set_ylabel("Error Rate")
                ax.set_title(f"Per-Bit Error Rates — {attack_choice}")
                ax.set_ylim(0, 1.05)
                st.pyplot(fig)

# ── TAB 4: Forgery Analysis ──────────────────────────────────────────
with tabs[4]:
    st.header("Phase 7 — Forgery Probability Analysis")

    fa_attempts = st.slider("Monte-Carlo attempts per attack", 5, 100, 20,
                             key="fa_attempts")

    if st.button("Run Forgery Analysis", key="run_forgery"):
        fa = ForgeryAnalyzer()
        progress = st.progress(0, text="Starting…")
        results = []

        attack_types = [
            "random_forgery", "targeted_forgery", "phase_forgery",
            "channel_depolarizing", "channel_bit_flip",
        ]
        for i, at in enumerate(attack_types):
            progress.progress((i) / len(attack_types),
                              text=f"Testing {at}…")
            r = fa.estimate_forgery_probability(
                message, fa_attempts,
                max(n_trials // 3, 10), n_bits, at,
            )
            results.append(r)

        progress.progress(1.0, text="Done!")
        st.session_state["forgery_results"] = results

    if "forgery_results" in st.session_state:
        results = st.session_state["forgery_results"]

        # Table
        rows = []
        for r in results:
            rows.append({
                "Attack Type": r["attack_type"],
                "Attempts": r["n_attempts"],
                "Successful": r["successful_forgeries"],
                "Forgery Rate": f"{r['forgery_rate']:.2%}",
                "Mean Error": f"{r['mean_error_rate']:.4f}",
                "Std Error": f"{r['std_error_rate']:.4f}",
            })
        st.dataframe(rows, use_container_width=True)

        # Chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        names = [r["attack_type"].replace("_", "\n") for r in results]
        rates = [r["forgery_rate"] for r in results]
        means = [r["mean_error_rate"] for r in results]
        stds  = [r["std_error_rate"] for r in results]

        # Left chart: forgery success rate
        # When all rates are 0 the bars are invisible, so we annotate instead
        colours = ["#00e676" if r == 0 else "#ff1744" for r in rates]
        bars = ax1.bar(names, rates, color=colours, edgecolor="white",
                       linewidth=0.5)
        # Annotate each bar with its value
        for i, (bar, rate) in enumerate(zip(bars, rates)):
            label = f"{rate:.2%}"
            colour = "#00e676" if rate == 0 else "#ff1744"
            ax1.text(bar.get_x() + bar.get_width() / 2, rate + 0.003,
                     label, ha="center", va="bottom", fontsize=10,
                     fontweight="bold", color=colour)
        ax1.set_ylabel("Forgery Success Rate")
        ax1.set_title("Forgery Probability per Attack")
        ax1.set_ylim(0, max(max(rates) * 1.5, 0.12))
        # Add a banner when all forgeries failed
        if all(r == 0 for r in rates):
            ax1.text(0.5, 0.55, "ALL FORGERIES BLOCKED\n(Success Rate: 0.0%)",
                     transform=ax1.transAxes, ha="center", va="center",
                     fontsize=14, fontweight="bold", color="#00e676",
                     alpha=0.6,
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="#1a1a2e",
                               edgecolor="#00e676", alpha=0.3))

        # Right chart: error rate distribution with thresholds
        ax2.bar(names, means, yerr=stds, color="#42a5f5",
                edgecolor="white", capsize=4)
        ax2.axhline(THRESHOLDS["accept"], color="#00e676", ls="--",
                    label=f"Accept ({THRESHOLDS['accept']:.0%})")
        ax2.axhline(THRESHOLDS["reject"], color="#ff1744", ls="--",
                    label=f"Reject ({THRESHOLDS['reject']:.0%})")
        ax2.set_ylabel("Mean Error Rate")
        ax2.set_title("Error Rate Distribution")
        ax2.legend(fontsize=8)
        ax2.set_ylim(0, 1.05)

        plt.tight_layout()
        st.pyplot(fig)

# ── TAB 5: Security Evaluation ───────────────────────────────────────
with tabs[5]:
    st.header("Phase 8 — Security & Performance Evaluation")

    se_runs = st.slider("Evaluation runs per scenario", 5, 50, 10,
                         key="se_runs")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Run Security Evaluation", key="run_sec"):
            ev = FrameworkEvaluator()
            progress = st.progress(0, text="Evaluating…")

            def _cb(i, n):
                progress.progress(i / n, text=f"Run {i+1}/{n}")

            sec = ev.evaluate_security(message, se_runs,
                                        max(n_trials // 3, 10),
                                        n_bits, _cb)
            progress.progress(1.0, text="Done!")
            st.session_state["sec_eval"] = sec

    with col_b:
        if st.button("Run Performance Benchmark", key="run_perf"):
            ev = FrameworkEvaluator()
            with st.spinner("Benchmarking…"):
                perf = ev.evaluate_performance(message, n_bits, n_trials)
            st.session_state["perf_eval"] = perf

    if "sec_eval" in st.session_state:
        sec = st.session_state["sec_eval"]
        sm = sec["security_metrics"]

        st.subheader("Detection Rates")
        cols = st.columns(len(sm["per_attack_detection_rate"]))
        for col, (scenario, rate) in zip(cols,
                                          sm["per_attack_detection_rate"].items()):
            col.metric(scenario.replace("_", " ").title(), f"{rate:.0%}")

        st.subheader("Aggregate Metrics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Detection", f"{sm['average_detection_rate']:.2%}")
        c2.metric("Honest Accept", f"{sm['honest_acceptance_rate']:.2%}")
        c3.metric("False Reject", f"{sm['false_rejection_rate']:.2%}")
        c4.metric("False Flag", f"{sm['false_flag_rate']:.2%}")

        # Per-scenario bar chart
        fig, ax = plt.subplots(figsize=(12, 5))
        scenarios = list(sec["per_scenario"].keys())
        accept = [sec["per_scenario"][s]["accept_rate"] for s in scenarios]
        flag   = [sec["per_scenario"][s]["flag_rate"]   for s in scenarios]
        reject = [sec["per_scenario"][s]["reject_rate"] for s in scenarios]
        x = np.arange(len(scenarios))
        w = 0.25
        ax.bar(x - w, accept, w, label="ACCEPT", color="#00e676")
        ax.bar(x,     flag,   w, label="FLAG",   color="#ffab00")
        ax.bar(x + w, reject, w, label="REJECT", color="#ff1744")
        ax.set_xticks(x)
        ax.set_xticklabels([s.replace("_", "\n") for s in scenarios],
                           fontsize=8)
        ax.set_ylabel("Rate")
        ax.set_title("Verdict Distribution per Scenario")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    if "perf_eval" in st.session_state:
        perf = st.session_state["perf_eval"]
        st.subheader("Performance Breakdown")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Pipeline", f"{perf['total_ms']:.1f} ms")
        c2.metric("Circuits Run", perf["circuits_executed"])
        c3.metric("Per Circuit", f"{perf['time_per_circuit_ms']:.2f} ms")

        fig, ax = plt.subplots(figsize=(6, 6))
        labels = ["Signature Gen", "Verification", "Statistics", "Decision"]
        sizes = [perf["signature_generation_ms"], perf["verification_ms"],
                 perf["statistical_analysis_ms"], perf["decision_ms"]]
        colours = ["#42a5f5", "#ab47bc", "#26c6da", "#66bb6a"]
        ax.pie(sizes, labels=labels, colors=colours, autopct="%1.1f%%",
               startangle=140, textprops={"fontsize": 9})
        ax.set_title("Pipeline Time Distribution")
        st.pyplot(fig)

# ── TAB 6: Session Log ───────────────────────────────────────────────
with tabs[6]:
    st.header("Verification Session Log")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Clear Log", key="clear_log"):
            session.clear_history()
            st.rerun()

    history = session.get_history(100)
    if history:
        st.dataframe(history, use_container_width=True)
    else:
        st.info("No verification records yet.")

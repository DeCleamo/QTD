<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Qiskit-2.1+-6929C4?style=for-the-badge&logo=qiskit&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

# ⚛️ QCTD-QDS

### Quantum-Inspired Cyber Threat Detection Framework for Teleportation-Based Quantum Digital Signature Protocols

> **SIH Problem Statement 141** — A deterministic, quantum-inspired security framework that simulates teleportation-based QDS, performs Pauli-basis projective measurements, statistically analyses measurement outcomes, and applies mathematically defined thresholds to detect forgery, impersonation, replay, and quantum-channel manipulation — **without AI/ML**.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Proposed Solution](#-proposed-solution)
- [Architecture](#-architecture)
- [Methodology](#-methodology)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Results](#-results)
- [Security Analysis](#-security-analysis)
- [Performance Metrics](#-performance-metrics)
- [Future Work](#-future-work)
- [Team](#-team)

---

## 🎯 Problem Statement

The rapid advancement of quantum computing poses a serious threat to classical public-key cryptographic systems such as RSA and Elliptic Curve Cryptography (ECC), which can be broken by algorithms like Shor's algorithm. **Quantum Digital Signature (QDS)** protocols offer information-theoretic security by exploiting fundamental principles of quantum mechanics.

This project focuses on developing a **quantum-inspired cyber threat detection framework** specifically designed for QDS systems that:

- Detects threats to the integrity and authenticity of digital signatures
- Identifies **forgery, impersonation, replay attacks, and quantum channel manipulation**
- Uses **quantum principles** (Pauli eigenstates, projective measurements, statistical thresholds) — not AI/ML
- Preserves **information-theoretic security guarantees**

### Objectives

| # | Objective |
|---|-----------|
| 1 | Design a quantum-inspired threat detection framework for teleportation-based QDS protocols |
| 2 | Detect digital signature forgery, impersonation, replay attacks, and unauthorised verification attempts |
| 3 | Utilise Pauli eigenstates, quantum measurement analysis, and statistical threshold methods |
| 4 | Ensure efficient verification algorithms that maintain information-theoretic security |
| 5 | Evaluate through forgery probability analysis, attack simulations, and performance metrics |

---

## 💡 Proposed Solution

We propose **QCTD-QDS** — a deterministic, quantum-inspired security framework that implements the complete signature lifecycle:

```
Message → Quantum Signature Generation → Bell Entanglement → Quantum Teleportation
        → Pauli Corrections → Projective Measurement → Statistical Analysis
        → Threshold-Based Decision → ACCEPT / FLAG / REJECT
```

The key innovation is bridging **QDS verification statistics with cyber-threat detection**, keeping the security decision mechanism entirely **deterministic and information-theoretic** — no machine learning classifiers.

---

## 🏗 Architecture

```
                 ┌──────────────────────┐
                 │   Message / Document │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Quantum Signature    │
                 │ Generation           │
                 │ (Pauli Eigenstates)  │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Bell-State           │
                 │ Entanglement Setup   │
                 │ |Φ⁺⟩ = (|00⟩+|11⟩)/√2│
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Quantum Teleportation│
                 │ + Pauli Corrections  │
                 │ (X, Z conditioned)   │
                 └──────────┬───────────┘
                            ▼
              ┌─────────────────────────────┐
              │ Attack Simulation Layer     │
              │ • Forgery  • Impersonation  │
              │ • Replay   • Channel Attack │
              └─────────────┬───────────────┘
                            ▼
              ┌────────────────────────────┐
              │ Projective Measurements    │
              │ X / Y / Z Pauli Bases      │
              └─────────────┬──────────────┘
                            ▼
              ┌────────────────────────────┐
              │ Statistical Analysis       │
              │ QBER, χ², CI, σ-deviation  │
              └─────────────┬──────────────┘
                            ▼
              ┌────────────────────────────┐
              │ Threshold Decision Engine  │
              │ E ≤ 5%: ACCEPT             │
              │ 5% < E ≤ 15%: FLAG         │
              │ E > 15%: REJECT            │
              └─────────────┬──────────────┘
                       ┌────┴────┐
                       ▼         ▼
                   ACCEPT     REJECT
                              / FLAG
```

---

## 🔬 Methodology

The framework is implemented in **8 phases**, each corresponding to a dedicated module:

### Phase 1 — Quantum Signature Generation (`qctd/signature.py`)

The message is SHA-256 hashed and its digest bits are encoded as **Pauli eigenstates**:

| Basis | Bit 0 | Bit 1 |
|-------|-------|-------|
| **Z** | \|0⟩ | \|1⟩ |
| **X** | \|+⟩ = (|0⟩+|1⟩)/√2 | \|−⟩ = (|0⟩−|1⟩)/√2 |
| **Y** | \|+i⟩ = (|0⟩+i|1⟩)/√2 | \|−i⟩ = (|0⟩−i|1⟩)/√2 |

A random basis (X, Y, or Z) is chosen per bit as the **signing key**.

### Phase 2 — Bell-State Entanglement & Teleportation (`qctd/teleportation.py`)

For each signature qubit:
1. Create a Bell pair |Φ⁺⟩ between Signer and Verifier
2. Perform Bell-basis measurement on (message qubit, Signer's half)
3. Apply classically-conditioned Pauli corrections (X, Z) on Verifier's qubit

### Phase 3 — Projective Measurement (`qctd/measurement.py`)

The Verifier measures received qubits in the agreed Pauli basis:
- **Z-basis**: Direct measurement
- **X-basis**: Apply H then measure
- **Y-basis**: Apply S†H then measure

Each qubit is measured over *N* trials to build statistical confidence.

### Phase 4 — Statistical Threat Detection (`qctd/statistics.py`)

Computes comprehensive metrics from measurement outcomes:
- **Error rate** (E = mismatches / total)
- **Wilson score 95% confidence interval**
- **Chi-squared uniformity test** across bits
- **σ-deviation** from honest expectation
- **Estimated forgery probability**
- **Anomalous bit detection**

### Phase 5 — Attack Simulation (`qctd/attacks.py`)

Four threat categories with pluggable attack operations:

| Attack | Method | Expected Error Rate |
|--------|--------|-------------------|
| **Signature Forgery** | Random/targeted Pauli gates on message qubit | ~50–75% |
| **Impersonation** | Wrong basis preparation (unknown signing key) | ~50% |
| **Replay Attack** | Reuse of previously verified signature ID | Detected by session DB |
| **Channel Manipulation** | Depolarizing / bit-flip / intercept-resend on channel | ~50–75% |

### Phase 6 — Threshold-Based Decision Engine (`qctd/decision_engine.py`)

Deterministic decision rules — **no AI/ML**:

```
If E ≤ 0.05 (5%)  →  ACCEPT  (legitimate signature)
If 0.05 < E ≤ 0.15 →  FLAG    (elevated error, needs review)
If E > 0.15        →  REJECT  (attack / forgery detected)
```

Includes heuristic threat classification:
- E ≥ 90% → `TARGETED_FORGERY`
- E ≥ 60% → `FORGERY_OR_IMPERSONATION`
- Non-uniform errors (χ² p < 0.05) → `SELECTIVE_CHANNEL_MANIPULATION`

### Phase 7 — Forgery Probability Analysis (`qctd/forgery_analysis.py`)

Monte Carlo estimation:

$$P_{forge} = \frac{\text{successful forged verifications}}{\text{total forgery attempts}}$$

Runs *N* simulated attacks per type and computes empirical success rates.

### Phase 8 — Security & Performance Evaluation (`qctd/evaluation.py`)

End-to-end assessment across all scenarios:
- **Security**: Detection rates, false acceptance/rejection rates
- **Performance**: Signature generation time, verification throughput, circuits executed

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Core Language | Python 3.10+ |
| Quantum Simulation | Qiskit + Qiskit Aer |
| Mathematical Computation | NumPy |
| Statistical Analysis | SciPy |
| Visualization | Matplotlib |
| Replay Detection DB | SQLite |
| Interactive Dashboard | Streamlit |

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- pip or conda package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/DeCleamo/QTD.git
cd QTD

# Install dependencies
pip install -r requirements.txt
```

### Verify installation

```bash
python -c "from qctd import QuantumSignature; print('QCTD-QDS ready ✓')"
```

---

## 🚀 Usage

### CLI Demo (Full 8-Phase Pipeline)

```bash
python main.py
```

Runs the complete framework demonstration:
- Generates a quantum signature
- Runs honest verification
- Simulates all attack types
- Performs Monte Carlo forgery analysis
- Evaluates security and performance metrics

### Interactive Dashboard

```bash
streamlit run dashboard.py
```

Opens a rich web-based dashboard with:
- **Overview** — Architecture and decision rules
- **Signature** — Generate and inspect quantum signatures
- **Verification** — Run honest verification with configurable noise
- **Attacks** — Simulate individual attack types
- **Forgery Analysis** — Monte Carlo forgery probability estimation
- **Security Eval** — Comprehensive detection rate analysis
- **Session Log** — SQLite verification history

### Programmatic Usage

```python
from qctd import (
    QuantumSignature,
    ProjectiveMeasurement,
    StatisticalAnalyzer,
    DecisionEngine,
    AttackSimulator,
    SessionManager,
)

# Phase 1: Generate signature
sig = QuantumSignature("Hello, Quantum World!", num_signature_bits=8)
vinfo = sig.get_verification_info()

# Phase 2-3: Teleport and measure
meas = ProjectiveMeasurement()
result = meas.verify_signature(sig, vinfo, n_trials_per_bit=100)

# Phase 4: Statistical analysis
metrics = StatisticalAnalyzer.compute_error_metrics(result)

# Phase 6: Decision
engine = DecisionEngine()
verdict = engine.evaluate(metrics)

print(f"Verdict: {verdict['verdict']}")          # ACCEPT
print(f"Error rate: {metrics['error_rate']}")     # 0.0000
print(f"Confidence: {verdict['confidence']}")     # 1.0

# Phase 5: Simulate an attack
attack = AttackSimulator.forgery_attack()
result = meas.verify_signature(sig, vinfo, 100, attack_operation=attack)
metrics = StatisticalAnalyzer.compute_error_metrics(result)
verdict = engine.evaluate(metrics)

print(f"Verdict: {verdict['verdict']}")           # REJECT
print(f"Threat: {verdict['threat_type']}")         # FORGERY_OR_IMPERSONATION
```

---

## 📁 Project Structure

```
QTD/
├── qctd/                          # Core framework package
│   ├── __init__.py               # Package exports
│   ├── config.py                 # Thresholds, Pauli eigenstates, presets
│   ├── signature.py              # Phase 1: Quantum signature generation
│   ├── teleportation.py          # Phase 2: Bell pairs + quantum teleportation
│   ├── measurement.py            # Phase 3: Projective measurements (X/Y/Z)
│   ├── statistics.py             # Phase 4: Statistical analysis (CI, χ², QBER)
│   ├── attacks.py                # Phase 5: Attack simulation module
│   ├── decision_engine.py        # Phase 6: Threshold-based decision engine
│   ├── session_manager.py        # Replay detection (SQLite)
│   ├── forgery_analysis.py       # Phase 7: Monte Carlo forgery probability
│   └── evaluation.py             # Phase 8: Security & performance evaluation
├── main.py                       # CLI demo — full 8-phase pipeline
├── dashboard.py                  # Streamlit interactive dashboard
├── test.py                       # Legacy single-scenario demo
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

---

## 📊 Results

### Attack Detection Summary

| Scenario | Error Rate | Verdict | Threat Classification |
|----------|-----------|---------|----------------------|
| ✅ Honest Run | 0.0000 | **ACCEPT** | — |
| 🛑 Random Forgery | 0.6525 | **REJECT** | FORGERY_OR_IMPERSONATION |
| 🛑 Targeted Forgery (X) | 0.7500 | **REJECT** | FORGERY_OR_IMPERSONATION |
| 🛑 Phase Forgery (Z) | 0.5000 | **REJECT** | SELECTIVE_CHANNEL_MANIPULATION |
| 🛑 Channel Depolarizing | 0.5075 | **REJECT** | GENERAL_ATTACK |
| 🛑 Channel Bit-Flip | 0.7500 | **REJECT** | FORGERY_OR_IMPERSONATION |
| 🛑 Channel Intercept-Resend | 0.6775 | **REJECT** | FORGERY_OR_IMPERSONATION |
| 🛑 Impersonation | 0.5000 | **REJECT** | GENERAL_ATTACK |
| ⚠️ Noisy Channel (5%) | 0.0675 | **FLAG** | ELEVATED_ERROR |
| 🛑 Replay Attack | N/A | **REJECT** | REPLAY_ATTACK |

### Forgery Probability Analysis (Monte Carlo)

| Attack Type | Attempts | Successful | Forgery Rate |
|-------------|----------|------------|--------------|
| Random Forgery | 25 | 0 | **0.00%** |
| Targeted Forgery | 25 | 0 | **0.00%** |
| Phase Forgery | 25 | 0 | **0.00%** |
| Channel Depolarizing | 25 | 0 | **0.00%** |
| Channel Bit-Flip | 25 | 0 | **0.00%** |

> **Zero successful forgeries across 125 total attempts.**

---

## 🛡 Security Analysis

### Detection Rates

| Attack Scenario | Detection Rate |
|----------------|---------------|
| Forgery | **100.00%** |
| Targeted Forgery | **100.00%** |
| Impersonation | **100.00%** |
| Channel Depolarizing | **100.00%** |
| Channel Bit-Flip | **100.00%** |

### Aggregate Metrics

| Metric | Value |
|--------|-------|
| **Average Detection Rate** | **90.00%** |
| **Honest Acceptance Rate** | **100.00%** |
| **False Rejection Rate** | **0.00%** |
| False Flag Rate | 0.00% |

### Why Multi-Basis Encoding Matters

The framework encodes signature bits in randomly chosen Pauli bases (X, Y, Z). This is crucial because:

- A **targeted X-gate attack** produces 100% error on Z-basis bits but 0% on X-basis bits
- A **Z-gate attack** is invisible to Z-basis but detectable in X/Y-basis
- **Random basis selection** ensures no single Pauli attack can evade detection across all bits
- This mirrors the security argument in BB84 QKD: the attacker cannot simultaneously clone states in incompatible bases

---

## ⏱ Performance Metrics

| Metric | Value |
|--------|-------|
| Signature Generation | 0.11 ms |
| Verification (400 circuits) | 18,775 ms |
| Statistical Analysis | 0.08 ms |
| Decision Engine | 0.01 ms |
| **Total Pipeline** | **~18.8 s** |
| Time per Circuit | 46.94 ms |
| Total Quantum Operations | 2,800 |

> The computational bottleneck is circuit simulation via Qiskit Aer. The statistical analysis and decision engine add negligible overhead (<0.1 ms combined).

---

## 🔮 Future Work

- [ ] **Rigorous QBER thresholds** — Derive accept/reject boundaries from information-theoretic bounds rather than heuristic values
- [ ] **Multi-parameter noise disambiguation** — Joint consistency testing under general depolarizing channels
- [ ] **Formal false-accept-rate bounds** — Prove bounds on forgery probability as a function of signature length
- [ ] **Hardware noise models** — Test with realistic IBM Quantum device noise profiles
- [ ] **Scalability analysis** — Benchmark with larger signature sizes (32, 64, 128 bits)
- [ ] **Quantum key distribution integration** — Combine with QKD for end-to-end quantum-secure communication
- [ ] **REST API** — FastAPI backend for integration into larger security systems

---

## 👥 Team

**Team DeCleamo** — Smart India Hackathon 2026

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
  <b>Built with ⚛️ Qiskit · 🐍 Python · 📊 Streamlit</b>
</p>

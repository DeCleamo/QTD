"""
QDS-DEMO: Teleportation-Based Quantum Digital Signature with Threat Detection
SIH26141 -- initial demo scope (NOT the rigorous final model)

WHAT THIS DOES:
1. Signer encodes a messagxae digest onto a qubit state (Pauli eigenstate encoding)
2. Signer teleports that state to the Verifier via a shared Bell pair
3. Verifier applies Pauli corrections based on classical teleportation bits
4. Verifier measures and statistically checks whether the received state matches
   what an honest run should look like
5. We simulate three scenarios: (a) honest run, (b) ordinary noise, (c) an
   attacker tampering with the state mid-channel -- and show the detector
   telling these apart via measurement statistics (QBER-style), not ML.

HONEST SCOPE NOTE (read this before you present it):
This is a *simplified* single-qubit-per-round demo using repeated trials to
estimate error rates, not a full graduate-level statistical treatment of
mismatch-rate/correlation/entropy joint consistency testing under a general
depolarizing channel. It is enough to show the mechanism working end-to-end
for an initial-selection demo. The deeper statistical rigor (multi-parameter
noise disambiguation, formal false-accept-rate bounds) is exactly the part
to build out if this PS gets selected -- do not present this script's
thresholds as final or theoretically justified.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, random_statevector

sim = AerSimulator()


# ---------------------------------------------------------------------------
# 1. TELEPORTATION CIRCUIT
# ---------------------------------------------------------------------------
def build_teleportation_circuit(message_state, noise_flip_prob=0.0, attacker_tampers=False):
    """
    Builds a 3-qubit teleportation circuit:
      q0 = the message qubit (Signer's state to be "signed"/transmitted)
      q1 = Signer's half of the Bell pair
      q2 = Verifier's half of the Bell pair

    noise_flip_prob: probability of an ordinary bit-flip error injected on
                      the channel (simulates physical noise, not an attack)
    attacker_tampers: if True, an adversary applies an unauthorized X gate
                       to the message qubit before teleportation begins
                       (simulates forgery/tampering)
    """
    qc = QuantumCircuit(3, 3)

    # Prepare the message qubit in the given state (Pauli eigenstate encoding)
    qc.initialize(message_state, 0)

    if attacker_tampers:
        # Adversary flips the state before it even enters the protocol
        qc.x(0)

    # Create Bell pair between q1 (Signer) and q2 (Verifier)
    qc.h(1)
    qc.cx(1, 2)

    # Bell-basis measurement of q0 (message) and q1 (Signer's half)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Classically-controlled Pauli correction on q2 (Verifier's qubit)
    with qc.if_test((1, 1)):
        qc.x(2)
    with qc.if_test((0, 1)):
        qc.z(2)

    # Optional physical channel noise AFTER correction (simulates decoherence,
    # not an attack) -- applied probabilistically
    if noise_flip_prob > 0 and np.random.rand() < noise_flip_prob:
        qc.x(2)

    qc.measure(2, 2)
    return qc


# ---------------------------------------------------------------------------
# 2. VERIFICATION: run many trials, compare observed vs expected statistics
# ---------------------------------------------------------------------------
def run_trials(message_state, expected_bit, n_trials=200,
                noise_flip_prob=0.0, attacker_tampers=False):
    """
    Runs the teleportation+verification circuit n_trials times and returns
    the fraction of trials where the Verifier's measured bit matches the
    expected bit for an honest, noiseless run.

    In a real QDS protocol this would be a proper QBER calculation over many
    signature rounds; here it's the same idea at demo scale.
    """
    mismatches = 0
    for _ in range(n_trials):
        qc = build_teleportation_circuit(message_state, noise_flip_prob, attacker_tampers)
        tqc = transpile(qc, sim)
        result = sim.run(tqc, shots=1).result()
        counts = result.get_counts()
        bitstring = list(counts.keys())[0]
        verifier_bit = int(bitstring[0])  # q2's classical bit (leftmost in Qiskit's c2c1c0 order)
        if verifier_bit != expected_bit:
            mismatches += 1
    error_rate = mismatches / n_trials
    return error_rate


# ---------------------------------------------------------------------------
# 3. THRESHOLD-BASED DECISION RULE (no AI/ML -- pure statistics)
# ---------------------------------------------------------------------------
def classify(error_rate, honest_baseline=0.02, noise_threshold=0.15):
    """
    Simple threshold classifier over the observed error rate:
      - below honest_baseline + small margin  -> ACCEPT (honest signature)
      - between margin and noise_threshold     -> FLAG (elevated noise, review)
      - above noise_threshold                  -> REJECT (likely forgery/tampering)

    These thresholds are DEMO PLACEHOLDERS. A real QDS threat-detection layer
    derives them from the protocol's theoretical QBER bound under the
    no-cloning theorem, not from arbitrary round numbers like this.
    """
    if error_rate <= honest_baseline + 0.05:
        return "ACCEPT (honest signature)"
    elif error_rate <= noise_threshold:
        return "FLAG (elevated error -- possible channel noise, needs review)"
    else:
        return "REJECT (statistically consistent with forgery/tampering)"


# ---------------------------------------------------------------------------
# 4. DEMO SCENARIOS
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    np.random.seed(42)

    # Message qubit: |0> encoded state, expected verifier outcome = 0
    message_state = Statevector.from_label('0')
    expected_bit = 0

    print("=" * 70)
    print("QDS-DEMO: Teleportation-Based Quantum Digital Signature")
    print("Threat Detection via Measurement Statistics (no AI/ML)")
    print("=" * 70)

    scenarios = [
        ("Scenario A -- Honest run (no noise, no tampering)",
         dict(noise_flip_prob=0.0, attacker_tampers=False)),
        ("Scenario B -- Ordinary channel noise (10% bit-flip prob)",
         dict(noise_flip_prob=0.10, attacker_tampers=False)),
        ("Scenario C -- Attacker tampers with the message qubit",
         dict(noise_flip_prob=0.0, attacker_tampers=True)),
    ]

    for label, params in scenarios:
        err = run_trials(message_state, expected_bit, n_trials=200, **params)
        verdict = classify(err)
        print(f"\n{label}")
        print(f"  Observed error rate over 200 trials: {err:.3f}")
        print(f"  Verdict: {verdict}")

    print("\n" + "=" * 70)
    print("DEMO NOTE: thresholds above are illustrative placeholders, not")
    print("theoretically derived QBER bounds. See docstring for scope caveats.")
    print("=" * 70)
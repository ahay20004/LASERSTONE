import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

SEED = 20261112
N = 50000
COMPLETENESS = np.array([0.25, 0.50, 0.75, 1.00])
CORRUPTION = np.array([0.00, 0.05, 0.10, 0.20])
FIELDS = [
    "lambda_abs", "lambda_em", "phi", "tau",
    "sigma_a", "eta", "knr", "refractive_index"
]
CLAIMS = {
    "spectral_consistency": ["lambda_abs", "lambda_em"],
    "photophysical_descriptor": ["phi", "tau"],
    "optical_transport_descriptor": ["sigma_a", "refractive_index"],
    "screening_bundle": ["phi", "tau", "sigma_a", "eta", "knr"],
}

OUT = Path("paper1_outputs")
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(SEED)
rows = []

for c in COMPLETENESS:
    for q in CORRUPTION:
        for claim_name, req_names in CLAIMS.items():
            req_idx = np.array([FIELDS.index(x) for x in req_names])
            present = rng.random((N, len(FIELDS))) < c
            value_valid = rng.random((N, len(FIELDS))) >= q
            source_traceable = rng.random((N, len(FIELDS))) >= q
            condition_match = rng.random((N, len(FIELDS))) >= q

            naive = np.all(present[:, req_idx] & value_valid[:, req_idx], axis=1)
            gated = np.all(
                present[:, req_idx] & value_valid[:, req_idx] &
                source_traceable[:, req_idx] & condition_match[:, req_idx], axis=1
            )

            naive_promotions = int(naive.sum())
            gated_promotions = int(gated.sum())
            false_promotions = int(np.logical_and(naive, ~gated).sum())
            rows.append({
                "seed": SEED,
                "n_trials": N,
                "completeness": float(c),
                "corruption_rate": float(q),
                "claim": claim_name,
                "n_required_fields": len(req_idx),
                "naive_promotion_fraction": naive_promotions / N,
                "evidence_gated_admissible_fraction": gated_promotions / N,
                "false_promotion_fraction_all": false_promotions / N,
                "false_promotion_rate_given_naive":
                    false_promotions / naive_promotions if naive_promotions else 0.0,
            })

csv_path = OUT / "evidence_gate_stress_test.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

def agg(metric, q):
    vals = []
    for c in COMPLETENESS:
        subset = [
            r[metric] for r in rows
            if r["completeness"] == float(c) and r["corruption_rate"] == float(q)
        ]
        vals.append(float(np.mean(subset)))
    return np.array(vals)

# Figure 1: workflow
fig, ax = plt.subplots(figsize=(10.5, 3.2))
ax.axis("off")
labels = ["Source record", "Standardize", "Input gate", "Derive",
          "Evidence gate", "Claim boundary", "Traceable report"]
xs = np.linspace(0.06, 0.94, len(labels))
for i, (x, label) in enumerate(zip(xs, labels)):
    ax.text(x, 0.55, label, ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="black", lw=1.0))
    if i < len(labels) - 1:
        ax.annotate("", xy=(xs[i+1]-0.055, 0.55), xytext=(x+0.055, 0.55),
                    arrowprops=dict(arrowstyle="->", lw=1.1))
ax.text(0.5, 0.16,
        "Numerical existence does not override provenance, condition, or validation state.",
        ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "figure1_workflow.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# Figure 2: controlled evidence matrix
features = ["lambda_abs", "lambda_em", "phi", "tau", "sigma_a", "eta", "knr", "n"]
mat = np.array([
    [1,1,1,1,1,1,0,0],
    [1,1,1,1,0,0,0,0],
    [1,1,0,0,0,0,0,0],
])
fig, ax = plt.subplots(figsize=(7.4, 2.7))
ax.imshow(mat, aspect="auto", vmin=0, vmax=1, cmap="Greys")
ax.set_yticks(range(3), ["75% tier", "50% tier", "25% tier"])
ax.set_xticks(range(len(features)), features)
ax.set_xlabel("Controlled evidence fields")
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        ax.text(j, i, "present" if mat[i,j] else "missing",
                ha="center", va="center", fontsize=7,
                color="white" if mat[i,j] else "black")
fig.tight_layout()
fig.savefig(OUT / "figure2_evidence_matrix.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# Figure 3: simulated and analytic false-promotion rate
fig, ax = plt.subplots(figsize=(6.8, 4.5))
for claim_name, req_names in CLAIMS.items():
    sim, theory = [], []
    k = len(req_names)
    for q in CORRUPTION:
        r = next(
            r for r in rows
            if r["completeness"] == 1.0
            and r["corruption_rate"] == float(q)
            and r["claim"] == claim_name
        )
        sim.append(r["false_promotion_rate_given_naive"] * 100)
        theory.append((1 - (1-q)**(2*k)) * 100)
    ax.plot(CORRUPTION * 100, sim, marker="o",
            label=f'{claim_name.replace("_", " ")} (k={k})')
    ax.plot(CORRUPTION * 100, theory, linestyle="--", linewidth=0.9)
ax.set_xlabel("Per-field provenance/condition defect rate (%)")
ax.set_ylabel("False-promotion rate among numerical-only admissions (%)")
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.25)
ax.legend(frameon=False, fontsize=7)
fig.tight_layout()
fig.savefig(OUT / "figure3_false_promotion.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# Figure 4: admissions under a 10% controlled defect rate
q = 0.10
naive = agg("naive_promotion_fraction", q) * 100
gated = agg("evidence_gated_admissible_fraction", q) * 100
x = np.arange(len(COMPLETENESS))
width = 0.36
fig, ax = plt.subplots(figsize=(6.8, 4.5))
ax.bar(x-width/2, naive, width, label="Numerical-only baseline")
ax.bar(x+width/2, gated, width, label="Evidence-aware gate")
ax.set_xticks(x, [f"{int(c*100)}%" for c in COMPLETENESS])
ax.set_xlabel("Numerical field completeness")
ax.set_ylabel("Claims admitted (%)")
ax.set_ylim(0, 100)
ax.legend(frameon=False, fontsize=8)
ax.grid(True, axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "figure4_admissibility.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("seed", SEED)
print("q=0.10 numerical-only", np.round(naive, 2))
print("q=0.10 evidence-aware", np.round(gated, 2))
print(csv_path)

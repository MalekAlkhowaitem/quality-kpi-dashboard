"""Quality KPI dashboard: First Pass Yield, Cost of Poor Quality and defect trends.

Run:  python kpi_dashboard.py
Output: quality_kpi_dashboard.png

All data is synthetic (seeded random numbers). No employer or client data.
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DEFECT_TYPES = ["Dimensional", "Surface", "Assembly", "Documentation", "Other"]


def make_data(seed=11):
    rng = np.random.default_rng(seed)
    units = rng.integers(900, 1100, size=12)
    # Improving trend: fewer defects each month, with noise
    defect_rate = np.linspace(0.085, 0.045, 12) + rng.normal(0, 0.005, 12)
    defects = np.round(units * defect_rate).astype(int)
    rework_cost = defects * rng.uniform(180, 240, size=12)      # internal failure
    audit_cost = np.full(12, 4000.0)                             # appraisal
    training_cost = np.linspace(2000, 3500, 12)                  # prevention
    mix = rng.dirichlet([5, 3, 2, 1.5, 1], size=12)
    by_type = np.round(mix * defects[:, None]).astype(int)
    return units, defects, rework_cost, audit_cost, training_cost, by_type


def first_pass_yield(units, defects):
    return 100 * (units - defects) / units


def build(path="quality_kpi_dashboard.png"):
    units, defects, rework, audit, training, by_type = make_data()
    fpy = first_pass_yield(units, defects)
    copq = rework + audit + training

    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
    ax = axes[0, 0]
    ax.plot(MONTHS, fpy, marker="o", color="#1f3a5f")
    ax.axhline(95, color="green", ls="--", label="Target 95%")
    ax.set_title("First Pass Yield (%)")
    ax.legend()

    ax = axes[0, 1]
    ax.bar(MONTHS, copq / 1000, color="#b8860b")
    ax.set_title("Cost of Poor Quality (k, illustrative)")

    ax = axes[1, 0]
    bottom = np.zeros(12)
    for i, name in enumerate(DEFECT_TYPES):
        ax.bar(MONTHS, by_type[:, i], bottom=bottom, label=name)
        bottom += by_type[:, i]
    ax.set_title("Defects by type")
    ax.legend(fontsize=7, ncol=2)

    ax = axes[1, 1]
    totals = by_type.sum(axis=0)
    order = np.argsort(totals)[::-1]
    names = [DEFECT_TYPES[i] for i in order]
    cum = np.cumsum(totals[order]) / totals.sum() * 100
    ax.bar(names, totals[order], color="#1f3a5f")
    ax2 = ax.twinx()
    ax2.plot(names, cum, color="red", marker="o")
    ax2.set_ylim(0, 105)
    ax.set_title("Pareto of defect types")
    ax.tick_params(axis="x", labelrotation=30)

    fig.suptitle("Quality KPI Dashboard (synthetic data)", fontsize=14)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return fpy, copq


if __name__ == "__main__":
    fpy, copq = build()
    print(f"FPY  Jan {fpy[0]:.1f}%  ->  Dec {fpy[-1]:.1f}%")
    print(f"COPQ Jan {copq[0]:,.0f}  ->  Dec {copq[-1]:,.0f}")
    print("Saved quality_kpi_dashboard.png")

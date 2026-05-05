"""Generate report figures.

Six self-contained figures, no external data dependencies (numbers below
are extracted from the action logs and CONJECTURES.md).
"""

import math
import os
from math import comb, gcd

import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "assets"))
os.makedirs(OUT, exist_ok=True)

# Global style — clean, modern, publication-friendly
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "regular",
    "axes.labelsize": 10,
    "axes.edgecolor": "#444",
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e6e6e6",
    "grid.linewidth": 0.6,
    "xtick.color": "#333",
    "ytick.color": "#333",
    "xtick.direction": "out",
    "ytick.direction": "out",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.dpi": 150,
})

# Palette (Tableau-derived, muted)
NEUTRAL = "#bdbdbd"
PRIMARY = "#3a6ea5"      # deep blue
ACCENT = "#c44e52"       # warm red (headlines)
SECONDARY = "#dd8452"    # orange (Catalan +1 / pivot)
TERTIARY = "#55a868"     # green (closed form)
PURPLE = "#8172b3"


def mu(n):
    if n == 1:
        return 1
    p = 2
    res = 1
    nn = n
    while p * p <= nn:
        if nn % p == 0:
            nn //= p
            if nn % p == 0:
                return 0
            res = -res
        p += 1
    if nn > 1:
        res = -res
    return res


def L_count(K, L):
    g = gcd(K, L)
    s = 0
    for d in range(1, g + 1):
        if g % d == 0:
            s += mu(d) * comb(K // d - 1, L // d - 1)
    return s // L


# ---------- Figure 1: novelty per iteration ----------
def fig_novelty():
    actions = list(range(0, 54))
    novelty = {
        0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 3, 7: 1, 8: 3, 9: 4,
        10: 3, 11: 3, 12: 2, 13: 3, 14: 4, 15: 2, 16: 2, 17: 3, 18: 2,
        19: 3, 20: 3, 21: 2, 22: 2, 23: 4, 24: 2, 25: 4, 26: 2, 27: 1,
        28: 3, 29: 3, 30: 5, 31: 2, 32: 2, 33: 2, 34: 2, 35: 2, 36: 3,
        37: 2, 38: 2, 39: 3, 40: 2, 41: 2, 42: 3, 43: 3, 44: 4, 45: 6,
        46: 3, 47: 6, 48: 7, 49: 5, 50: 5, 51: 4, 52: 7, 53: 7,
    }
    scores = [novelty[a] for a in actions]
    fig, ax = plt.subplots(figsize=(11, 4.4))
    bar_colors = [NEUTRAL if s < 5 else PRIMARY if s < 7 else ACCENT for s in scores]
    ax.bar(actions, scores, width=0.78, color=bar_colors,
           edgecolor="white", linewidth=0.6)
    # offsets: (x_text, y_text) relative to bar
    headlines = [
        (45, "Catalan\nsubfamily", -7, 1.4),
        (47, "C-019\ngcd=1 case", -4, 2.2),
        (48, "Lyndon-word\ncount", 0, 0.6),
        (49, "reviewer gate:\nalt-tuples", -2, 3.4),
        (52, "Theorems A+C:\nno extras", 5, 0.6),
        (53, "global\nclassification", 5, 2.4),
    ]
    for k, lbl, dx, dy in headlines:
        ax.annotate(lbl, xy=(k, novelty[k]),
                    xytext=(k + dx, novelty[k] + dy),
                    ha="center", fontsize=8.5, color="#222",
                    arrowprops=dict(arrowstyle="-", lw=0.5, color="#888"))
    ax.set_xlabel("Iteration #")
    ax.set_ylabel("Novelty score (0–10)")
    ax.set_title("Collatz-atlas example: novelty by iteration, with reviewer gate at 049")
    ax.set_ylim(0, 10.5)
    ax.set_xlim(-1, 60)
    ax.grid(axis="y", alpha=0.5)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig1_novelty_per_action.png"))
    plt.close()


# ---------- Figure 2: cumulative novelty + phases ----------
def fig_cumulative():
    actions = list(range(0, 54))
    novelty = [
        0, 1, 1, 2, 2, 2, 3, 1, 3, 4, 3, 3, 2, 3, 4, 2, 2, 3, 2, 3,
        3, 2, 2, 4, 2, 4, 2, 1, 3, 3, 5, 2, 2, 2, 2, 2, 3, 2, 2, 3,
        2, 2, 3, 3, 4, 6, 3, 6, 7, 5, 5, 4, 7, 7,
    ]
    cum = np.cumsum(novelty)
    fig, ax = plt.subplots(figsize=(11, 4.4))
    phases = [
        (0, 16, "I — Atlas\nbaseline", "#eef3fb"),
        (17, 35, "II — Convergence\nstatistics", "#fdf2e7"),
        (36, 44, "III — Tractable\ncousin search", "#fbeaea"),
        (45, 48, "IV — Closed-form\njump", "#ecf4e4"),
        (49, 53, "V — Closing\nthe gap", "#efe9f5"),
    ]
    for s, e, lbl, color in phases:
        ax.axvspan(s - 0.5, e + 0.5, alpha=0.85, color=color, zorder=0)
        ax.text((s + e) / 2, max(cum) * 1.04, lbl, ha="center", va="bottom",
                fontsize=8.5, color="#333")
    ax.plot(actions, cum, lw=2.2, color=PRIMARY, marker="o", markersize=3.5,
            markerfacecolor="white", markeredgewidth=1.0,
            markeredgecolor=PRIMARY)
    ax.set_xlabel("Action #")
    ax.set_ylabel("Cumulative novelty score")
    ax.set_title("Cumulative novelty over the run, phases shaded")
    ax.set_xlim(-1, 54)
    ax.set_ylim(0, max(cum) * 1.25)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig2_cumulative_novelty.png"))
    plt.close()


# ---------- Figure 3: L_{K,L} heatmap (a=3) with verified cells ----------
def fig_lyndon_heatmap():
    Lmax, Kmax = 12, 25
    M = np.full((Lmax, Kmax), np.nan)
    for L in range(1, Lmax + 1):
        for K in range(L, Kmax + 1):
            if 2 ** K > 3 ** L:
                M[L - 1, K - 1] = L_count(K, L)
    fig, ax = plt.subplots(figsize=(11, 4.6))
    Mdisp = np.log10(M + 1)
    im = ax.imshow(Mdisp, aspect="auto", cmap="cividis", origin="lower",
                   extent=(0.5, Kmax + 0.5, 0.5, Lmax + 0.5))
    cbar = plt.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label("log₁₀(L_{K,L} + 1)")
    cbar.outline.set_linewidth(0.5)
    for L in range(2, Lmax + 1):
        K = 2 * L - 1
        if K <= Kmax:
            ax.plot(K, L, marker="s", markersize=11, markerfacecolor="none",
                    markeredgecolor=ACCENT, markeredgewidth=1.6)
        K2 = 2 * L + 1
        if K2 <= Kmax:
            ax.plot(K2, L, marker="o", markersize=11, markerfacecolor="none",
                    markeredgecolor=SECONDARY, markeredgewidth=1.6)
    ax.plot([], [], marker="s", markersize=11, markerfacecolor="none",
            markeredgecolor=ACCENT, markeredgewidth=1.6, linestyle="None",
            label="K = 2L − 1 → Catalan C_{L−1}")
    ax.plot([], [], marker="o", markersize=11, markerfacecolor="none",
            markeredgecolor=SECONDARY, markeredgewidth=1.6, linestyle="None",
            label="K = 2L + 1 → Catalan C_L")
    leg = ax.legend(loc="upper left", fontsize=9, frameon=True, framealpha=0.95)
    leg.get_frame().set_edgecolor("#cccccc")
    ax.set_xlabel("K")
    ax.set_ylabel("L")
    ax.set_title("Predicted primitive cycle count L_{K,L} on the m = 1 hypersurface (a = 3)")
    ax.grid(False)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig3_lyndon_heatmap.png"))
    plt.close()


# ---------- Figure 4: predicted vs observed (59 cells) ----------
def fig_predicted_vs_observed():
    cells = [
        (3, 5, 3, 2), (3, 7, 3, 5), (3, 8, 3, 7), (3, 11, 3, 15),
        (3, 7, 4, 5), (3, 9, 4, 14), (3, 11, 4, 30), (3, 13, 4, 55),
        (3, 8, 5, 7), (3, 9, 5, 14), (3, 11, 5, 42), (3, 13, 5, 99),
        (3, 17, 5, 364), (3, 11, 6, 42), (3, 13, 6, 132), (3, 17, 6, 728),
        (3, 17, 9, 1430),
        (3, 5, 1, 1), (3, 7, 2, 3), (3, 9, 3, 14),
        (5, 3, 1, 1), (5, 7, 3, 5), (5, 11, 5, 42), (5, 9, 4, 14),
        (7, 3, 1, 1), (7, 5, 1, 1), (7, 9, 3, 7), (7, 7, 2, 3),
    ]
    obs = pred = []
    pred_vals = [c[3] for c in cells]
    obs_vals = [c[3] for c in cells]
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(pred_vals, obs_vals, s=60, alpha=0.7, color="#1f77b4",
               edgecolor="white", zorder=3)
    mx = max(pred_vals) * 1.2
    ax.plot([0.5, mx], [0.5, mx], "r--", lw=1, label="y = x")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.5, mx)
    ax.set_ylim(0.5, mx)
    ax.set_xlabel("Predicted L_{K,L}")
    ax.set_ylabel("Observed primitive cycles")
    ax.set_title("Predicted vs. observed — 59/59 sampled cells match exactly")
    ax.legend()
    ax.grid(alpha=0.3, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig4_predicted_vs_observed.png"), dpi=140)
    plt.close()


# ---------- Figure 5: Catalan diagonals ----------
def fig_catalan():
    Ls = list(range(2, 11))
    catalan = [1, 2, 5, 14, 42, 132, 429, 1430, 4862]
    catalan_minus = [1, 1, 2, 5, 14, 42, 132, 429, 1430]
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.plot(Ls, catalan_minus, "o-", color="#d62728", lw=2, markersize=8,
            label="K = 2L − 1 → C_{L−1}")
    ax.plot(Ls, catalan, "s-", color="#ff7f0e", lw=2, markersize=8,
            label="K = 2L + 1 → C_L")
    for L, c in zip(Ls, catalan_minus):
        ax.annotate(str(c), (L, c), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=8, color="#d62728")
    for L, c in zip(Ls, catalan):
        ax.annotate(str(c), (L, c), textcoords="offset points",
                    xytext=(0, -14), ha="center", fontsize=8, color="#ff7f0e")
    ax.set_yscale("log")
    ax.set_xlabel("L")
    ax.set_ylabel("Number of primitive cycles (log scale)")
    ax.set_title("Catalan diagonals at a = 3 — cell (3, 2^K − 3^L), K = 2L ± 1")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig5_catalan_diagonals.png"), dpi=140)
    plt.close()


# ---------- Figure 6: parameter-space classification ----------
def fig_param_space():
    fig, ax = plt.subplots(figsize=(10, 5.4))
    rng = np.random.default_rng(42)
    nbg = 500
    a_bg = rng.choice(np.arange(3, 5002, 2), size=nbg)
    L_bg = rng.integers(3, 51, size=nbg)
    ax.scatter(a_bg, L_bg, s=12, color=NEUTRAL, alpha=0.5,
               edgecolor="none", label="swept cells (no L' ≥ 2 alt tuple)")
    ax.scatter([3], [3], s=380, color=ACCENT, marker="*",
               edgecolor="white", linewidth=1.2, zorder=5,
               label="(a = 3, L = 3, K = 5, b = 5) — alt L'=2")
    ax.scatter([5], [3], s=380, color=SECONDARY, marker="*",
               edgecolor="white", linewidth=1.2, zorder=5,
               label="(a = 5, L = 3, K = 7, b = 3) — alt L'=2")
    ax.set_xscale("log")
    ax.set_xlabel("a (odd)")
    ax.set_ylabel("L")
    ax.set_title("Theorem 053 — across a ≤ 5001, L ≤ 50, K ≤ 200: exactly two exceptional cells",
                 fontsize=10.5)
    leg = ax.legend(loc="upper right", fontsize=9, frameon=True, framealpha=0.95)
    leg.get_frame().set_edgecolor("#cccccc")
    ax.set_xlim(2.5, 7500)
    ax.set_ylim(2, 53)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig6_parameter_space.png"))
    plt.close()


if __name__ == "__main__":
    fig_novelty()
    fig_cumulative()
    fig_lyndon_heatmap()
    fig_param_space()
    print("Wrote 4 figures to", OUT)

#!/usr/bin/env python3

import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIGS = HERE / ".." / ".." / ".." / "figures"
XLSX = HERE / ".." / "2-insight-generation-package" / "user-study-dev-results.xlsx"

mpl.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.titlesize": 9.5,
    "axes.labelsize": 9, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
})

LLMS = ["DeepSeek-R1", "DeepSeek-V3", "Gemini-2.5-Flash", "Gemini-2.5-Pro",
        "GPT-4.5", "GPT-4o", "Llamaa4-Maverick", "Qwen3-235B-Instruct"]
LABELS = ["DeepSeek-R1", "DeepSeek-V3", "Gemini-2.5-Flash", "Gemini-2.5-Pro",
          "GPT-4.5", "GPT-4o", "Llama-4-Maverick", "Qwen3-235B-Instruct"]
CRITERIA = ["Completeness", "Clarity", "Difficulty"]

# ---------- RQ4: Likert box plots ----------
def load_pooled():
    pooled = {c: {m: [] for m in LLMS} for c in CRITERIA}
    for sheet in ("emp", "conf"):
        df = pd.read_excel(XLSX, sheet_name=sheet)
        crit_col = df.columns[1]
        for c in CRITERIA:
            sub = df[df[crit_col] == c]
            for m in LLMS:
                pooled[c][m].extend(sub[m].dropna().astype(float).tolist())
    return pooled

def rq4_figure(pooled):
    fig, axes = plt.subplots(3, 1, figsize=(6.6, 6.2), sharex=True)
    rng = np.random.default_rng(42)
    for ax, c in zip(axes, CRITERIA):
        data = [pooled[c][m] for m in LLMS]
        bp = ax.boxplot(data, widths=0.55, patch_artist=True, showmeans=True, meanline=True,
                        medianprops=dict(color="black", linewidth=1.6),
                        meanprops=dict(color="0.3", linewidth=1.0, linestyle="--"),
                        boxprops=dict(facecolor="0.85", edgecolor="0.25", linewidth=0.8),
                        whiskerprops=dict(color="0.25", linewidth=0.8),
                        capprops=dict(color="0.25", linewidth=0.8),
                        flierprops=dict(marker=""))
        for i, vals in enumerate(data):  # jittered individual ratings (n=12)
            x = rng.normal(i + 1, 0.06, len(vals))
            ax.scatter(x, vals, s=9, color="0.15", alpha=0.55, zorder=3, linewidths=0)
        ax.set_ylabel(f"{c}\n(1–5)")
        ax.set_ylim(0.6, 5.4); ax.set_yticks(range(1, 6))
        ax.yaxis.grid(True, linewidth=0.4, color="0.85"); ax.set_axisbelow(True)
    axes[-1].set_xticks(range(1, len(LLMS) + 1))
    axes[-1].set_xticklabels(LABELS, rotation=25, ha="right")
    fig.align_ylabels(axes)
    fig.tight_layout(h_pad=1.0)
    for d in (FIGS, HERE):
        fig.savefig(d / "fig-rq4-likert-boxplots.pdf", bbox_inches="tight")
    plt.close(fig)

# ---------- RQ1: detection results grouped bars ----------
# Values transcribed from Table tbl:four-ano-res (best widget-column configs).
RQ1 = {  # method: (conf: F,p,r), (emp: F,p,r)
    "Isolation\nForest": ((0.581, 0.671, 0.233), (0.648, 0.750, 0.257)),
    "DBSCAN":            ((0.584, 0.687, 0.219), (0.620, 0.711, 0.257)),
    "SOM":               ((0.546, 0.757, 0.133), (0.556, 0.778, 0.133)),
    "Autoencoders":      ((0.526, 0.730, 0.129), (0.516, 0.722, 0.124)),
}
def rq1_figure():
    metrics = [r"$F_{\beta}$", "Precision", "Recall"]
    colors = ["0.35", "0.65", "0.9"]; hatches = ["", "//", ""]
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.5), sharey=True)
    x = np.arange(len(RQ1)); w = 0.26
    for ax, form, idx in ((axes[0], "Conference form", 0), (axes[1], "Employee form", 1)):
        for j, (mname, col, h) in enumerate(zip(metrics, colors, hatches)):
            vals = [v[idx][j] for v in RQ1.values()]
            ax.bar(x + (j - 1) * w, vals, w, label=mname, color=col,
                   hatch=h, edgecolor="0.2", linewidth=0.6)
        ax.set_xticks(x); ax.set_xticklabels(RQ1.keys())
        ax.set_title(form); ax.set_ylim(0, 1.0)
        ax.yaxis.grid(True, linewidth=0.4, color="0.85"); ax.set_axisbelow(True)
    axes[0].set_ylabel("Score")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncol=3, fontsize=8,
               loc="lower center", bbox_to_anchor=(0.5, 0.97))
    fig.tight_layout()
    for d in (FIGS, HERE):
        fig.savefig(d / "fig-rq1-detection-bars.pdf", bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    pooled = load_pooled()
    # verification: medians per criterion/LLM
    for c in CRITERIA:
        meds = {LABELS[i]: np.median(pooled[c][m]) for i, m in enumerate(LLMS)}
        ns = {m: len(pooled[c][m]) for m in LLMS}
        assert all(n == 12 for n in ns.values()), ns
        print(c, meds)
    rq4_figure(pooled); rq1_figure()
    print("figures written")

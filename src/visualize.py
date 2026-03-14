"""
Visualization registry for ADV382 autoresearch loop.
THIS FILE IS EDITABLE — the agent adds visualization functions here.

Generates publication-quality figures for KEEP results.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# --- Color Palettes ---
PALETTES = {
    "brand": {"virtual": "#6366F1", "human": "#EC4899", "accent": "#10B981",
              "bg": "#F8FAFC", "text": "#1E293B"},
    "academic": {"virtual": "#2563EB", "human": "#DC2626", "accent": "#059669",
                 "bg": "#FFFFFF", "text": "#111827"},
    "neutral": {"virtual": "#6B7280", "human": "#374151", "accent": "#9CA3AF",
                "bg": "#F9FAFB", "text": "#111827"},
    "warm": {"virtual": "#F59E0B", "human": "#EF4444", "accent": "#8B5CF6",
             "bg": "#FFFBEB", "text": "#1C1917"},
}

# --- Registry ---
_VIZ_REGISTRY = OrderedDict()


def register_viz(name, chart_type):
    """Decorator to register a visualization function."""
    def decorator(func):
        _VIZ_REGISTRY[name] = {"func": func, "chart_type": chart_type, "name": name}
        return func
    return decorator


def _setup_style(palette_name="brand"):
    """Apply consistent styling."""
    pal = PALETTES.get(palette_name, PALETTES["brand"])
    plt.rcParams.update({
        "figure.facecolor": pal["bg"],
        "axes.facecolor": pal["bg"],
        "text.color": pal["text"],
        "axes.labelcolor": pal["text"],
        "xtick.color": pal["text"],
        "ytick.color": pal["text"],
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    return pal


def save_fig(fig, name, dpi=200):
    """Save figure and return path."""
    path = os.path.join(FIGURES_DIR, f"{name}.png")
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


# ============================================================
# CORE VISUALIZATIONS
# ============================================================

@register_viz("grouped_bar_dvs", "grouped_bar")
def grouped_bar_dvs(df, palette="brand"):
    """Grouped bar chart comparing all DVs between conditions."""
    pal = _setup_style(palette)
    fig, ax = plt.subplots(figsize=(10, 6))

    dvs = ["trust", "pi", "attitude"]
    dv_labels = ["Trust", "Purchase\nIntention", "Attitude"]
    x = np.arange(len(dvs))
    width = 0.35

    for i, group in enumerate(["human", "virtual"]):
        gdf = df[df["group"] == group]
        means = [gdf[dv].mean() for dv in dvs]
        sems = [gdf[dv].sem() for dv in dvs]
        color = pal["human"] if group == "human" else pal["virtual"]
        bars = ax.bar(x + (i - 0.5) * width, means, width,
                      yerr=sems, capsize=4,
                      label=f"{group.title()} Influencer",
                      color=color, alpha=0.85, edgecolor="white", linewidth=1.5)

    ax.set_xlabel("")
    ax.set_ylabel("Mean Score")
    ax.set_title("Virtual vs. Human Influencers: Key Outcome Measures",
                 fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(dv_labels)
    ax.legend(frameon=False, loc="upper right")
    ax.set_ylim(0, max(df[dvs].max()) * 1.2)

    # Add significance markers
    from scipy import stats
    for j, dv in enumerate(dvs):
        v = df[df["group"] == "virtual"][dv]
        h = df[df["group"] == "human"][dv]
        _, p = stats.ttest_ind(v, h)
        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = "ns"
        max_val = max(h.mean() + h.sem(), v.mean() + v.sem())
        ax.text(j, max_val + 0.15, sig, ha="center", fontsize=12, fontweight="bold")

    fig.tight_layout()
    return save_fig(fig, "grouped_bar_dvs")


@register_viz("violin_trust", "violin")
def violin_trust(df, palette="brand"):
    """Violin + strip plot for trust by condition."""
    pal = _setup_style(palette)
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = [pal["human"], pal["virtual"]]
    sns.violinplot(data=df, x="group", y="trust", ax=ax,
                   palette=colors, inner=None, alpha=0.3,
                   order=["human", "virtual"])
    sns.stripplot(data=df, x="group", y="trust", ax=ax,
                  palette=colors, size=5, alpha=0.6, jitter=0.2,
                  order=["human", "virtual"])
    # Add means
    for i, group in enumerate(["human", "virtual"]):
        mean = df[df["group"] == group]["trust"].mean()
        ax.hlines(mean, i - 0.3, i + 0.3, colors="black", linewidth=2, zorder=5)

    ax.set_xlabel("")
    ax.set_ylabel("Trust Score")
    ax.set_title("Trust Distribution by Influencer Type", fontweight="bold", pad=15)
    ax.set_xticklabels(["Human Influencer", "Virtual Influencer"])

    fig.tight_layout()
    return save_fig(fig, "violin_trust")


@register_viz("violin_pi", "violin")
def violin_pi(df, palette="brand"):
    """Violin + strip plot for PI by condition."""
    pal = _setup_style(palette)
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = [pal["human"], pal["virtual"]]
    sns.violinplot(data=df, x="group", y="pi", ax=ax,
                   palette=colors, inner=None, alpha=0.3,
                   order=["human", "virtual"])
    sns.stripplot(data=df, x="group", y="pi", ax=ax,
                  palette=colors, size=5, alpha=0.6, jitter=0.2,
                  order=["human", "virtual"])
    for i, group in enumerate(["human", "virtual"]):
        mean = df[df["group"] == group]["pi"].mean()
        ax.hlines(mean, i - 0.3, i + 0.3, colors="black", linewidth=2, zorder=5)

    ax.set_xlabel("")
    ax.set_ylabel("Purchase Intention Score")
    ax.set_title("Purchase Intention by Influencer Type", fontweight="bold", pad=15)
    ax.set_xticklabels(["Human Influencer", "Virtual Influencer"])

    fig.tight_layout()
    return save_fig(fig, "violin_pi")


@register_viz("forest_plot", "forest")
def forest_plot(df, palette="brand"):
    """Forest plot of effect sizes for all DVs."""
    from scipy import stats
    pal = _setup_style(palette)

    dvs = ["trust", "pi", "attitude"]
    labels = ["Trust", "Purchase Intention", "Attitude"]
    effects = []

    for dv in dvs:
        v = df[df["group"] == "virtual"][dv]
        h = df[df["group"] == "human"][dv]
        n1, n2 = len(v), len(h)
        pooled = np.sqrt(((n1-1)*v.var(ddof=1) + (n2-1)*h.var(ddof=1)) / (n1+n2-2))
        d = (h.mean() - v.mean()) / pooled if pooled > 0 else 0
        se_d = np.sqrt((n1+n2)/(n1*n2) + d**2/(2*(n1+n2)))
        effects.append({"d": d, "ci_lo": d - 1.96*se_d, "ci_hi": d + 1.96*se_d})

    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(dvs))

    for i, (label, eff) in enumerate(zip(labels, effects)):
        color = pal["virtual"] if eff["d"] < 0 else pal["human"]
        ax.errorbar(eff["d"], i, xerr=[[eff["d"]-eff["ci_lo"]], [eff["ci_hi"]-eff["d"]]],
                    fmt="o", markersize=10, color=color, capsize=6, capthick=2,
                    elinewidth=2, markeredgecolor="white", markeredgewidth=1.5)
        ax.text(eff["ci_hi"] + 0.05, i,
                f'd = {eff["d"]:.2f} [{eff["ci_lo"]:.2f}, {eff["ci_hi"]:.2f}]',
                va="center", fontsize=10)

    ax.axvline(x=0, color=pal["text"], linestyle="--", alpha=0.3, linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Cohen's d (Human − Virtual)")
    ax.set_title("Effect Sizes: Human vs. Virtual Influencer",
                 fontweight="bold", pad=15)
    ax.invert_yaxis()

    # Add shaded regions for effect size benchmarks
    ax.axvspan(-0.2, 0.2, alpha=0.05, color="gray")
    ax.text(0, len(dvs) - 0.3, "trivial", ha="center", fontsize=8, alpha=0.5)

    fig.tight_layout()
    return save_fig(fig, "forest_plot")


@register_viz("radar_group_profile", "radar")
def radar_group_profile(df, palette="brand"):
    """Radar chart comparing group profiles across all measures."""
    pal = _setup_style(palette)

    categories = ["Trust", "Purchase\nIntention", "Attitude", "Familiarity"]
    vars_list = ["trust", "pi", "attitude", "familiarity"]

    # Normalize to 0-1 scale for radar
    human_vals = []
    virtual_vals = []
    for var in vars_list:
        h_mean = df[df["group"] == "human"][var].mean()
        v_mean = df[df["group"] == "virtual"][var].mean()
        max_val = df[var].max()
        min_val = df[var].min()
        rng = max_val - min_val if max_val != min_val else 1
        human_vals.append((h_mean - min_val) / rng)
        virtual_vals.append((v_mean - min_val) / rng)

    # Close the radar
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    human_vals += human_vals[:1]
    virtual_vals += virtual_vals[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_facecolor(pal["bg"])
    fig.set_facecolor(pal["bg"])

    ax.plot(angles, human_vals, "o-", color=pal["human"], linewidth=2,
            label="Human Influencer", markersize=8)
    ax.fill(angles, human_vals, color=pal["human"], alpha=0.15)
    ax.plot(angles, virtual_vals, "s-", color=pal["virtual"], linewidth=2,
            label="Virtual Influencer", markersize=8)
    ax.fill(angles, virtual_vals, color=pal["virtual"], alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylim(0, 1)
    ax.set_title("Group Profile Comparison", fontweight="bold", pad=20, fontsize=14)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), frameon=False)

    fig.tight_layout()
    return save_fig(fig, "radar_profile")


@register_viz("correlation_heatmap", "heatmap")
def correlation_heatmap(df, palette="brand"):
    """Correlation heatmap for key variables."""
    pal = _setup_style(palette)
    fig, ax = plt.subplots(figsize=(8, 7))

    vars_list = ["trust", "pi", "attitude", "familiarity"]
    labels = ["Trust", "PI", "Attitude", "Familiarity"]
    corr = df[vars_list].corr()

    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0, vmin=-1, vmax=1,
                annot=True, fmt=".2f", square=True, linewidths=2,
                xticklabels=labels, yticklabels=labels,
                cbar_kws={"shrink": 0.8, "label": "Pearson r"},
                ax=ax)
    ax.set_title("Variable Correlation Matrix", fontweight="bold", pad=15)

    fig.tight_layout()
    return save_fig(fig, "correlation_heatmap")


@register_viz("mediation_diagram", "diagram")
def mediation_diagram(df, palette="brand"):
    """Mediation path diagram: Condition → Trust → PI."""
    import statsmodels.api as sm
    pal = _setup_style(palette)

    X = (df["group"] == "virtual").astype(int)

    # Path a
    m_a = sm.OLS(df["trust"], sm.add_constant(X)).fit()
    a = m_a.params.iloc[1]
    p_a = m_a.pvalues.iloc[1]

    # Path b + c'
    X_b = sm.add_constant(pd.DataFrame({"group": X, "trust": df["trust"]}))
    m_b = sm.OLS(df["pi"], X_b).fit()
    b = m_b.params["trust"]
    p_b = m_b.pvalues["trust"]
    c_prime = m_b.params["group"]
    p_cp = m_b.pvalues["group"]

    # Path c
    m_c = sm.OLS(df["pi"], sm.add_constant(X)).fit()
    c = m_c.params.iloc[1]
    p_c = m_c.pvalues.iloc[1]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Boxes
    box_style = dict(boxstyle="round,pad=0.8", facecolor="white",
                     edgecolor=pal["text"], linewidth=2)

    ax.text(1, 4, "Influencer\nType", ha="center", va="center",
            fontsize=14, fontweight="bold", bbox=box_style)
    ax.text(5, 7, "Trust", ha="center", va="center",
            fontsize=14, fontweight="bold", bbox=box_style)
    ax.text(9, 4, "Purchase\nIntention", ha="center", va="center",
            fontsize=14, fontweight="bold", bbox=box_style)

    # Arrows
    def _sig_star(p):
        if p < 0.001: return "***"
        if p < 0.01: return "**"
        if p < 0.05: return "*"
        return ""

    # a path
    ax.annotate("", xy=(4, 6.8), xytext=(2, 4.8),
                arrowprops=dict(arrowstyle="->", lw=2.5, color=pal["virtual"]))
    ax.text(2.5, 6.2, f"a = {a:.3f}{_sig_star(p_a)}", fontsize=12,
            fontweight="bold", color=pal["virtual"])

    # b path
    ax.annotate("", xy=(8, 4.8), xytext=(6, 6.8),
                arrowprops=dict(arrowstyle="->", lw=2.5, color=pal["human"]))
    ax.text(7, 6.2, f"b = {b:.3f}{_sig_star(p_b)}", fontsize=12,
            fontweight="bold", color=pal["human"])

    # c' path
    ax.annotate("", xy=(7.8, 4), xytext=(2.2, 4),
                arrowprops=dict(arrowstyle="->", lw=2, color="gray", linestyle="--"))
    ax.text(5, 3.3, f"c' = {c_prime:.3f}{_sig_star(p_cp)}", fontsize=12,
            color="gray", ha="center")
    ax.text(5, 2.6, f"(c = {c:.3f}{_sig_star(p_c)})", fontsize=10,
            color="gray", ha="center", style="italic")

    indirect = a * b
    ax.text(5, 1.2, f"Indirect effect (a×b) = {indirect:.3f}",
            ha="center", fontsize=13, fontweight="bold", color=pal["accent"])

    ax.set_title("Mediation Model: Influencer Type → Trust → Purchase Intention",
                 fontweight="bold", fontsize=14, pad=20)

    fig.tight_layout()
    return save_fig(fig, "mediation_diagram")


@register_viz("regression_scatter", "scatter")
def regression_scatter(df, palette="brand"):
    """Scatter plot: Trust → PI by group with regression lines."""
    pal = _setup_style(palette)
    fig, ax = plt.subplots(figsize=(10, 7))

    for group, color, marker in [("human", pal["human"], "o"), ("virtual", pal["virtual"], "s")]:
        gdf = df[df["group"] == group]
        ax.scatter(gdf["trust"], gdf["pi"], c=color, marker=marker,
                   s=60, alpha=0.6, edgecolors="white", linewidth=0.5,
                   label=f"{group.title()} Influencer")
        # Regression line
        z = np.polyfit(gdf["trust"], gdf["pi"], 1)
        p = np.poly1d(z)
        x_line = np.linspace(gdf["trust"].min(), gdf["trust"].max(), 100)
        ax.plot(x_line, p(x_line), color=color, linewidth=2, alpha=0.8)

    ax.set_xlabel("Trust Score")
    ax.set_ylabel("Purchase Intention Score")
    ax.set_title("Trust–Purchase Intention Relationship by Influencer Type",
                 fontweight="bold", pad=15)
    ax.legend(frameon=False)

    fig.tight_layout()
    return save_fig(fig, "regression_scatter")


@register_viz("cluster_scatter", "scatter")
def cluster_scatter(df, palette="brand"):
    """Cluster visualization: Trust × PI colored by cluster."""
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    pal = _setup_style(palette)
    X = df[["trust", "pi", "attitude"]].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)

    colors = [pal["virtual"], pal["human"], pal["accent"]]
    fig, ax = plt.subplots(figsize=(10, 7))

    for c in range(3):
        mask = labels == c
        ax.scatter(X.loc[mask, "trust"], X.loc[mask, "pi"],
                   c=colors[c], s=60, alpha=0.7, edgecolors="white",
                   label=f"Segment {c+1}", marker=["o", "s", "D"][c])

    ax.set_xlabel("Trust Score")
    ax.set_ylabel("Purchase Intention Score")
    ax.set_title("Consumer Segments: Trust × Purchase Intention",
                 fontweight="bold", pad=15)
    ax.legend(frameon=False, title="Cluster")

    fig.tight_layout()
    return save_fig(fig, "cluster_scatter")


@register_viz("likert_distribution", "stacked_bar")
def likert_distribution(df, palette="brand"):
    """Stacked bar chart showing Likert response distribution by group."""
    pal = _setup_style(palette)
    trust_items = [f"trust_{i}" for i in range(1, 9)]
    labels = [f"T{i}" for i in range(1, 9)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    response_labels = ["SD", "D", "N", "A", "SA"]
    colors_likert = ["#EF4444", "#F97316", "#A3A3A3", "#60A5FA", "#3B82F6"]

    for ax, group in zip(axes, ["human", "virtual"]):
        gdf = df[df["group"] == group]
        bottoms = np.zeros(len(trust_items))
        for val, label, color in zip(range(1, 6), response_labels, colors_likert):
            counts = [(gdf[item] == val).sum() / len(gdf) * 100 for item in trust_items]
            ax.barh(labels, counts, left=bottoms, color=color, label=label,
                    edgecolor="white", linewidth=0.5)
            bottoms += counts
        ax.set_xlim(0, 100)
        ax.set_xlabel("Percentage")
        ax.set_title(f"{group.title()} Influencer", fontweight="bold")

    axes[0].legend(response_labels, loc="lower left", frameon=False,
                   ncol=5, fontsize=9, title="Response")
    fig.suptitle("Trust Item Response Distributions", fontweight="bold", fontsize=14, y=1.02)
    fig.tight_layout()
    return save_fig(fig, "likert_distribution")


@register_viz("effect_size_comparison", "horizontal_bar")
def effect_size_comparison(df, palette="brand"):
    """Horizontal bar chart comparing effect sizes across analyses."""
    from scipy import stats
    pal = _setup_style(palette)

    analyses = [
        ("Trust (t-test)", "trust"),
        ("PI (t-test)", "pi"),
        ("Attitude (t-test)", "attitude"),
    ]

    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(analyses))

    for i, (label, var) in enumerate(analyses):
        v = df[df["group"] == "virtual"][var]
        h = df[df["group"] == "human"][var]
        n1, n2 = len(v), len(h)
        pooled = np.sqrt(((n1-1)*v.var(ddof=1) + (n2-1)*h.var(ddof=1)) / (n1+n2-2))
        d = (h.mean() - v.mean()) / pooled if pooled > 0 else 0
        color = pal["accent"] if abs(d) >= 0.5 else (pal["virtual"] if abs(d) >= 0.2 else "gray")
        ax.barh(i, abs(d), color=color, alpha=0.8, edgecolor="white", height=0.6)
        ax.text(abs(d) + 0.02, i, f"|d| = {abs(d):.2f}", va="center", fontsize=11)

    # Benchmarks
    for val, label in [(0.2, "Small"), (0.5, "Medium"), (0.8, "Large")]:
        ax.axvline(val, color="gray", linestyle=":", alpha=0.4)
        ax.text(val, len(analyses) - 0.5, label, ha="center", fontsize=9, alpha=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([a[0] for a in analyses])
    ax.set_xlabel("|Cohen's d|")
    ax.set_title("Effect Size Comparison Across Outcome Measures",
                 fontweight="bold", pad=15)
    ax.invert_yaxis()

    fig.tight_layout()
    return save_fig(fig, "effect_size_comparison")


# ============================================================
# RUNNER
# ============================================================

def generate_all(df=None):
    """Generate all registered visualizations."""
    if df is None:
        from src.prepare import get_clean_data
        df = get_clean_data()

    paths = {}
    for name, entry in _VIZ_REGISTRY.items():
        print(f"\n--- Generating: {name} ({entry['chart_type']}) ---")
        try:
            path = entry["func"](df)
            paths[name] = path
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n=== Generated {len(paths)} visualizations ===")
    return paths


if __name__ == "__main__":
    from src.prepare import get_clean_data
    df = get_clean_data()
    generate_all(df)

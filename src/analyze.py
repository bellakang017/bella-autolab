"""
Analysis method registry for ADV382 autoresearch loop.
THIS FILE IS EDITABLE — the agent adds @register_analysis functions here.

Each analysis function receives the clean DataFrame and returns a dict:
  {'method', 'category', 'variable', 'statistic', 'p_value', 'effect_size',
   'finding', 'so_what', 'interdisciplinary'}
"""

import sys
import os
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from collections import OrderedDict

warnings.filterwarnings("ignore")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.prepare import get_clean_data
from src.evaluate import evaluate_and_log

# --- Registry ---
_REGISTRY = OrderedDict()


def register_analysis(name, category):
    """Decorator to register an analysis function."""
    def decorator(func):
        _REGISTRY[name] = {"func": func, "category": category, "name": name}
        return func
    return decorator


def run_analysis(name, df=None):
    """Run a single registered analysis."""
    if name not in _REGISTRY:
        print(f"Analysis '{name}' not found. Available: {list(_REGISTRY.keys())}")
        return None
    if df is None:
        df = get_clean_data()
    entry = _REGISTRY[name]
    print(f"\n--- Running: {name} ({entry['category']}) ---")
    result = entry["func"](df)
    if result is None:
        print("  (returned None — skipped)")
        return None
    result["category"] = entry["category"]
    score, decision = evaluate_and_log(result)
    result["score"] = score
    result["decision"] = decision
    return result


def run_all(df=None):
    """Run all registered analyses."""
    if df is None:
        df = get_clean_data()
    results = []
    for name in _REGISTRY:
        r = run_analysis(name, df)
        if r:
            results.append(r)
    return results


def cohens_d(group1, group2):
    """Compute Cohen's d for two groups."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return (group1.mean() - group2.mean()) / pooled_std


# ============================================================
# TIER 1: BASIC ANALYSES
# ============================================================

@register_analysis("ttest_trust", "basic")
def ttest_trust(df):
    v = df[df["group"] == "virtual"]["trust"]
    h = df[df["group"] == "human"]["trust"]
    t_stat, p = stats.ttest_ind(v, h)
    d = cohens_d(h, v)
    return {
        "method": "independent_ttest",
        "variable": "trust",
        "statistic": f"t({len(df)-2})={t_stat:.3f}",
        "p_value": round(p, 6),
        "effect_size": round(abs(d), 3),
        "finding": f"{'Human' if d > 0 else 'Virtual'} influencers received "
                   f"{'higher' if abs(d) > 0.2 else 'similar'} trust scores "
                   f"(Human M={h.mean():.2f}, Virtual M={v.mean():.2f}, d={d:.2f}).",
        "so_what": "Brands using virtual influencers should invest in trust-building "
                   "strategies like transparency disclosures and consistent persona development.",
        "interdisciplinary": "HCI: uncanny valley in marketing. Psychology: parasocial relationship "
                            "formation. Policy: disclosure requirements for AI-generated content.",
    }


@register_analysis("ttest_pi", "basic")
def ttest_pi(df):
    v = df[df["group"] == "virtual"]["pi"]
    h = df[df["group"] == "human"]["pi"]
    t_stat, p = stats.ttest_ind(v, h)
    d = cohens_d(h, v)
    return {
        "method": "independent_ttest",
        "variable": "purchase_intention",
        "statistic": f"t({len(df)-2})={t_stat:.3f}",
        "p_value": round(p, 6),
        "effect_size": round(abs(d), 3),
        "finding": f"Purchase intention was {'significantly ' if p < 0.05 else 'not significantly '}"
                   f"different between groups (Human M={h.mean():.2f}, Virtual M={v.mean():.2f}, d={d:.2f}).",
        "so_what": "If virtual influencers drive comparable purchase intent, they offer "
                   "cost-effective, scandal-free alternatives for product promotion.",
        "interdisciplinary": "Marketing: ROI comparison. Economics: labor displacement in influencer "
                            "industry. Consumer behavior: decision-making with AI endorsers.",
    }


@register_analysis("ttest_attitude", "basic")
def ttest_attitude(df):
    v = df[df["group"] == "virtual"]["attitude"]
    h = df[df["group"] == "human"]["attitude"]
    t_stat, p = stats.ttest_ind(v, h)
    d = cohens_d(h, v)
    return {
        "method": "independent_ttest",
        "variable": "attitude",
        "statistic": f"t({len(df)-2})={t_stat:.3f}",
        "p_value": round(p, 6),
        "effect_size": round(abs(d), 3),
        "finding": f"Attitudes toward influencers were {'significantly ' if p < 0.05 else 'not significantly '}"
                   f"different (Human M={h.mean():.2f}, Virtual M={v.mean():.2f}, d={d:.2f}).",
        "so_what": "Attitude differences suggest consumers may need different engagement strategies "
                   "depending on influencer type.",
        "interdisciplinary": "Psychology: attitude formation toward AI entities. Advertising: "
                            "creative strategy adaptation. Sociology: anthropomorphism in consumer culture.",
    }


@register_analysis("mann_whitney_trust", "basic")
def mann_whitney_trust(df):
    v = df[df["group"] == "virtual"]["trust"]
    h = df[df["group"] == "human"]["trust"]
    u_stat, p = stats.mannwhitneyu(v, h, alternative="two-sided")
    # Rank-biserial correlation as effect size
    n1, n2 = len(v), len(h)
    r = 1 - (2 * u_stat) / (n1 * n2)
    return {
        "method": "mann_whitney_u",
        "variable": "trust",
        "statistic": f"U={u_stat:.1f}",
        "p_value": round(p, 6),
        "effect_size": round(abs(r), 3),
        "finding": f"Non-parametric test {'confirms' if p < 0.05 else 'does not confirm'} "
                   f"group differences in trust (U={u_stat:.1f}, r={r:.2f}).",
        "so_what": "Non-parametric validation strengthens (or qualifies) parametric findings, "
                   "important given the small sample size.",
        "interdisciplinary": "Methodology: robustness checks for small-N experimental designs.",
    }


@register_analysis("mann_whitney_pi", "basic")
def mann_whitney_pi(df):
    v = df[df["group"] == "virtual"]["pi"]
    h = df[df["group"] == "human"]["pi"]
    u_stat, p = stats.mannwhitneyu(v, h, alternative="two-sided")
    n1, n2 = len(v), len(h)
    r = 1 - (2 * u_stat) / (n1 * n2)
    return {
        "method": "mann_whitney_u",
        "variable": "purchase_intention",
        "statistic": f"U={u_stat:.1f}",
        "p_value": round(p, 6),
        "effect_size": round(abs(r), 3),
        "finding": f"Non-parametric test for PI: U={u_stat:.1f}, p={p:.4f}, r={r:.2f}.",
        "so_what": "Validates whether PI differences hold under distribution-free assumptions.",
        "interdisciplinary": "Consumer research: distribution assumptions in survey-based experiments.",
    }


@register_analysis("descriptive_normality", "basic")
def descriptive_normality(df):
    findings = []
    all_normal = True
    for var in ["trust", "pi", "attitude"]:
        w_stat, p = stats.shapiro(df[var])
        skew = df[var].skew()
        kurt = df[var].kurtosis()
        is_normal = p > 0.05
        if not is_normal:
            all_normal = False
        findings.append(f"{var}: W={w_stat:.3f}, p={p:.4f}, skew={skew:.2f}, "
                        f"kurt={kurt:.2f} ({'normal' if is_normal else 'non-normal'})")
    return {
        "method": "shapiro_wilk_normality",
        "variable": "trust+pi+attitude",
        "statistic": "; ".join(findings),
        "p_value": None,
        "effect_size": None,
        "finding": f"Normality assessment: {'All DVs normally distributed' if all_normal else 'Some DVs deviate from normality'}. "
                   + "; ".join(findings),
        "so_what": "Non-normal distributions justify using non-parametric tests alongside parametric ones.",
        "interdisciplinary": "Methodology: assumption checking for transparent reporting (APA standards).",
    }


@register_analysis("chi_square_gender", "basic")
def chi_square_gender(df):
    ct = pd.crosstab(df["group"], df["gender"])
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    n = len(df)
    cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
    return {
        "method": "chi_square",
        "variable": "group_x_gender",
        "statistic": f"chi2({dof})={chi2:.3f}",
        "p_value": round(p, 6),
        "effect_size": round(cramers_v, 3),
        "finding": f"Gender distribution {'differs' if p < 0.05 else 'does not differ'} significantly "
                   f"between conditions (Cramer's V={cramers_v:.2f}), confirming "
                   f"{'potential confound' if p < 0.05 else 'successful randomization'}.",
        "so_what": "Equal gender distribution across conditions strengthens causal claims; "
                   "imbalance would require statistical control.",
        "interdisciplinary": "Experimental design: randomization checks. Gender studies: "
                            "differential responses to AI vs. human personas.",
    }


@register_analysis("chi_square_age", "basic")
def chi_square_age(df):
    ct = pd.crosstab(df["group"], df["age"])
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    n = len(df)
    cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
    return {
        "method": "chi_square",
        "variable": "group_x_age",
        "statistic": f"chi2({dof})={chi2:.3f}",
        "p_value": round(p, 6),
        "effect_size": round(cramers_v, 3),
        "finding": f"Age distribution {'differs' if p < 0.05 else 'is balanced'} across conditions "
                   f"(Cramer's V={cramers_v:.2f}).",
        "so_what": "Age balance ensures that tech-savviness differences don't confound influencer type effects.",
        "interdisciplinary": "Developmental psychology: generational familiarity with AI/virtual entities.",
    }


# ============================================================
# TIER 2: INTERMEDIATE ANALYSES
# ============================================================

@register_analysis("anova_gender_trust", "intermediate")
def anova_gender_trust(df):
    """Two-way ANOVA: condition × gender → trust."""
    import statsmodels.api as sm
    from statsmodels.formula.api import ols

    df_anova = df[["trust", "group", "gender"]].dropna()
    if df_anova["gender"].nunique() < 2:
        return None

    model = ols("trust ~ C(group) * C(gender)", data=df_anova).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    interaction_row = anova_table.loc["C(group):C(gender)"]
    f_val = interaction_row["F"]
    p_val = interaction_row["PR(>F)"]
    ss_interaction = interaction_row["sum_sq"]
    ss_total = anova_table["sum_sq"].sum()
    eta_sq = ss_interaction / ss_total

    return {
        "method": "two_way_anova",
        "variable": "trust_by_group_x_gender",
        "statistic": f"F={f_val:.3f}",
        "p_value": round(p_val, 6),
        "effect_size": round(eta_sq, 4),
        "finding": f"The interaction between influencer type and gender on trust was "
                   f"{'significant' if p_val < 0.05 else 'not significant'} "
                   f"(F={f_val:.2f}, p={p_val:.4f}, η²={eta_sq:.3f}).",
        "so_what": "Gender-specific responses to virtual influencers could inform targeted marketing "
                   "campaigns with different influencer types for different demographics.",
        "interdisciplinary": "Gender studies: gendered tech acceptance. Marketing: demographic segmentation. "
                            "HCI: gender differences in AI trust.",
    }


@register_analysis("regression_trust_attitude_pi", "intermediate")
def regression_trust_attitude_pi(df):
    """Multiple regression: trust + attitude → PI."""
    import statsmodels.api as sm

    X = sm.add_constant(df[["trust", "attitude"]])
    y = df["pi"]
    model = sm.OLS(y, X).fit()

    return {
        "method": "multiple_regression",
        "variable": "pi_from_trust_attitude",
        "statistic": f"R²={model.rsquared:.3f}, F={model.fvalue:.3f}",
        "p_value": round(model.f_pvalue, 6),
        "effect_size": round(model.rsquared, 3),
        "finding": f"Trust (β={model.params['trust']:.3f}, p={model.pvalues['trust']:.4f}) and "
                   f"attitude (β={model.params['attitude']:.3f}, p={model.pvalues['attitude']:.4f}) "
                   f"together explain {model.rsquared*100:.1f}% of PI variance.",
        "so_what": "Identifying which psychological lever (trust vs. attitude) more strongly drives "
                   "purchase intent helps brands prioritize their influencer strategy.",
        "interdisciplinary": "Consumer psychology: dual-process models. Advertising: message strategy. "
                            "Economics: willingness-to-pay predictors.",
    }


@register_analysis("mediation_trust", "intermediate")
def mediation_trust(df):
    """Mediation: condition → trust → PI (Baron & Kenny + Sobel)."""
    import statsmodels.api as sm

    # Encode group: virtual=1, human=0
    X = (df["group"] == "virtual").astype(int)

    # Path a: condition → trust
    model_a = sm.OLS(df["trust"], sm.add_constant(X)).fit()
    a = model_a.params.iloc[1]
    se_a = model_a.bse.iloc[1]

    # Path b: trust → PI (controlling for condition)
    X_b = sm.add_constant(pd.DataFrame({"group": X, "trust": df["trust"]}))
    model_b = sm.OLS(df["pi"], X_b).fit()
    b = model_b.params["trust"]
    se_b = model_b.bse["trust"]

    # Path c: condition → PI (total)
    model_c = sm.OLS(df["pi"], sm.add_constant(X)).fit()
    c = model_c.params.iloc[1]

    # Path c': condition → PI (controlling for trust)
    c_prime = model_b.params["group"]

    # Sobel test
    sobel_se = np.sqrt(a**2 * se_b**2 + b**2 * se_a**2)
    sobel_z = (a * b) / sobel_se if sobel_se > 0 else 0
    sobel_p = 2 * (1 - stats.norm.cdf(abs(sobel_z)))
    indirect = a * b

    # Proportion mediated
    prop_med = abs(indirect / c) if c != 0 else 0

    return {
        "method": "mediation_baron_kenny",
        "variable": "condition_trust_pi",
        "statistic": f"indirect={indirect:.3f}, Sobel z={sobel_z:.3f}",
        "p_value": round(sobel_p, 6),
        "effect_size": round(prop_med, 3),
        "finding": f"Trust {'significantly mediates' if sobel_p < 0.05 else 'does not significantly mediate'} "
                   f"the effect of influencer type on PI (indirect={indirect:.3f}, z={sobel_z:.2f}, p={sobel_p:.4f}). "
                   f"Path a={a:.3f}, path b={b:.3f}, c={c:.3f}, c'={c_prime:.3f}.",
        "so_what": "If trust mediates the condition→PI link, brands should focus on building trust "
                   "for virtual influencers rather than just increasing exposure.",
        "interdisciplinary": "Psychology: trust as mechanism. Marketing: customer journey modeling. "
                            "Policy: should disclosures target trust or awareness?",
    }


@register_analysis("moderation_familiarity", "intermediate")
def moderation_familiarity(df):
    """Moderation: condition × VI familiarity → trust."""
    import statsmodels.api as sm

    df_mod = df.dropna(subset=["familiarity"])
    X_group = (df_mod["group"] == "virtual").astype(int)
    fam = df_mod["familiarity"]
    interaction = X_group * fam

    X = sm.add_constant(pd.DataFrame({
        "group": X_group, "familiarity": fam, "interaction": interaction
    }))
    model = sm.OLS(df_mod["trust"], X).fit()

    int_coef = model.params["interaction"]
    int_p = model.pvalues["interaction"]

    return {
        "method": "moderation_regression",
        "variable": "trust_by_group_x_familiarity",
        "statistic": f"interaction β={int_coef:.3f}, t={model.tvalues['interaction']:.3f}",
        "p_value": round(int_p, 6),
        "effect_size": round(model.rsquared, 3),
        "finding": f"VI familiarity {'significantly moderates' if int_p < 0.05 else 'does not significantly moderate'} "
                   f"the effect of condition on trust (β={int_coef:.3f}, p={int_p:.4f}). "
                   f"R²={model.rsquared:.3f}.",
        "so_what": "If familiarity buffers trust deficits, educating consumers about virtual influencers "
                   "could be a viable strategy for brands.",
        "interdisciplinary": "Psychology: mere exposure effect. Technology adoption: TAM model. "
                            "Education: digital literacy as moderator of AI attitudes.",
    }


@register_analysis("manova_all_dvs", "intermediate")
def manova_all_dvs(df):
    """MANOVA: condition → (trust, PI, attitude)."""
    from statsmodels.multivariate.manova import MANOVA

    df_manova = df[["trust", "pi", "attitude", "group"]].dropna()
    manova = MANOVA.from_formula("trust + pi + attitude ~ group", data=df_manova)
    result = manova.mv_test()

    # Extract Pillai's trace
    test_result = result.results["group"]["stat"]
    pillai = test_result.loc["Pillai's trace", "Value"]
    f_val = test_result.loc["Pillai's trace", "F Value"]
    p_val = test_result.loc["Pillai's trace", "Pr > F"]

    return {
        "method": "manova",
        "variable": "trust+pi+attitude_by_group",
        "statistic": f"Pillai's trace={pillai:.3f}, F={f_val:.3f}",
        "p_value": round(p_val, 6),
        "effect_size": round(pillai, 3),
        "finding": f"MANOVA {'revealed' if p_val < 0.05 else 'did not reveal'} a significant multivariate "
                   f"effect of influencer type on the combined DVs (Pillai's={pillai:.3f}, F={f_val:.2f}, p={p_val:.4f}).",
        "so_what": "A multivariate effect confirms that influencer type impacts the constellation of "
                   "consumer responses, not just isolated metrics.",
        "interdisciplinary": "Research methods: multivariate approaches. Marketing: holistic consumer "
                            "response profiles. Psychology: integrated attitude systems.",
    }


# ============================================================
# TIER 3: ADVANCED ANALYSES
# ============================================================

@register_analysis("efa_structure", "advanced")
def efa_structure(df):
    """Exploratory Factor Analysis on trust + PI + attitude items."""
    from factor_analyzer import FactorAnalyzer
    from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo

    items = [f"trust_{i}" for i in range(1, 9)] + \
            [f"pi_{i}" for i in range(1, 5)] + \
            [f"attitude_{i}" for i in range(1, 5)]
    X = df[items].dropna()

    # Adequacy tests
    chi2, p_bartlett = calculate_bartlett_sphericity(X)
    kmo_all, kmo = calculate_kmo(X)

    # Fit 3-factor model
    fa = FactorAnalyzer(n_factors=3, rotation="varimax")
    fa.fit(X)
    loadings = pd.DataFrame(fa.loadings_, index=items, columns=["F1", "F2", "F3"])
    variance = fa.get_factor_variance()
    total_var = sum(variance[1])  # proportion of variance

    return {
        "method": "exploratory_factor_analysis",
        "variable": "all_items_3factor",
        "statistic": f"KMO={kmo:.3f}, Bartlett χ²={chi2:.1f}, variance explained={total_var:.1%}",
        "p_value": round(p_bartlett, 6),
        "effect_size": round(total_var, 3),
        "finding": f"3-factor EFA explains {total_var:.1%} of variance (KMO={kmo:.3f}). "
                   f"Bartlett's test p={p_bartlett:.4f}. Factor structure "
                   f"{'supports' if kmo > 0.6 else 'partially supports'} the trust/PI/attitude distinction.",
        "so_what": "Confirming the factor structure validates that trust, PI, and attitude are "
                   "distinct constructs, not a single 'influencer evaluation' dimension.",
        "interdisciplinary": "Psychometrics: construct validity. Scale development: measurement models. "
                            "Marketing research: survey instrument validation.",
    }


@register_analysis("cluster_analysis", "advanced")
def cluster_analysis(df):
    """K-means clustering of respondents based on trust, PI, attitude."""
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score

    X = df[["trust", "pi", "attitude"]].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Try 2-4 clusters, pick best silhouette
    best_k, best_sil = 2, -1
    for k in range(2, 5):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels)
        if sil > best_sil:
            best_k, best_sil = k, sil

    km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    df_cluster = X.copy()
    df_cluster["cluster"] = labels

    # Cluster profiles
    profiles = df_cluster.groupby("cluster")[["trust", "pi", "attitude"]].mean()
    profile_strs = []
    for c in range(best_k):
        row = profiles.loc[c]
        profile_strs.append(f"C{c}: trust={row['trust']:.2f}, pi={row['pi']:.2f}, att={row['attitude']:.2f}")

    # Check group distribution across clusters
    df_cluster["group"] = df["group"].values[:len(df_cluster)]
    ct = pd.crosstab(df_cluster["cluster"], df_cluster["group"])

    return {
        "method": "kmeans_clustering",
        "variable": "respondent_segments",
        "statistic": f"k={best_k}, silhouette={best_sil:.3f}",
        "p_value": None,
        "effect_size": round(best_sil, 3),
        "finding": f"K-means identified {best_k} respondent segments (silhouette={best_sil:.2f}). "
                   + "; ".join(profile_strs) + ". "
                   f"Group distribution across clusters: {ct.to_dict()}.",
        "so_what": "Consumer segments suggest that virtual influencer campaigns should be tailored — "
                   "high-trust/high-PI segments may respond differently than skeptical segments.",
        "interdisciplinary": "Marketing: consumer segmentation. Psychology: individual differences in AI trust. "
                            "Advertising: audience targeting strategies.",
    }


@register_analysis("path_analysis", "advanced")
def path_analysis(df):
    """Path analysis: condition → trust → attitude → PI (SEM-lite)."""
    import statsmodels.api as sm

    X_group = (df["group"] == "virtual").astype(int)

    # Path 1: condition → trust
    m1 = sm.OLS(df["trust"], sm.add_constant(X_group)).fit()
    path_ct = m1.params.iloc[1]

    # Path 2: condition + trust → attitude
    X2 = sm.add_constant(pd.DataFrame({"group": X_group, "trust": df["trust"]}))
    m2 = sm.OLS(df["attitude"], X2).fit()
    path_ta = m2.params["trust"]
    path_ca = m2.params["group"]

    # Path 3: condition + trust + attitude → PI
    X3 = sm.add_constant(pd.DataFrame({
        "group": X_group, "trust": df["trust"], "attitude": df["attitude"]
    }))
    m3 = sm.OLS(df["pi"], X3).fit()
    path_tp = m3.params["trust"]
    path_ap = m3.params["attitude"]
    path_cp = m3.params["group"]

    # Indirect effects
    indirect_via_trust = path_ct * path_tp
    indirect_via_trust_attitude = path_ct * path_ta * path_ap
    total_indirect = indirect_via_trust + indirect_via_trust_attitude + path_ca * path_ap

    return {
        "method": "path_analysis",
        "variable": "condition_trust_attitude_pi",
        "statistic": f"R²(PI)={m3.rsquared:.3f}",
        "p_value": round(m3.f_pvalue, 6),
        "effect_size": round(m3.rsquared, 3),
        "finding": f"Path model: condition→trust ({path_ct:.3f}), trust→attitude ({path_ta:.3f}), "
                   f"attitude→PI ({path_ap:.3f}), trust→PI ({path_tp:.3f}). "
                   f"Total model R²={m3.rsquared:.3f}. "
                   f"Indirect via trust: {indirect_via_trust:.3f}, "
                   f"via trust→attitude: {indirect_via_trust_attitude:.3f}.",
        "so_what": "The path model reveals whether trust or attitude is the more critical mediator, "
                   "guiding where brands should intervene in the consumer decision chain.",
        "interdisciplinary": "Psychology: causal chain modeling. Marketing: customer journey optimization. "
                            "HCI: trust→adoption pathways in human-AI interaction.",
    }


# ============================================================
# TIER 4: CREATIVE ANALYSES
# ============================================================

@register_analysis("bayesian_ttest_trust", "creative")
def bayesian_ttest_trust(df):
    """Bayesian independent t-test for trust using pingouin."""
    import pingouin as pg

    result = pg.ttest(
        df[df["group"] == "virtual"]["trust"],
        df[df["group"] == "human"]["trust"],
        alternative="two-sided"
    )
    bf = float(result["BF10"].values[0])
    d = float(result["cohen-d"].values[0])
    p = float(result["p-val"].values[0])

    # Interpret BF
    if bf > 100:
        bf_interp = "extreme evidence"
    elif bf > 30:
        bf_interp = "very strong evidence"
    elif bf > 10:
        bf_interp = "strong evidence"
    elif bf > 3:
        bf_interp = "moderate evidence"
    elif bf > 1:
        bf_interp = "anecdotal evidence"
    else:
        bf_interp = "evidence favoring null"

    return {
        "method": "bayesian_ttest",
        "variable": "trust",
        "statistic": f"BF10={bf:.3f}, d={d:.3f}",
        "p_value": round(p, 6),
        "effect_size": round(abs(d), 3),
        "finding": f"Bayesian t-test: BF10={bf:.2f} ({bf_interp} for group difference), "
                   f"Cohen's d={d:.2f}.",
        "so_what": "Bayes factors provide evidence strength rather than binary significance — "
                   "useful for small samples where NHST may lack power.",
        "interdisciplinary": "Statistics: Bayesian vs. frequentist debate. Replication crisis: "
                            "accumulating evidence across studies. Policy: evidence standards for regulation.",
    }


@register_analysis("bootstrap_ci_trust", "creative")
def bootstrap_ci_trust(df):
    """Bootstrap confidence intervals for trust difference."""
    v = df[df["group"] == "virtual"]["trust"].values
    h = df[df["group"] == "human"]["trust"].values
    observed_diff = h.mean() - v.mean()

    n_boot = 10000
    rng = np.random.RandomState(42)
    boot_diffs = []
    for _ in range(n_boot):
        v_boot = rng.choice(v, size=len(v), replace=True)
        h_boot = rng.choice(h, size=len(h), replace=True)
        boot_diffs.append(h_boot.mean() - v_boot.mean())

    boot_diffs = np.array(boot_diffs)
    ci_lower = np.percentile(boot_diffs, 2.5)
    ci_upper = np.percentile(boot_diffs, 97.5)
    # Proportion of bootstrap samples where diff > 0
    prop_positive = np.mean(boot_diffs > 0)

    return {
        "method": "bootstrap_ci",
        "variable": "trust_difference",
        "statistic": f"diff={observed_diff:.3f}, 95% CI=[{ci_lower:.3f}, {ci_upper:.3f}]",
        "p_value": round(min(prop_positive, 1 - prop_positive) * 2, 6),
        "effect_size": round(abs(observed_diff), 3),
        "finding": f"Bootstrap (10,000 resamples): Human-Virtual trust difference = {observed_diff:.3f}, "
                   f"95% CI [{ci_lower:.3f}, {ci_upper:.3f}]. "
                   f"{'CI excludes zero → significant' if ci_lower > 0 or ci_upper < 0 else 'CI includes zero → not significant'}.",
        "so_what": "Distribution-free confidence intervals provide robust uncertainty estimates "
                   "critical for small-sample research.",
        "interdisciplinary": "Methodology: resampling methods for small-N. Industry: uncertainty "
                            "quantification for marketing decisions.",
    }


@register_analysis("power_analysis", "creative")
def power_analysis(df):
    """Post-hoc power analysis for the t-test on trust."""
    from scipy.stats import norm

    v = df[df["group"] == "virtual"]["trust"]
    h = df[df["group"] == "human"]["trust"]
    d = cohens_d(h, v)
    n1, n2 = len(v), len(h)

    # Power calculation for two-sample t-test
    alpha = 0.05
    z_alpha = norm.ppf(1 - alpha / 2)
    se = np.sqrt(1/n1 + 1/n2)
    ncp = abs(d) / se  # non-centrality parameter
    power = 1 - norm.cdf(z_alpha - ncp)

    # Required N for 80% power
    z_beta = norm.ppf(0.80)
    required_per_group = int(np.ceil(((z_alpha + z_beta) / abs(d))**2 * 2)) if abs(d) > 0 else 999

    return {
        "method": "power_analysis",
        "variable": "trust_ttest_power",
        "statistic": f"power={power:.3f}, required_n_per_group={required_per_group}",
        "p_value": None,
        "effect_size": round(abs(d), 3),
        "finding": f"Post-hoc power for trust t-test (d={d:.2f}): {power:.1%}. "
                   f"For 80% power at this effect size, need {required_per_group} per group "
                   f"(have {n1}/{n2}).",
        "so_what": f"{'Adequate power suggests reliable findings.' if power > 0.8 else 'Low power suggests results should be interpreted with caution and replicated.'} "
                   f"Future studies should plan for N≥{required_per_group} per group.",
        "interdisciplinary": "Research design: sample size planning. Grant writing: power justification. "
                            "Replication: minimum sample requirements for effect detection.",
    }


@register_analysis("network_correlation", "creative")
def network_correlation(df):
    """Network correlation analysis — variable relationship structure."""
    vars_to_use = ["trust", "pi", "attitude", "familiarity"]
    corr_matrix = df[vars_to_use].corr()

    # Find strongest and weakest correlations
    pairs = []
    for i, v1 in enumerate(vars_to_use):
        for j, v2 in enumerate(vars_to_use):
            if i < j:
                r = corr_matrix.loc[v1, v2]
                pairs.append((v1, v2, r))

    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    strongest = pairs[0]
    weakest = pairs[-1]

    # Average absolute correlation
    avg_r = np.mean([abs(p[2]) for p in pairs])

    return {
        "method": "network_correlation",
        "variable": "all_variables",
        "statistic": f"avg|r|={avg_r:.3f}",
        "p_value": None,
        "effect_size": round(avg_r, 3),
        "finding": f"Network correlation analysis: strongest link {strongest[0]}-{strongest[1]} "
                   f"(r={strongest[2]:.3f}), weakest {weakest[0]}-{weakest[1]} (r={weakest[2]:.3f}). "
                   f"Average |r|={avg_r:.3f}.",
        "so_what": "The variable network reveals which constructs are most tightly coupled, "
                   "suggesting intervention points for influencer campaigns.",
        "interdisciplinary": "Network science: psychological variable systems. Marketing: "
                            "construct interrelationships. Data science: feature correlation structure.",
    }


@register_analysis("response_heatmap_data", "creative")
def response_heatmap_data(df):
    """Response pattern analysis — Likert distribution by item and group."""
    trust_items = [f"trust_{i}" for i in range(1, 9)]
    pi_items = [f"pi_{i}" for i in range(1, 5)]

    # Check if response patterns differ between groups
    pattern_diffs = []
    for item in trust_items + pi_items:
        v = df[df["group"] == "virtual"][item]
        h = df[df["group"] == "human"][item]
        u_stat, p = stats.mannwhitneyu(v, h, alternative="two-sided")
        pattern_diffs.append({"item": item, "p": p, "v_mean": v.mean(), "h_mean": h.mean()})

    sig_items = [d for d in pattern_diffs if d["p"] < 0.05]
    nonsig_items = [d for d in pattern_diffs if d["p"] >= 0.05]

    return {
        "method": "item_level_analysis",
        "variable": "trust_pi_items",
        "statistic": f"significant_items={len(sig_items)}/{len(pattern_diffs)}",
        "p_value": None,
        "effect_size": None,
        "finding": f"Item-level analysis: {len(sig_items)} of {len(pattern_diffs)} items show "
                   f"significant group differences. "
                   + (f"Significant items: {', '.join(d['item'] for d in sig_items)}." if sig_items else "No individual items reached significance."),
        "so_what": "Item-level patterns reveal which specific trust/PI aspects drive composite differences — "
                   "actionable for message strategy.",
        "interdisciplinary": "Psychometrics: differential item functioning. UX: specific trust facets. "
                            "Content strategy: which claims resonate.",
    }


# ============================================================
# TIER 5: INTERDISCIPLINARY / META ANALYSES
# ============================================================

@register_analysis("effect_size_summary", "interdisciplinary")
def effect_size_summary(df):
    """Forest-plot data: effect sizes for all DVs."""
    effects = []
    for var in ["trust", "pi", "attitude"]:
        v = df[df["group"] == "virtual"][var]
        h = df[df["group"] == "human"][var]
        d = cohens_d(h, v)
        t_stat, p = stats.ttest_ind(v, h)

        # CI for Cohen's d (approximate)
        n1, n2 = len(v), len(h)
        se_d = np.sqrt((n1 + n2) / (n1 * n2) + d**2 / (2 * (n1 + n2)))
        ci_lower = d - 1.96 * se_d
        ci_upper = d + 1.96 * se_d

        effects.append({
            "variable": var, "d": d, "ci_lower": ci_lower,
            "ci_upper": ci_upper, "p": p
        })

    summary = "; ".join(
        f"{e['variable']}: d={e['d']:.2f} [{e['ci_lower']:.2f}, {e['ci_upper']:.2f}]"
        for e in effects
    )

    return {
        "method": "effect_size_forest",
        "variable": "all_dvs",
        "statistic": summary,
        "p_value": None,
        "effect_size": round(np.mean([abs(e["d"]) for e in effects]), 3),
        "finding": f"Effect sizes across DVs: {summary}. "
                   f"Average |d| = {np.mean([abs(e['d']) for e in effects]):.2f}.",
        "so_what": "The effect size landscape shows which outcomes are most and least affected by "
                   "influencer type — essential for meta-analytic accumulation.",
        "interdisciplinary": "Meta-analysis: effect size reporting standards. Replication: "
                            "comparative effect magnitudes. Industry: practical significance assessment.",
    }


@register_analysis("stakeholder_matrix", "interdisciplinary")
def stakeholder_matrix(df):
    """Stakeholder impact matrix — who should use these findings?"""
    v_trust = df[df["group"] == "virtual"]["trust"].mean()
    h_trust = df[df["group"] == "human"]["trust"].mean()
    v_pi = df[df["group"] == "virtual"]["pi"].mean()
    h_pi = df[df["group"] == "human"]["pi"].mean()
    trust_diff = h_trust - v_trust
    pi_diff = h_pi - v_pi

    stakeholders = {
        "Brand Marketers": f"Trust gap of {trust_diff:.2f} points suggests virtual influencers need complementary trust signals.",
        "Ad Agencies": f"PI difference of {pi_diff:.2f} points informs channel allocation between human and virtual endorsers.",
        "Platform Designers": "UX patterns for virtual influencer profiles should emphasize authenticity cues.",
        "Regulators": "Disclosure requirements may need updating as virtual influencers become indistinguishable.",
        "Academic Researchers": f"N={len(df)} provides baseline effects for power analysis in replication studies.",
    }

    matrix_str = " | ".join(f"{k}: {v}" for k, v in stakeholders.items())

    return {
        "method": "stakeholder_impact_matrix",
        "variable": "cross_domain",
        "statistic": f"5 stakeholder groups identified",
        "p_value": None,
        "effect_size": None,
        "finding": f"Stakeholder analysis identifies 5 key groups impacted by these findings. "
                   + matrix_str,
        "so_what": "Translating academic findings into stakeholder-specific action items "
                   "maximizes research impact beyond the academic community.",
        "interdisciplinary": "Knowledge translation: research-to-practice pipeline. Science communication: "
                            "audience-specific messaging. Public policy: evidence-based regulation.",
    }


@register_analysis("cross_domain_implications", "interdisciplinary")
def cross_domain_implications(df):
    """Cross-domain implications analysis."""
    v_trust = df[df["group"] == "virtual"]["trust"].mean()
    h_trust = df[df["group"] == "human"]["trust"].mean()
    d_trust = cohens_d(
        df[df["group"] == "human"]["trust"],
        df[df["group"] == "virtual"]["trust"]
    )

    domains = {
        "Psychology": f"Parasocial relationships with AI differ from human bonds (d={d_trust:.2f}). "
                     "Extends theory on source credibility in computer-mediated communication.",
        "HCI": "Virtual influencer interfaces need trust-calibration mechanisms. "
              "Design implications for human-AI interaction patterns.",
        "Public Health": "If virtual influencers promote health products, lower trust may reduce "
                        "adoption of beneficial behaviors — a double-edged sword.",
        "Policy": "FTC/regulatory frameworks may need virtual influencer-specific disclosure guidelines "
                 "as consumer trust heuristics differ from human endorsers.",
        "Industry": f"Virtual influencers average {v_trust:.2f} vs human {h_trust:.2f} on trust. "
                   "Cost savings must be weighed against potential trust penalties.",
    }

    return {
        "method": "cross_domain_analysis",
        "variable": "five_domain_implications",
        "statistic": "5 domains analyzed",
        "p_value": None,
        "effect_size": round(abs(d_trust), 3),
        "finding": " | ".join(f"{k}: {v}" for k, v in domains.items()),
        "so_what": "Interdisciplinary framing transforms a single experiment into a multi-stakeholder "
                   "research contribution with broader impact.",
        "interdisciplinary": " | ".join(f"{k}: {v}" for k, v in domains.items()),
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-latest", action="store_true",
                        help="Run the most recently registered analysis")
    parser.add_argument("--run-all", action="store_true",
                        help="Run all registered analyses")
    parser.add_argument("--run", type=str,
                        help="Run a specific analysis by name")
    parser.add_argument("--list", action="store_true",
                        help="List all registered analyses")
    args = parser.parse_args()

    if args.list:
        for name, entry in _REGISTRY.items():
            print(f"  {name} ({entry['category']})")
    elif args.run:
        run_analysis(args.run)
    elif args.run_latest:
        names = list(_REGISTRY.keys())
        if names:
            run_analysis(names[-1])
    elif args.run_all:
        results = run_all()
        print(f"\n=== Summary: {len(results)} analyses run ===")
        kept = [r for r in results if r["decision"] == "KEEP"]
        discarded = [r for r in results if r["decision"] == "DISCARD"]
        print(f"KEEP: {len(kept)}, DISCARD: {len(discarded)}")
    else:
        parser.print_help()

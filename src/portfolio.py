"""
Portfolio HTML generator for ADV382 autoresearch results.
THIS FILE IS FIXED SCAFFOLD — DO NOT MODIFY.

Combines KEEP results + best visualizations into a standalone HTML page.
Editorial magazine aesthetic with narrative-first storytelling.
"""

import os
import sys
import csv
import base64
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
RESULTS_TSV = os.path.join(OUTPUT_DIR, "results.tsv")
FIGURES_DIR = os.path.join(OUTPUT_DIR, "figures")
PORTFOLIO_DIR = os.path.join(OUTPUT_DIR, "portfolio")


def load_results():
    """Load results from TSV."""
    results = []
    with open(RESULTS_TSV, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            results.append(row)
    return results


def img_to_base64(path):
    """Convert image to base64 data URI for standalone HTML."""
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"


def get_figure_mapping():
    """Map analysis methods to their best visualization."""
    return {
        "independent_ttest": ["grouped_bar_dvs", "violin_trust", "violin_pi", "forest_plot"],
        "mann_whitney_u": ["violin_trust", "forest_plot"],
        "multiple_regression": ["regression_scatter", "correlation_heatmap"],
        "mediation_baron_kenny": ["mediation_diagram"],
        "exploratory_factor_analysis": ["correlation_heatmap"],
        "kmeans_clustering": ["cluster_scatter"],
        "path_analysis": ["mediation_diagram", "regression_scatter"],
        "bayesian_ttest": ["forest_plot", "violin_trust"],
        "bootstrap_ci": ["forest_plot"],
        "effect_size_forest": ["forest_plot", "effect_size_comparison"],
        "cross_domain_analysis": ["radar_profile"],
        "item_level_analysis": ["likert_distribution"],
        "network_correlation": ["correlation_heatmap"],
        "stakeholder_impact_matrix": ["radar_profile"],
    }


# ─── Narrative builders ───

def _build_headline_insight(kept):
    """Extract the single most compelling insight for the hero."""
    # Find the trust t-test result
    for r in kept:
        if r.get("method") == "independent_ttest" and "trust" in r.get("variable", ""):
            return r
    return kept[0] if kept else {}


def _build_three_takeaways(kept):
    """Build three headline takeaways for the narrative section."""
    takeaways = []

    # 1. Trust gap
    for r in kept:
        if r.get("method") == "independent_ttest" and "trust" in r.get("variable", ""):
            takeaways.append({
                "number": "01",
                "headline": "The Trust Gap Is Real",
                "body": r.get("finding", ""),
                "so_what": r.get("so_what", ""),
                "figure": "violin_trust",
            })
            break

    # 2. Mediation / mechanism
    for r in kept:
        if "mediation" in r.get("method", ""):
            takeaways.append({
                "number": "02",
                "headline": "Trust Is the Mechanism, Not Just a Symptom",
                "body": r.get("finding", ""),
                "so_what": r.get("so_what", ""),
                "figure": "mediation_diagram",
            })
            break

    # 3. Attitude or regression
    for r in kept:
        if r.get("method") == "multiple_regression":
            takeaways.append({
                "number": "03",
                "headline": "Attitude Drives Purchase More Than Trust",
                "body": r.get("finding", ""),
                "so_what": r.get("so_what", ""),
                "figure": "regression_scatter",
            })
            break

    # Fill remaining if needed
    if len(takeaways) < 3:
        for r in kept:
            already = {t["headline"] for t in takeaways}
            if r.get("finding", "")[:30] not in [t["body"][:30] for t in takeaways]:
                takeaways.append({
                    "number": f"0{len(takeaways)+1}",
                    "headline": r.get("method", "").replace("_", " ").title(),
                    "body": r.get("finding", ""),
                    "so_what": r.get("so_what", ""),
                    "figure": None,
                })
                if len(takeaways) >= 3:
                    break

    return takeaways


def _build_so_what_grid(kept):
    """Build the 'So What' implications grid from all KEEP results."""
    # Collect all so_what and interdisciplinary content
    implications = {
        "For Brand Marketers": [],
        "For Policymakers": [],
        "For Researchers": [],
        "For Platform Designers": [],
    }

    for r in kept:
        sw = r.get("so_what", "")
        inter = r.get("interdisciplinary", "")
        combined = sw + " " + inter

        if any(w in combined.lower() for w in ["brand", "market", "campaign", "advertis", "agency"]):
            implications["For Brand Marketers"].append(sw)
        if any(w in combined.lower() for w in ["policy", "regulat", "ftc", "disclos", "legal"]):
            implications["For Policymakers"].append(sw)
        if any(w in combined.lower() for w in ["research", "study", "replicate", "method", "power", "sample"]):
            implications["For Researchers"].append(sw)
        if any(w in combined.lower() for w in ["hci", "design", "interface", "ux", "platform"]):
            implications["For Platform Designers"].append(sw)

    return implications


def generate_portfolio():
    """Generate the full portfolio HTML."""
    os.makedirs(PORTFOLIO_DIR, exist_ok=True)

    results = load_results()
    kept = [r for r in results if r.get("decision") == "KEEP"]
    discarded = [r for r in results if r.get("decision") == "DISCARD"]
    fig_map = get_figure_mapping()

    # Load all figures as base64
    fig_data = {}
    if os.path.isdir(FIGURES_DIR):
        for png in os.listdir(FIGURES_DIR):
            if png.endswith(".png"):
                name = png.replace(".png", "")
                fig_data[name] = img_to_base64(os.path.join(FIGURES_DIR, png))

    # Build narrative elements
    headline = _build_headline_insight(kept)
    takeaways = _build_three_takeaways(kept)
    so_what_grid = _build_so_what_grid(kept)

    # ─── TAKEAWAY SECTION HTML ───
    takeaway_html = ""
    for i, t in enumerate(takeaways):
        fig_src = fig_data.get(t.get("figure", ""), "")
        direction = "normal" if i % 2 == 0 else "reverse"
        takeaway_html += f"""
        <div class="takeaway {'takeaway--reverse' if i % 2 != 0 else ''}" data-reveal>
            <div class="takeaway__text">
                <span class="takeaway__number">{t['number']}</span>
                <h3 class="takeaway__headline">{t['headline']}</h3>
                <p class="takeaway__body">{t['body']}</p>
                <div class="takeaway__sowhat">
                    <span class="sowhat-label">So what?</span>
                    <p>{t['so_what']}</p>
                </div>
            </div>
            {'<div class="takeaway__figure"><img src="' + fig_src + '" alt="' + t.get("headline","") + '"></div>' if fig_src else ''}
        </div>
        """

    # ─── SO WHAT GRID HTML ───
    sowhat_cards = ""
    icons = {
        "For Brand Marketers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"/></svg>',
        "For Policymakers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z"/></svg>',
        "For Researchers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"/></svg>',
        "For Platform Designers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25"/></svg>',
    }

    for stakeholder, items in so_what_grid.items():
        if not items:
            continue
        # Deduplicate and take best 2
        seen = set()
        unique = []
        for item in items:
            short = item[:60]
            if short not in seen and item.strip():
                seen.add(short)
                unique.append(item)
        unique = unique[:2]
        if not unique:
            continue

        icon = icons.get(stakeholder, "")
        sowhat_cards += f"""
        <div class="sowhat-card" data-reveal>
            <div class="sowhat-card__icon">{icon}</div>
            <h4 class="sowhat-card__title">{stakeholder}</h4>
            <ul class="sowhat-card__list">
                {''.join(f'<li>{item}</li>' for item in unique)}
            </ul>
        </div>
        """

    # ─── EVIDENCE GALLERY ───
    gallery_order = ["grouped_bar_dvs", "forest_plot", "violin_trust",
                     "mediation_diagram", "radar_profile", "correlation_heatmap",
                     "regression_scatter", "cluster_scatter", "likert_distribution",
                     "effect_size_comparison", "violin_pi"]
    gallery_labels = {
        "grouped_bar_dvs": "Group Comparison Across All DVs",
        "forest_plot": "Effect Size Forest Plot",
        "violin_trust": "Trust Score Distribution",
        "mediation_diagram": "Mediation Path Model",
        "radar_profile": "Group Profile Radar",
        "correlation_heatmap": "Variable Correlation Matrix",
        "regression_scatter": "Trust-PI Regression by Group",
        "cluster_scatter": "Consumer Segments",
        "likert_distribution": "Item Response Patterns",
        "effect_size_comparison": "Effect Size Benchmarks",
        "violin_pi": "Purchase Intention Distribution",
    }
    gallery_html = ""
    for fig_name in gallery_order:
        if fig_name in fig_data and fig_data[fig_name]:
            label = gallery_labels.get(fig_name, fig_name.replace("_", " ").title())
            size_class = "gallery__item--wide" if fig_name in ["grouped_bar_dvs", "mediation_diagram", "likert_distribution"] else ""
            gallery_html += f"""
            <div class="gallery__item {size_class}" data-reveal>
                <img src="{fig_data[fig_name]}" alt="{label}" loading="lazy">
                <p class="gallery__caption">{label}</p>
            </div>
            """

    # ─── ADDITIONAL FINDINGS ───
    additional_html = ""
    # Skip the ones already in takeaways
    takeaway_methods = set()
    for t in takeaways:
        # Find matching kept result
        for r in kept:
            if t["body"] == r.get("finding", ""):
                takeaway_methods.add((r.get("method",""), r.get("variable","")))

    for r in kept:
        key = (r.get("method",""), r.get("variable",""))
        if key in takeaway_methods:
            continue
        category = r.get("category", "")
        badge_colors = {
            "basic": "#2563EB", "intermediate": "#7C3AED",
            "advanced": "#DB2777", "creative": "#D97706",
            "interdisciplinary": "#059669"
        }
        badge_color = badge_colors.get(category, "#64748B")
        method_label = r.get("method", "").replace("_", " ").title()
        score = r.get("score_total", "")

        figs = fig_map.get(r.get("method", ""), [])
        fig_src = fig_data.get(figs[0], "") if figs else ""

        additional_html += f"""
        <div class="finding" data-reveal>
            <div class="finding__header">
                <span class="finding__badge" style="--badge-color: {badge_color}">{category}</span>
                <span class="finding__score">{score}/100</span>
            </div>
            <h4 class="finding__method">{method_label}</h4>
            <p class="finding__text">{r.get('finding', '')}</p>
            <div class="finding__insight">
                <div class="finding__sowhat">
                    <span class="finding__label">So what?</span>
                    <p>{r.get('so_what', '')}</p>
                </div>
                <div class="finding__inter">
                    <span class="finding__label">Across disciplines</span>
                    <p>{r.get('interdisciplinary', '')}</p>
                </div>
            </div>
            {'<img class="finding__fig" src="' + fig_src + '" alt="' + method_label + '">' if fig_src else ''}
        </div>
        """

    # ─── TRANSPARENCY TABLE ───
    transparency_rows = ""
    for r in results:
        dec = r.get("decision", "")
        dec_class = "keep" if dec == "KEEP" else "discard"
        transparency_rows += f"""
        <tr class="transparency__{dec_class}">
            <td class="transparency__method">{r.get('method', '').replace('_', ' ')}</td>
            <td>{r.get('variable', '').replace('_', ' ')}</td>
            <td><span class="transparency__cat">{r.get('category', '')}</span></td>
            <td class="transparency__score">{r.get('score_total', '')}</td>
            <td><span class="transparency__decision transparency__decision--{dec_class}">{dec}</span></td>
        </tr>
        """

    # ─── INTERDISCIPLINARY DEEP DIVE ───
    domains_content = {
        "Psychology": "Parasocial relationships with AI entities follow fundamentally different developmental trajectories than human bonds. Our finding of a medium trust gap (d=0.55) between virtual and human influencers extends source credibility theory into non-human endorser contexts and raises questions about the uncanny valley effect in commercial settings.",
        "Human-Computer Interaction": "The trust deficit we observe suggests that virtual influencer interfaces need explicit trust-calibration mechanisms. Design patterns borrowed from explainable AI research could help bridge the gap. The path model (condition&#8594;trust&#8594;attitude&#8594;PI) provides a blueprint for where design interventions would be most effective.",
        "Public Health Communication": "If virtual influencers are deployed for health product endorsements, the lower trust they engender may reduce adoption of beneficial behaviors. This is a double-edged sword: synthetic endorsers could reach larger audiences but with diminished persuasive impact on health-related decisions.",
        "Regulatory Policy": "Current FTC disclosure frameworks were designed for human endorsers. Our data suggests consumer trust heuristics differ fundamentally for virtual influencers, warranting virtual-influencer-specific disclosure guidelines and consumer protection standards.",
        "Industry Strategy": "Virtual influencers average 2.32 vs. human 2.71 on trust (5-point scale). The cost savings from controllable, scandal-free virtual influencers must be weighed against this 0.39-point trust penalty. Our cluster analysis reveals distinct consumer segments that respond differently &#8212; suggesting targeted deployment rather than wholesale replacement.",
    }

    domains_html = ""
    domain_icons = {
        "Psychology": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18"/></svg>',
        "Human-Computer Interaction": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3"/></svg>',
        "Public Health Communication": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"/></svg>',
        "Regulatory Policy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.97zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.97z"/></svg>',
        "Industry Strategy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6"/></svg>',
    }

    for domain, content in domains_content.items():
        icon = domain_icons.get(domain, "")
        domains_html += f"""
        <div class="domain" data-reveal>
            <div class="domain__icon">{icon}</div>
            <h4 class="domain__title">{domain}</h4>
            <p class="domain__text">{content}</p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Virtual vs. Human Influencers | ADV382 Research Portfolio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* ═══════════════════════════════════════════
   DESIGN TOKENS
   ═══════════════════════════════════════════ */
:root {{
    /* Warm editorial palette */
    --ink: #1A1614;
    --ink-secondary: #4A4543;
    --ink-muted: #7A7674;
    --paper: #FDFBF9;
    --paper-warm: #F7F3EF;
    --paper-deep: #EDE8E3;
    --accent: #B44D2D;
    --accent-light: #D4785C;
    --accent-pale: #F5E6DF;
    --teal: #1A6B5A;
    --teal-pale: #DFF0EB;
    --violet: #5B3E8A;
    --violet-pale: #EDE5F5;
    --gold: #A67C2E;
    --gold-pale: #F5EDD8;
    --slate: #8B8685;
    --rule: #DDD8D4;
    --rule-light: #EDE9E5;

    /* Typography */
    --serif: 'Crimson Pro', Georgia, 'Times New Roman', serif;
    --sans: 'Atkinson Hyperlegible', system-ui, -apple-system, sans-serif;
    --mono: 'IBM Plex Mono', 'Menlo', monospace;

    /* Spacing */
    --s1: 0.25rem;
    --s2: 0.5rem;
    --s3: 0.75rem;
    --s4: 1rem;
    --s5: 1.5rem;
    --s6: 2rem;
    --s7: 3rem;
    --s8: 4rem;
    --s9: 6rem;
    --s10: 8rem;
}}

/* ═══════════════════════════════════════════
   RESET & BASE
   ═══════════════════════════════════════════ */
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

html {{ scroll-behavior: smooth; }}

body {{
    font-family: var(--sans);
    background: var(--paper);
    color: var(--ink);
    line-height: 1.65;
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

img {{ max-width: 100%; height: auto; display: block; }}

/* Grain overlay */
body::after {{
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 9999;
    opacity: 0.018;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}}

/* ═══════════════════════════════════════════
   SCROLL REVEAL
   ═══════════════════════════════════════════ */
[data-reveal] {{
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}}
[data-reveal].visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* ═══════════════════════════════════════════
   NAV
   ═══════════════════════════════════════════ */
.nav {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    padding: var(--s4) var(--s6);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(253,251,249,0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid transparent;
    transition: border-color 0.3s;
}}
.nav.scrolled {{ border-bottom-color: var(--rule); }}
.nav__brand {{
    font-family: var(--serif);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--ink);
    text-decoration: none;
    letter-spacing: -0.01em;
}}
.nav__links {{
    display: flex;
    gap: var(--s5);
    list-style: none;
}}
.nav__links a {{
    font-size: 0.8rem;
    color: var(--ink-muted);
    text-decoration: none;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    transition: color 0.2s;
}}
.nav__links a:hover {{ color: var(--accent); }}

/* ═══════════════════════════════════════════
   HERO
   ═══════════════════════════════════════════ */
.hero {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: var(--s10) var(--s6) var(--s9);
    position: relative;
    overflow: hidden;
}}
.hero::before {{
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 55%;
    height: 100%;
    background: linear-gradient(135deg, var(--accent-pale) 0%, var(--paper) 60%, transparent 100%);
    clip-path: polygon(25% 0, 100% 0, 100% 100%, 0% 100%);
    opacity: 0.5;
}}
.hero__inner {{
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--s8);
    align-items: center;
}}
.hero__text {{ max-width: 560px; }}
.hero__eyebrow {{
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: var(--s5);
    display: flex;
    align-items: center;
    gap: var(--s3);
}}
.hero__eyebrow::before {{
    content: '';
    display: inline-block;
    width: 32px;
    height: 1px;
    background: var(--accent);
}}
.hero h1 {{
    font-family: var(--serif);
    font-size: clamp(2.6rem, 5vw, 4.2rem);
    line-height: 1.08;
    font-weight: 300;
    letter-spacing: -0.02em;
    margin-bottom: var(--s5);
    color: var(--ink);
}}
.hero h1 strong {{
    font-weight: 600;
    color: var(--accent);
}}
.hero__subtitle {{
    font-size: 1.1rem;
    line-height: 1.7;
    color: var(--ink-secondary);
    margin-bottom: var(--s7);
    max-width: 480px;
}}
.hero__stats {{
    display: flex;
    gap: var(--s7);
}}
.hero__stat {{
    text-align: left;
}}
.hero__stat-num {{
    font-family: var(--serif);
    font-size: 2.8rem;
    font-weight: 300;
    color: var(--accent);
    line-height: 1;
    letter-spacing: -0.03em;
}}
.hero__stat-label {{
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--ink-muted);
    margin-top: var(--s1);
}}
.hero__figure {{
    position: relative;
}}
.hero__figure img {{
    border-radius: 8px;
    box-shadow: 0 24px 80px rgba(26,22,20,0.08), 0 4px 16px rgba(26,22,20,0.04);
}}
.hero__figure::after {{
    content: '';
    position: absolute;
    inset: 12px -12px -12px 12px;
    border: 1px solid var(--rule);
    border-radius: 8px;
    z-index: -1;
}}

/* ═══════════════════════════════════════════
   SECTIONS
   ═══════════════════════════════════════════ */
.section {{
    padding: var(--s9) var(--s6);
}}
.section__inner {{
    max-width: 1200px;
    margin: 0 auto;
}}
.section__label {{
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: var(--s3);
    display: flex;
    align-items: center;
    gap: var(--s3);
}}
.section__label::before {{
    content: '';
    display: inline-block;
    width: 24px;
    height: 1px;
    background: var(--accent);
}}
.section__title {{
    font-family: var(--serif);
    font-size: clamp(1.8rem, 3.5vw, 2.8rem);
    font-weight: 400;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin-bottom: var(--s4);
    max-width: 700px;
}}
.section__desc {{
    font-size: 1.05rem;
    color: var(--ink-secondary);
    max-width: 600px;
    margin-bottom: var(--s8);
    line-height: 1.7;
}}

/* ═══════════════════════════════════════════
   METHOD CARDS
   ═══════════════════════════════════════════ */
.method-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--s5);
}}
.method-card {{
    background: white;
    border: 1px solid var(--rule-light);
    border-radius: 10px;
    padding: var(--s6);
    transition: transform 0.25s cubic-bezier(0.16,1,0.3,1), box-shadow 0.25s;
}}
.method-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(26,22,20,0.06);
}}
.method-card h4 {{
    font-family: var(--serif);
    font-size: 1.3rem;
    font-weight: 500;
    margin-bottom: var(--s3);
    color: var(--ink);
}}
.method-card p {{
    font-size: 0.9rem;
    color: var(--ink-secondary);
    line-height: 1.65;
}}

/* ═══════════════════════════════════════════
   TAKEAWAYS — THE MAIN STORY
   ═══════════════════════════════════════════ */
.takeaway {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--s8);
    align-items: center;
    padding: var(--s8) 0;
    border-bottom: 1px solid var(--rule-light);
}}
.takeaway--reverse {{ direction: rtl; }}
.takeaway--reverse > * {{ direction: ltr; }}
.takeaway:last-child {{ border-bottom: none; }}
.takeaway__number {{
    font-family: var(--serif);
    font-size: 4rem;
    font-weight: 300;
    color: var(--accent-pale);
    line-height: 1;
    display: block;
    margin-bottom: var(--s3);
    letter-spacing: -0.04em;
}}
.takeaway__headline {{
    font-family: var(--serif);
    font-size: 1.8rem;
    font-weight: 500;
    line-height: 1.2;
    margin-bottom: var(--s4);
    color: var(--ink);
    letter-spacing: -0.01em;
}}
.takeaway__body {{
    font-size: 1rem;
    color: var(--ink-secondary);
    line-height: 1.7;
    margin-bottom: var(--s5);
}}
.takeaway__sowhat {{
    background: var(--accent-pale);
    border-left: 3px solid var(--accent);
    padding: var(--s4) var(--s5);
    border-radius: 0 8px 8px 0;
}}
.sowhat-label {{
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    display: block;
    margin-bottom: var(--s2);
}}
.takeaway__sowhat p {{
    font-size: 0.95rem;
    color: var(--ink);
    line-height: 1.65;
    font-style: italic;
}}
.takeaway__figure {{
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(26,22,20,0.06);
    border: 1px solid var(--rule-light);
}}
.takeaway__figure img {{
    width: 100%;
}}

/* ═══════════════════════════════════════════
   SO WHAT GRID
   ═══════════════════════════════════════════ */
.sowhat-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--s5);
}}
.sowhat-card {{
    background: white;
    border: 1px solid var(--rule-light);
    border-radius: 12px;
    padding: var(--s6);
    transition: transform 0.25s cubic-bezier(0.16,1,0.3,1), box-shadow 0.25s;
}}
.sowhat-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 16px 48px rgba(26,22,20,0.07);
}}
.sowhat-card__icon {{
    width: 40px;
    height: 40px;
    color: var(--accent);
    margin-bottom: var(--s4);
}}
.sowhat-card__icon svg {{
    width: 100%;
    height: 100%;
}}
.sowhat-card__title {{
    font-family: var(--serif);
    font-size: 1.25rem;
    font-weight: 500;
    margin-bottom: var(--s4);
    color: var(--ink);
}}
.sowhat-card__list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: var(--s3);
}}
.sowhat-card__list li {{
    font-size: 0.9rem;
    color: var(--ink-secondary);
    line-height: 1.6;
    padding-left: var(--s5);
    position: relative;
}}
.sowhat-card__list li::before {{
    content: '';
    position: absolute;
    left: 0;
    top: 0.55em;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-light);
}}

/* ═══════════════════════════════════════════
   EVIDENCE GALLERY
   ═══════════════════════════════════════════ */
.gallery {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--s5);
}}
.gallery__item {{
    background: white;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--rule-light);
    transition: transform 0.25s cubic-bezier(0.16,1,0.3,1), box-shadow 0.25s;
}}
.gallery__item:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(26,22,20,0.06);
}}
.gallery__item--wide {{ grid-column: span 2; }}
.gallery__item img {{ width: 100%; }}
.gallery__caption {{
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--ink-muted);
    padding: var(--s3) var(--s4);
    letter-spacing: 0.02em;
}}

/* ═══════════════════════════════════════════
   ADDITIONAL FINDINGS
   ═══════════════════════════════════════════ */
.findings-list {{
    display: flex;
    flex-direction: column;
    gap: var(--s6);
}}
.finding {{
    background: white;
    border: 1px solid var(--rule-light);
    border-radius: 12px;
    padding: var(--s6);
    transition: transform 0.2s, box-shadow 0.2s;
}}
.finding:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(26,22,20,0.05);
}}
.finding__header {{
    display: flex;
    align-items: center;
    gap: var(--s3);
    margin-bottom: var(--s3);
}}
.finding__badge {{
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: var(--s1) var(--s3);
    border-radius: 4px;
    background: var(--badge-color, var(--accent));
    color: white;
}}
.finding__score {{
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--ink-muted);
}}
.finding__method {{
    font-family: var(--serif);
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: var(--s3);
}}
.finding__text {{
    font-size: 0.95rem;
    color: var(--ink-secondary);
    line-height: 1.7;
    margin-bottom: var(--s4);
}}
.finding__insight {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--s5);
    padding-top: var(--s4);
    border-top: 1px solid var(--rule-light);
}}
.finding__label {{
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    display: block;
    margin-bottom: var(--s2);
}}
.finding__sowhat p,
.finding__inter p {{
    font-size: 0.85rem;
    color: var(--ink-secondary);
    line-height: 1.6;
}}
.finding__fig {{
    margin-top: var(--s5);
    border-radius: 8px;
    border: 1px solid var(--rule-light);
}}

/* ═══════════════════════════════════════════
   DEEP DIVE — DARK SECTION
   ═══════════════════════════════════════════ */
.deep {{
    background: var(--ink);
    color: var(--paper);
}}
.deep .section__label {{
    color: var(--accent-light);
}}
.deep .section__label::before {{ background: var(--accent-light); }}
.deep .section__title {{ color: var(--paper); }}
.deep .section__desc {{ color: rgba(253,251,249,0.6); }}

.domains {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: var(--s5);
}}
.domain {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: var(--s6);
    transition: background 0.25s;
}}
.domain:hover {{
    background: rgba(255,255,255,0.07);
}}
.domain__icon {{
    width: 32px;
    height: 32px;
    color: var(--accent-light);
    margin-bottom: var(--s4);
}}
.domain__icon svg {{ width: 100%; height: 100%; }}
.domain__title {{
    font-family: var(--serif);
    font-size: 1.15rem;
    font-weight: 500;
    margin-bottom: var(--s3);
    color: var(--accent-light);
}}
.domain__text {{
    font-size: 0.9rem;
    color: rgba(253,251,249,0.7);
    line-height: 1.7;
}}

/* ═══════════════════════════════════════════
   TRANSPARENCY TABLE
   ═══════════════════════════════════════════ */
.transparency {{
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid var(--rule-light);
    background: white;
}}
.transparency table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}}
.transparency th {{
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: left;
    padding: var(--s4);
    background: var(--paper-warm);
    color: var(--ink-muted);
    border-bottom: 2px solid var(--rule);
}}
.transparency td {{
    padding: var(--s3) var(--s4);
    border-bottom: 1px solid var(--rule-light);
    vertical-align: middle;
}}
.transparency__discard {{ opacity: 0.45; }}
.transparency__discard:hover {{ opacity: 0.7; }}
.transparency tr:hover {{ background: rgba(180,77,45,0.02); }}
.transparency__method {{ font-weight: 500; }}
.transparency__score {{ font-family: var(--mono); font-size: 0.8rem; }}
.transparency__cat {{
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.05em;
}}
.transparency__decision {{
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 500;
    padding: var(--s1) var(--s2);
    border-radius: 4px;
    display: inline-block;
}}
.transparency__decision--keep {{ background: var(--teal-pale); color: var(--teal); }}
.transparency__decision--discard {{ background: #FEE2E2; color: #991B1B; }}

/* ═══════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════ */
footer {{
    padding: var(--s8) var(--s6);
    text-align: center;
    border-top: 1px solid var(--rule);
}}
.footer__credit {{
    font-family: var(--serif);
    font-size: 1.2rem;
    font-weight: 500;
    color: var(--ink);
    margin-bottom: var(--s3);
}}
.footer__detail {{
    font-size: 0.85rem;
    color: var(--ink-muted);
    line-height: 1.8;
}}
.footer__line {{
    width: 48px;
    height: 1px;
    background: var(--accent);
    margin: var(--s5) auto;
}}

/* ═══════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════ */
@media (max-width: 1024px) {{
    .hero__inner {{ grid-template-columns: 1fr; }}
    .hero__figure {{ display: none; }}
    .method-grid {{ grid-template-columns: 1fr; }}
}}
@media (max-width: 768px) {{
    .hero {{ padding: var(--s9) var(--s5) var(--s8); }}
    .section {{ padding: var(--s8) var(--s5); }}
    .hero__stats {{ flex-wrap: wrap; gap: var(--s5); }}
    .takeaway {{ grid-template-columns: 1fr; gap: var(--s5); }}
    .takeaway--reverse {{ direction: ltr; }}
    .sowhat-grid {{ grid-template-columns: 1fr; }}
    .gallery {{ grid-template-columns: 1fr; }}
    .gallery__item--wide {{ grid-column: span 1; }}
    .finding__insight {{ grid-template-columns: 1fr; }}
    .nav__links {{ display: none; }}
    .domains {{ grid-template-columns: 1fr; }}
}}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {{
    [data-reveal] {{
        opacity: 1;
        transform: none;
        transition: none;
    }}
    * {{ transition-duration: 0.01ms !important; }}
}}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav" id="nav">
    <a class="nav__brand" href="#">ADV 382 Research</a>
    <ul class="nav__links">
        <li><a href="#method">Method</a></li>
        <li><a href="#findings">Findings</a></li>
        <li><a href="#sowhat">So What</a></li>
        <li><a href="#evidence">Evidence</a></li>
        <li><a href="#deep-dive">Deep Dive</a></li>
        <li><a href="#transparency">Transparency</a></li>
    </ul>
</nav>

<!-- HERO -->
<header class="hero">
    <div class="hero__inner">
        <div class="hero__text">
            <p class="hero__eyebrow">ADV 382 &middot; Experimental Research &middot; 2026</p>
            <h1>Do consumers <strong>trust</strong> a virtual influencer the same way they trust a human one?</h1>
            <p class="hero__subtitle">
                We ran an experiment with 83 participants, conducted {len(results)} automated analyses,
                and found a clear answer: <em>no</em> &#8212; and the implications reach far beyond marketing.
            </p>
            <div class="hero__stats">
                <div class="hero__stat">
                    <div class="hero__stat-num">83</div>
                    <div class="hero__stat-label">Participants</div>
                </div>
                <div class="hero__stat">
                    <div class="hero__stat-num">{len(results)}</div>
                    <div class="hero__stat-label">Analyses</div>
                </div>
                <div class="hero__stat">
                    <div class="hero__stat-num">{len(kept)}</div>
                    <div class="hero__stat-label">Key findings</div>
                </div>
                <div class="hero__stat">
                    <div class="hero__stat-num">d=0.55</div>
                    <div class="hero__stat-label">Trust gap</div>
                </div>
            </div>
            <a href="../ghost-deck/index.html" target="_blank" style="
                display:inline-flex; align-items:center; gap:12px;
                margin-top:var(--s6); padding:14px 24px;
                background:var(--accent); color:white;
                font-family:var(--sans); font-size:0.9rem; font-weight:500;
                border-radius:6px; text-decoration:none;
                transition:transform 0.2s, box-shadow 0.2s;
            " onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 8px 24px rgba(180,77,45,0.25)'" onmouseout="this.style.transform='';this.style.boxShadow=''">
                Strategy Deck &mdash; 9-slide executive summary
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
        </div>
        <div class="hero__figure">
            {'<img src="' + fig_data.get("forest_plot","") + '" alt="Effect Size Forest Plot">' if fig_data.get("forest_plot") else ''}
        </div>
    </div>
</header>

<!-- METHOD -->
<section class="section" id="method">
    <div class="section__inner">
        <p class="section__label">01 &mdash; Method</p>
        <h2 class="section__title">How we tested it</h2>
        <p class="section__desc">
            A between-subjects experiment where participants viewed advertising from either
            a virtual or human influencer, then rated their trust, purchase intention, and attitude.
        </p>
        <div class="method-grid">
            <div class="method-card" data-reveal>
                <h4>Sample</h4>
                <p>N = 83 participants randomly assigned to conditions. Virtual: 41, Human: 42. Predominantly female (76%), aged 18&#8211;28 (65%), daily social media users (93%).</p>
            </div>
            <div class="method-card" data-reveal>
                <h4>Constructs</h4>
                <p><strong>Trust</strong> (8 items, &#945;=.89) &#8212; authenticity, reliability, integrity.
                   <strong>Purchase Intention</strong> (4 items, &#945;=.90).
                   <strong>Attitude</strong> (4 items, &#945;=.94) &#8212; 7-point bipolar scales.</p>
            </div>
            <div class="method-card" data-reveal>
                <h4>Automated Analysis</h4>
                <p>{len(results)} statistical methods scored on rigor, effect magnitude, novelty, storytelling, and actionability. {len(kept)} passed the quality threshold (&ge;50/100). All results reported transparently.</p>
            </div>
        </div>
    </div>
</section>

<!-- KEY FINDINGS — THE STORY -->
<section class="section" id="findings" style="background: var(--paper-warm);">
    <div class="section__inner">
        <p class="section__label">02 &mdash; Key Findings</p>
        <h2 class="section__title">Three things you need to know</h2>
        <p class="section__desc">
            Not just what we found, but what it means &#8212; for brands, for consumers, and for the future of AI-driven marketing.
        </p>
        {takeaway_html}
    </div>
</section>

<!-- SO WHAT — STAKEHOLDER IMPLICATIONS -->
<section class="section" id="sowhat">
    <div class="section__inner">
        <p class="section__label">03 &mdash; So What?</p>
        <h2 class="section__title">Who should care about this, and why</h2>
        <p class="section__desc">
            Research doesn't matter if it stays in a paper. Here's what each stakeholder should do with these findings.
        </p>
        <div class="sowhat-grid">
            {sowhat_cards}
        </div>
    </div>
</section>

<!-- EVIDENCE GALLERY -->
<section class="section" id="evidence" style="background: var(--paper-warm);">
    <div class="section__inner">
        <p class="section__label">04 &mdash; Visual Evidence</p>
        <h2 class="section__title">The data, visualized</h2>
        <p class="section__desc">
            Every chart tells part of the story. From group comparisons to mediation paths and consumer segments.
        </p>
        <div class="gallery">
            {gallery_html}
        </div>
    </div>
</section>

<!-- ADDITIONAL FINDINGS -->
<section class="section">
    <div class="section__inner">
        <p class="section__label">05 &mdash; Complete Findings</p>
        <h2 class="section__title">Every analysis that made the cut</h2>
        <p class="section__desc">
            {len(kept)} analyses passed our quality threshold. Each includes statistical evidence, practical implications, and cross-disciplinary connections.
        </p>
        <div class="findings-list">
            {additional_html}
        </div>
    </div>
</section>

<!-- DEEP DIVE -->
<section class="section deep" id="deep-dive">
    <div class="section__inner">
        <p class="section__label">06 &mdash; Deep Dive</p>
        <h2 class="section__title">Interdisciplinary implications</h2>
        <p class="section__desc">
            This experiment speaks to five fields beyond advertising. Here's what each discipline can take from our findings.
        </p>
        <div class="domains">
            {domains_html}
        </div>
    </div>
</section>

<!-- TRANSPARENCY -->
<section class="section" id="transparency">
    <div class="section__inner">
        <p class="section__label">07 &mdash; Full Transparency</p>
        <h2 class="section__title">Every analysis we tried</h2>
        <p class="section__desc">
            All {len(results)} analyses &#8212; kept and discarded. Non-significant results are not failures; they are findings. Faded rows were scored below the quality threshold.
        </p>
        <div class="transparency">
            <table>
                <thead>
                    <tr>
                        <th>Method</th>
                        <th>Variable</th>
                        <th>Category</th>
                        <th>Score</th>
                        <th>Decision</th>
                    </tr>
                </thead>
                <tbody>
                    {transparency_rows}
                </tbody>
            </table>
        </div>
    </div>
</section>

<!-- FOOTER -->
<footer>
    <div class="footer__line"></div>
    <p class="footer__credit">Bella Kang</p>
    <p class="footer__detail">
        ADV 382: Data Divas &middot; Virtual vs. Human Influencer Experiment<br>
        {len(results)} automated analyses &middot; {len(kept)} findings kept &middot; {len(fig_data)} visualizations<br>
        Powered by iterative computational analysis &middot; Generated {datetime.now().strftime('%B %d, %Y')}
    </p>
</footer>

<!-- SCRIPTS -->
<script>
// Scroll reveal
const reveals = document.querySelectorAll('[data-reveal]');
const observer = new IntersectionObserver((entries) => {{
    entries.forEach((entry, i) => {{
        if (entry.isIntersecting) {{
            setTimeout(() => entry.target.classList.add('visible'), i * 60);
            observer.unobserve(entry.target);
        }}
    }});
}}, {{ threshold: 0.1, rootMargin: '0px 0px -40px 0px' }});
reveals.forEach(el => observer.observe(el));

// Nav scroll effect
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {{
    nav.classList.toggle('scrolled', window.scrollY > 40);
}});
</script>

</body>
</html>"""

    output_path = os.path.join(PORTFOLIO_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n=== Portfolio generated ===")
    print(f"  Path: {output_path}")
    print(f"  Results: {len(kept)} KEEP / {len(discarded)} DISCARD")
    print(f"  Figures embedded: {len(fig_data)}")
    return output_path


if __name__ == "__main__":
    generate_portfolio()

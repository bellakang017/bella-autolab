"""
Analysis quality scoring for the autoresearch loop.
THIS FILE IS FIXED — DO NOT MODIFY.

5 criteria, each 0-20 points (total 0-100).
Decision: score >= 50 → KEEP, else → DISCARD.
"""

import os
import csv
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
RESULTS_TSV = os.path.join(OUTPUT_DIR, "results.tsv")

KEEP_THRESHOLD = 50


def score_statistical_rigor(p_value):
    """Score based on p-value significance level. 0-20 points."""
    if p_value is None:
        return 2
    try:
        p = float(p_value)
    except (ValueError, TypeError):
        return 2
    if p < 0.001:
        return 20
    elif p < 0.01:
        return 16
    elif p < 0.05:
        return 12
    elif p < 0.10:
        return 6
    else:
        return 2


def score_effect_magnitude(effect_size):
    """Score based on effect size magnitude. 0-20 points.
    Uses Cohen's conventions: small=0.2, medium=0.5, large=0.8 (for d)
    or small=0.01, medium=0.06, large=0.14 (for eta-squared).
    """
    if effect_size is None:
        return 2
    try:
        es = abs(float(effect_size))
    except (ValueError, TypeError):
        return 2
    # Heuristic: if < 1, treat as eta-squared scale; if >= 1, treat as d-scale
    if es < 1:
        # eta-squared / r-squared / partial eta-squared scale
        if es >= 0.14:
            return 20
        elif es >= 0.06:
            return 14
        elif es >= 0.01:
            return 8
        else:
            return 2
    else:
        # Cohen's d scale
        if es >= 0.8:
            return 20
        elif es >= 0.5:
            return 14
        elif es >= 0.2:
            return 8
        else:
            return 2


def _load_past_results():
    """Load past results from results.tsv."""
    if not os.path.exists(RESULTS_TSV):
        return []
    results = []
    with open(RESULTS_TSV, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            results.append(row)
    return results


def score_novelty(category, variable, method):
    """Score based on novelty relative to past results. 0-20 points.
    - New category: 15
    - Same category, different variable/method: 5
    - Duplicate: 0
    """
    past = _load_past_results()
    if not past:
        return 15  # first analysis is always novel

    past_categories = set()
    past_combos = set()
    for r in past:
        cat = r.get("category", "")
        var = r.get("variable", "")
        meth = r.get("method", "")
        past_categories.add(cat)
        past_combos.add((cat, var, meth))

    if (category, variable, method) in past_combos:
        return 0  # exact duplicate

    if category not in past_categories:
        return 15  # new category

    return 5  # same category, different variable/method


def score_storytelling(result):
    """Score based on storytelling potential. 0-20 points.
    - so_what present and substantive: +5
    - interdisciplinary present and substantive: +5
    - clear directionality (higher/lower, positive/negative): +5
    - surprising or counterintuitive finding: +5
    """
    score = 0

    so_what = result.get("so_what", "")
    if so_what and len(str(so_what)) > 20:
        score += 5

    interdisciplinary = result.get("interdisciplinary", "")
    if interdisciplinary and len(str(interdisciplinary)) > 20:
        score += 5

    finding = str(result.get("finding", ""))
    direction_words = ["higher", "lower", "greater", "less", "more", "positive",
                       "negative", "increase", "decrease", "stronger", "weaker"]
    if any(w in finding.lower() for w in direction_words):
        score += 5

    surprise_words = ["however", "surprisingly", "contrary", "unexpected",
                      "despite", "no significant", "no difference", "failed to"]
    if any(w in finding.lower() for w in surprise_words):
        score += 5

    return score


def score_actionability(result):
    """Score based on actionability. 0-20 points.
    - Specific stakeholder mentioned: +7
    - Specific action recommended: +7
    - Competitive interpretation: +6
    """
    score = 0
    so_what = str(result.get("so_what", "")).lower()
    interdisciplinary = str(result.get("interdisciplinary", "")).lower()
    combined = so_what + " " + interdisciplinary

    stakeholders = ["marketer", "brand", "advertiser", "consumer", "regulator",
                    "policymaker", "researcher", "platform", "agency", "influencer",
                    "company", "manager", "designer", "developer"]
    if any(s in combined for s in stakeholders):
        score += 7

    actions = ["should", "recommend", "consider", "implement", "develop",
               "invest", "prioritize", "disclose", "require", "adopt",
               "leverage", "optimize", "design"]
    if any(a in combined for a in actions):
        score += 7

    compete_words = ["vs", "versus", "compared to", "advantage", "competitive",
                     "outperform", "alternative", "traditional", "emerging"]
    if any(c in combined for c in compete_words):
        score += 6

    return score


def evaluate(result):
    """Score an analysis result. Returns (total_score, breakdown, decision)."""
    category = result.get("category", "unknown")
    variable = result.get("variable", "unknown")
    method = result.get("method", "unknown")
    p_value = result.get("p_value")
    effect_size = result.get("effect_size")

    breakdown = {
        "statistical_rigor": score_statistical_rigor(p_value),
        "effect_magnitude": score_effect_magnitude(effect_size),
        "novelty": score_novelty(category, variable, method),
        "storytelling": score_storytelling(result),
        "actionability": score_actionability(result),
    }

    total = sum(breakdown.values())
    decision = "KEEP" if total >= KEEP_THRESHOLD else "DISCARD"

    return total, breakdown, decision


def log_result(result, score, breakdown, decision):
    """Append result to results.tsv."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_exists = os.path.exists(RESULTS_TSV) and os.path.getsize(RESULTS_TSV) > 0

    fieldnames = [
        "timestamp", "method", "category", "variable", "statistic", "p_value",
        "effect_size", "finding", "so_what", "interdisciplinary",
        "score_total", "score_rigor", "score_effect", "score_novelty",
        "score_story", "score_action", "decision"
    ]

    with open(RESULTS_TSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "method": result.get("method", ""),
            "category": result.get("category", ""),
            "variable": result.get("variable", ""),
            "statistic": result.get("statistic", ""),
            "p_value": result.get("p_value", ""),
            "effect_size": result.get("effect_size", ""),
            "finding": result.get("finding", ""),
            "so_what": result.get("so_what", ""),
            "interdisciplinary": result.get("interdisciplinary", ""),
            "score_total": score,
            "score_rigor": breakdown["statistical_rigor"],
            "score_effect": breakdown["effect_magnitude"],
            "score_novelty": breakdown["novelty"],
            "score_story": breakdown["storytelling"],
            "score_action": breakdown["actionability"],
            "decision": decision,
        })


def evaluate_and_log(result):
    """Evaluate a result, log it, and return (score, decision)."""
    score, breakdown, decision = evaluate(result)
    log_result(result, score, breakdown, decision)
    print(f"  [{decision}] score={score} "
          f"(rigor={breakdown['statistical_rigor']}, effect={breakdown['effect_magnitude']}, "
          f"novelty={breakdown['novelty']}, story={breakdown['storytelling']}, "
          f"action={breakdown['actionability']})")
    return score, decision


# --- Test mode ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        print("=== Evaluate.py Self-Test ===\n")

        # Test 1: highly significant result
        r1 = {
            "method": "independent_ttest", "category": "basic",
            "variable": "trust", "statistic": "t(81)=3.45",
            "p_value": 0.001, "effect_size": 0.76,
            "finding": "Virtual influencers showed significantly lower trust than human influencers.",
            "so_what": "Brands should consider trust deficits when partnering with virtual influencers.",
            "interdisciplinary": "HCI researchers should investigate the uncanny valley effect in marketing contexts.",
        }
        s1, b1, d1 = evaluate(r1)
        print(f"Test 1 (significant): score={s1}, decision={d1}, breakdown={b1}")
        assert d1 == "KEEP", f"Expected KEEP, got {d1}"

        # Test 2: non-significant result
        r2 = {
            "method": "independent_ttest", "category": "basic",
            "variable": "pi", "statistic": "t(81)=0.42",
            "p_value": 0.68, "effect_size": 0.09,
            "finding": "No significant difference in purchase intention.",
            "so_what": "", "interdisciplinary": "",
        }
        s2, b2, d2 = evaluate(r2)
        print(f"Test 2 (non-sig): score={s2}, decision={d2}, breakdown={b2}")

        # Test 3: novel category
        r3 = {
            "method": "bayesian_ttest", "category": "creative",
            "variable": "trust", "statistic": "BF10=5.2",
            "p_value": None, "effect_size": 0.6,
            "finding": "Bayesian analysis provides strong evidence for trust differences.",
            "so_what": "Marketers should invest in transparency mechanisms for virtual influencer campaigns.",
            "interdisciplinary": "Public health communicators should consider alternative trust-building strategies vs traditional human endorsers.",
        }
        s3, b3, d3 = evaluate(r3)
        print(f"Test 3 (novel+story): score={s3}, decision={d3}, breakdown={b3}")

        print("\n=== All tests passed ===")

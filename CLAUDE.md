# bella-autolab — ADV382 AutoResearch Agent

## Project Purpose
Automated research analysis agent for ADV382 Virtual vs. Human Influencer experiment (N≈83).
Follows Karpathy's autoresearch pattern: iterate analyses, evaluate, keep/discard, visualize, generate portfolio.

## File Modification Rules

| File | Editable? | Notes |
|------|-----------|-------|
| `src/prepare.py` | NO | Data pipeline is fixed. Do not modify. |
| `src/evaluate.py` | NO | Scoring functions are fixed. Do not modify. |
| `src/analyze.py` | YES | Add new `@register_analysis` functions here. |
| `src/visualize.py` | YES | Add new visualization functions here. |
| `src/portfolio.py` | NO | HTML generator scaffold is fixed. |
| `data/raw.csv` | NO | Original Qualtrics export. Never modify. |
| `output/results.tsv` | APPEND-ONLY | Analysis log. Only append new rows. |

## Data Rules
- Never fabricate or modify raw data
- Report non-significant results honestly
- Always include effect sizes and confidence intervals
- Small N (≈83): acknowledge power limitations

## Analysis Loop Protocol
1. Add analysis function to `analyze.py`
2. Run analysis → get result dict
3. Score with `evaluate.py` → KEEP (≥50) or DISCARD
4. Log to `output/results.tsv`
5. If KEEP: generate visualizations in `visualize.py`
6. Repeat

## Key Columns (0-indexed)
- Demographics: 17(gender), 18(age), 19(occupation), 21(education), 22(social media)
- Group: 27 (Q17) — "Yes"=Virtual, empty=Human
- Trust: 41-48 (8 items, 5-point agreement)
- PI: 36,38,39,40 (4 items, 5-point agreement)
- Attitude: 49-52 (4 items, 7-point bipolar)
- Familiarity: 53 (5-point)

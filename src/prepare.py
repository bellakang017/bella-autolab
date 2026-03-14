"""
Data preparation pipeline for ADV382 Virtual vs. Human Influencer experiment.
THIS FILE IS FIXED — DO NOT MODIFY.
"""

import os
import pickle
import csv
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RAW_CSV = os.path.join(DATA_DIR, "raw.csv")
CLEAN_PKL = os.path.join(DATA_DIR, "clean.pkl")

# --- Column indices (0-based) in the raw CSV ---
COL_PROGRESS = 4
COL_GENDER = 17
COL_AGE = 18
COL_OCCUPATION = 19
COL_EDUCATION = 21
COL_SOCIAL_MEDIA = 22
COL_GROUP = 27          # Q17: "Yes" = Virtual, empty = Human
COL_PRODUCT = 32

# Trust items (8): cols 41-48 (5-point agreement)
TRUST_COLS = list(range(41, 49))
# Purchase Intention items (4): cols 36, 38, 39, 40 (5-point agreement)
PI_COLS = [36, 38, 39, 40]
# Attitude items (4): cols 49-52 (7-point bipolar)
ATTITUDE_COLS = list(range(49, 53))
# Familiarity: col 53 (5-point)
FAMILIARITY_COL = 53
# Follow VI: col 54
FOLLOW_COL = 54

# --- Encoding maps ---
AGREEMENT_MAP = {
    "strongly disagree": 1,
    "somewhat disagree": 2,
    "neither agree nor disagree": 3,
    "somewhat agree": 4,
    "strongly agree": 5,
}

ATTITUDE_MAP = {
    # Bad-Good
    "bad": 1, "somewhat bad": 2, "neutral": 4, "somewhat good": 6, "good": 7,
    # Dislike-Like
    "dislike": 1, "somewhat dislike": 2, "somewhat like": 6, "like": 7,
    # Unfavourable-Favourable (handles all casing/spelling variants)
    "unfavourable": 1, "unfavorable": 1,
    "somewhat unfavorable": 2, "somewhat unfavourable": 2,
    "somewhat favorable": 6, "somewhat favourable": 6,
    "favourable": 7, "favorable": 7,
    # Negative-Positive
    "negative": 1, "somewhat negative": 2, "somewhat positive": 6, "positive": 7,
}

FAMILIARITY_MAP = {
    "not familiar at all": 1,
    "slightly familar": 2,    # typo in original data
    "slightly familiar": 2,
    "moderately familiar": 3,
    "very familiar": 4,
    "extremely familiar": 5,
}


def load_qualtrics():
    """Load raw Qualtrics CSV, handling 3-row header."""
    with open(RAW_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Row 0: short names (may have duplicates like Q36, Q19_1)
    # Row 1: full question text
    # Row 2: ImportId JSON
    # Row 3+: data
    short_names = rows[0]
    questions = rows[1]
    data_rows = rows[3:]  # skip import-id row

    # Resolve duplicate column names by appending suffix
    seen = {}
    unique_names = []
    for name in short_names:
        if name in seen:
            seen[name] += 1
            unique_names.append(f"{name}__dup{seen[name]}")
        else:
            seen[name] = 0
            unique_names.append(name)

    df = pd.DataFrame(data_rows, columns=unique_names)
    df.attrs["questions"] = dict(zip(unique_names, questions))
    return df


def filter_complete(df):
    """Remove incomplete responses. Keep rows with progress>=95 AND complete DV data."""
    # Convert progress to numeric
    df["Progress"] = pd.to_numeric(df["Progress"], errors="coerce")
    df = df[df["Progress"] >= 95].copy()

    # Core DV columns that must be non-empty
    core_col_indices = TRUST_COLS + PI_COLS + ATTITUDE_COLS
    core_col_names = [df.columns[i] for i in core_col_indices]

    # Drop rows with any empty core DV
    for col in core_col_names:
        df = df[df[col].str.strip() != ""]
        df = df[df[col].notna()]

    df = df.reset_index(drop=True)
    return df


def _encode_series(series, mapping):
    """Encode a text series using a case-insensitive mapping."""
    return series.str.strip().str.lower().map(mapping).astype(float)


def encode_likert(df):
    """Encode all Likert scale responses to numeric values."""
    # Trust items (agreement scale)
    for idx in TRUST_COLS:
        col = df.columns[idx]
        df[f"trust_{idx - TRUST_COLS[0] + 1}"] = _encode_series(df[col], AGREEMENT_MAP)

    # PI items (agreement scale)
    for i, idx in enumerate(PI_COLS):
        col = df.columns[idx]
        df[f"pi_{i + 1}"] = _encode_series(df[col], AGREEMENT_MAP)

    # Attitude items (bipolar scale)
    for i, idx in enumerate(ATTITUDE_COLS):
        col = df.columns[idx]
        df[f"attitude_{i + 1}"] = _encode_series(df[col], ATTITUDE_MAP)

    # Familiarity
    fam_col = df.columns[FAMILIARITY_COL]
    df["familiarity"] = _encode_series(df[fam_col], FAMILIARITY_MAP)

    return df


def cronbach_alpha(items_df):
    """Calculate Cronbach's alpha for a set of items."""
    items = items_df.dropna()
    n_items = items.shape[1]
    if n_items < 2:
        return np.nan
    item_vars = items.var(axis=0, ddof=1)
    total_var = items.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return np.nan
    alpha = (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)
    return alpha


def create_composites(df):
    """Create composite scores (means) and compute Cronbach's alpha."""
    trust_items = [f"trust_{i}" for i in range(1, 9)]
    pi_items = [f"pi_{i}" for i in range(1, 5)]
    attitude_items = [f"attitude_{i}" for i in range(1, 5)]

    df["trust"] = df[trust_items].mean(axis=1)
    df["pi"] = df[pi_items].mean(axis=1)
    df["attitude"] = df[attitude_items].mean(axis=1)

    # Compute and store alphas
    alphas = {
        "trust": cronbach_alpha(df[trust_items]),
        "pi": cronbach_alpha(df[pi_items]),
        "attitude": cronbach_alpha(df[attitude_items]),
    }
    df.attrs["cronbach_alphas"] = alphas

    return df


def assign_groups(df):
    """Assign experimental groups based on Q17 (virtual influencer confirmation)."""
    group_col = df.columns[COL_GROUP]
    df["group"] = df[group_col].apply(
        lambda x: "virtual" if str(x).strip().lower() == "yes" else "human"
    )
    return df


def extract_demographics(df):
    """Extract and clean demographic variables."""
    df["gender"] = df[df.columns[COL_GENDER]].str.strip()
    df["age"] = df[df.columns[COL_AGE]].str.strip()
    df["occupation"] = df[df.columns[COL_OCCUPATION]].str.strip()
    df["education"] = df[df.columns[COL_EDUCATION]].str.strip()
    df["social_media_freq"] = df[df.columns[COL_SOCIAL_MEDIA]].str.strip()
    df["product"] = df[df.columns[COL_PRODUCT]].str.strip()

    # Follow VI (col 54)
    follow_col = df.columns[FOLLOW_COL]
    df["follow_vi"] = df[follow_col].str.strip()

    return df


def get_clean_data(force=False):
    """Main pipeline: load, filter, encode, composite, group. Returns clean DataFrame."""
    if not force and os.path.exists(CLEAN_PKL):
        with open(CLEAN_PKL, "rb") as f:
            df = pickle.load(f)
        print(f"[prepare] Loaded cached clean data: N={len(df)}")
        return df

    print("[prepare] Loading raw Qualtrics CSV...")
    df = load_qualtrics()
    print(f"  Raw rows: {len(df)}")

    df = filter_complete(df)
    print(f"  After filtering: N={len(df)}")

    df = assign_groups(df)
    groups = df["group"].value_counts()
    print(f"  Groups: {groups.to_dict()}")

    df = encode_likert(df)
    df = create_composites(df)
    df = extract_demographics(df)

    alphas = df.attrs.get("cronbach_alphas", {})
    print(f"  Cronbach's alphas: { {k: f'{v:.3f}' for k, v in alphas.items()} }")

    # Check for encoding failures
    for var in ["trust", "pi", "attitude"]:
        n_missing = df[var].isna().sum()
        if n_missing > 0:
            print(f"  WARNING: {n_missing} missing values in {var}")

    # Cache
    with open(CLEAN_PKL, "wb") as f:
        pickle.dump(df, f)
    print(f"  Saved to {CLEAN_PKL}")

    return df


if __name__ == "__main__":
    df = get_clean_data(force=True)
    print(f"\n=== Summary ===")
    print(f"N = {len(df)}")
    print(f"Groups: {df['group'].value_counts().to_dict()}")
    print(f"\nComposite descriptives:")
    for var in ["trust", "pi", "attitude", "familiarity"]:
        if var in df.columns:
            print(f"  {var}: M={df[var].mean():.2f}, SD={df[var].std():.2f}, "
                  f"range=[{df[var].min():.1f}, {df[var].max():.1f}]")
    print(f"\nCronbach's alphas: {df.attrs.get('cronbach_alphas', {})}")
    print(f"\nDemographics:")
    for var in ["gender", "age", "education", "social_media_freq"]:
        print(f"  {var}: {df[var].value_counts().to_dict()}")

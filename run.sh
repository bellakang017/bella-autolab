#!/bin/bash
# ADV382 AutoResearch Pipeline — Full Run
set -e

cd "$(dirname "$0")"
source .venv/bin/activate

echo "=========================================="
echo "  ADV382 AutoResearch Pipeline"
echo "=========================================="
echo ""

# Step 1: Data preparation
echo "[1/4] Preparing data..."
python3 src/prepare.py
echo ""

# Step 2: Run all analyses
echo "[2/4] Running all analyses..."
python3 src/analyze.py --run-all
echo ""

# Step 3: Generate visualizations
echo "[3/4] Generating visualizations..."
python3 src/visualize.py
echo ""

# Step 4: Build portfolio
echo "[4/4] Building portfolio..."
python3 src/portfolio.py
echo ""

echo "=========================================="
echo "  Pipeline complete!"
echo "  Portfolio: output/portfolio/index.html"
echo "  Results:   output/results.tsv"
echo "  Figures:   output/figures/"
echo "=========================================="

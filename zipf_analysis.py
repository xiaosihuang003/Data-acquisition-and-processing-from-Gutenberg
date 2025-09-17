# zipf_analysis.py

"""
Compute and visualize Zipf's law on the unified vocabulary built from cleaned books.

"""

from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path
from collections import Counter
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Utility functions
# -----------------------------

def read_clean_tokens(clean_dir: Path) -> Counter:
    # Read all cleaned .txt files and accumulate token counts.
    # Cleaned files were written by clean_and_vocab.py (space-separated lemmas).
    counter = Counter()
    if not clean_dir.exists():
        raise FileNotFoundError(f"Clean directory not found: {clean_dir}")

    files = sorted([p for p in clean_dir.glob("*.txt") if p.is_file()])
    if not files:
        raise RuntimeError(f"No cleaned .txt files found in: {clean_dir}. "
                           f"Run clean_and_vocab.py first.")

    for fp in files:
        # NOTE: each file is a long space-separated string of tokens
        with fp.open("r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        # Split by whitespace and update global counter
        tokens = text.split()
        counter.update(tokens)

    return counter


def build_rank_frequency(counter: Counter) -> Tuple[np.ndarray, np.ndarray, list, np.ndarray]:
    # Convert counts to a sorted rank–frequency representation.
    # Returns: ranks, probs, words_sorted, counts_sorted
    items = counter.most_common()
    words_sorted = [w for (w, c) in items]
    counts_sorted = np.array([c for (w, c) in items], dtype=np.int64)
    total = counts_sorted.sum()

    # Avoid division by zero (should not happen if we have tokens)
    probs = counts_sorted.astype(np.float64) / float(total)
    ranks = np.arange(1, len(counts_sorted) + 1, dtype=np.int64)
    return ranks, probs, words_sorted, counts_sorted


def save_rank_table(out_csv: Path, ranks: np.ndarray, words: list, counts: np.ndarray, probs: np.ndarray) -> None:
    # Save "rank,word,count,prob" as CSV for inspection.
    df = pd.DataFrame({
        "rank": ranks,
        "word": words,
        "count": counts,
        "prob": probs
    })
    df.to_csv(out_csv, index=False)


def fit_zipf_exponent(ranks: np.ndarray, probs: np.ndarray, rmin: int, rmax: int) -> Tuple[float, float]:
    # Fit exponent 'a' on a restricted scaling window [rmin, rmax].
    # Model in log10 space: log p(r) = c - a * log r
    mask = (ranks >= rmin) & (ranks <= rmax)
    if mask.sum() < 5:
        raise ValueError(f"Too few points to fit in window [{rmin}, {rmax}]")

    x = np.log10(ranks[mask])
    y = np.log10(probs[mask])

    # Least-squares line y = b + m*x; here m = -a, b = log10(C)
    m, b = np.polyfit(x, y, 1)
    a_fit = -m
    C_fit = 10 ** b
    return a_fit, C_fit


def model_with_fixed_a(ranks: np.ndarray, probs: np.ndarray, rmin: int, rmax: int, a: float) -> np.ndarray:
    # For a fixed 'a', estimate C by least squares in log-space on the same scaling window.
    mask = (ranks >= rmin) & (ranks <= rmax)
    x = np.log10(ranks[mask])
    y = np.log10(probs[mask])

    # For fixed slope -a, the best intercept b is mean(y + a*x)
    b = np.mean(y + a * x)
    C = 10 ** b
    return C * (ranks.astype(np.float64) ** (-a))


# -----------------------------
# Plotting
# -----------------------------

def plot_empirical_rank_freq(out_png: Path, ranks: np.ndarray, probs: np.ndarray) -> None:
    # Basic log–log rank–frequency plot.
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.loglog(ranks, probs, label="Empirical")
    ax.set_xlabel("Rank (r)")
    ax.set_ylabel("Frequency p(r)")
    ax.set_title("Zipf: Empirical rank–frequency (Top-20 books)")
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.close(fig)


def plot_overlay(out_png: Path,
                 ranks: np.ndarray,
                 probs: np.ndarray,
                 a_candidates=(0.8, 1.0, 1.2),
                 fit_window: Tuple[int, int] = (10, 3000)) -> float:
    # Overlay empirical curve with several Zipf models and a fitted slope.
    rmin, rmax = fit_window

    # Fit 'a' only on the scaling regime to avoid tail bias
    a_fit, C_fit = fit_zipf_exponent(ranks, probs, rmin, rmax)
    p_fit = C_fit * (ranks.astype(np.float64) ** (-a_fit))

    # Prepare candidate curves with log-space LS intercept
    models = []
    for a in a_candidates:
        p = model_with_fixed_a(ranks, probs, rmin, rmax, a)
        models.append((a, p))

    # Plot
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.loglog(ranks, probs, label="Empirical")
    for a, p in models:
        ax.loglog(ranks, p, linestyle="--", label=f"Zipf a={a:.2f}")
    ax.loglog(ranks, p_fit, linewidth=2.0, label=f"Fitted a={a_fit:.3f}")

    ax.set_xlabel("Rank (r)")
    ax.set_ylabel("Frequency p(r)")
    ax.set_title("Zipf: empirical vs. Zipf-law models")
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.close(fig)

    return a_fit


# -----------------------------
# Main
# -----------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Zipf's law analysis for the unified vocabulary (Top-20 Gutenberg books)."
    )
    parser.add_argument("--clean-dir", type=str, default="data/clean",
                        help="Directory of cleaned texts (space-separated tokens).")
    parser.add_argument("--out-dir", type=str, default="outputs",
                        help="Directory to write CSV and figures.")
    parser.add_argument("--rmin", type=int, default=10,
                        help="Lower rank bound for fitting (inclusive).")
    parser.add_argument("--rmax", type=int, default=3000,
                        help="Upper rank bound for fitting (inclusive).")
    args = parser.parse_args()

    clean_dir = Path(args.clean_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Read cleaned tokens & aggregate counts
    print("[INFO] Reading cleaned tokens ...")
    counter = read_clean_tokens(clean_dir)

    # 2) Build rank-frequency & save table
    print("[INFO] Building rank–frequency table ...")
    ranks, probs, words, counts = build_rank_frequency(counter)
    out_csv = out_dir / "zipf_freqs.csv"
    save_rank_table(out_csv, ranks, words, counts, probs)
    print(f"[INFO] Saved rank table -> {out_csv}")

    # 3) Plot empirical curve
    rank_freq_png = out_dir / "zipf_rank_freq.png"
    plot_empirical_rank_freq(rank_freq_png, ranks, probs)
    print(f"[INFO] Saved empirical figure -> {rank_freq_png}")

    # 4) Plot overlay with models and fitted slope
    overlay_png = out_dir / "zipf_overlay.png"
    a_fit = plot_overlay(overlay_png, ranks, probs,
                         a_candidates=(0.8, 1.0, 1.2),
                         fit_window=(args.rmin, args.rmax))
    print(f"[INFO] Saved overlay -> {overlay_png}")
    print(f"[INFO] Fitted exponent a (window {args.rmin}-{args.rmax}): a = {a_fit:.4f}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

# zipf_analysis.py

"""
Zipf analysis on the unified vocabulary built from the 20 cleaned books.
This script:
  - reads tokens from data/clean/*.txt (space-separated, lemmatized),
  - computes empirical frequencies p(r) sorted by rank,
  - overlays Zipf-law curves p(r) ~ C * r^{-a} for several exponents,
  - fits the best exponent via log-log linear regression,
  - writes CSV and saves plots under outputs/.
"""

# ===== Standard imports =====
import os
import math
from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ===== Paths =====
PROJECT_ROOT = Path(__file__).resolve().parent
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
OUT_DIR = PROJECT_ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ===== Utilities =====
def load_clean_tokens(clean_dir: Path) -> Counter:
    """
    Load all cleaned text files and count tokens.

    Notes (green comments):
    - Files in data/clean were produced by your pipeline; each file contains
      tokens separated by single spaces and already lemmatized.
    """
    if not clean_dir.exists():
        raise FileNotFoundError(f"Clean directory not found: {clean_dir}")

    counter = Counter()
    total_files = 0

    for fp in sorted(clean_dir.glob("*.txt")):
        total_files += 1
        with fp.open("r", encoding="utf-8", errors="ignore") as f:
            # Read whole file and split on whitespace; tokens are normalized already
            tokens = f.read().split()
            counter.update(tokens)

    if total_files == 0:
        raise RuntimeError(
            f"No files in {clean_dir}. Run `python clean_and_vocab.py` first."
        )
    return counter


def empirical_rank_freq(counter: Counter):
    """
    Turn a token counter into rank–frequency arrays.

    Returns:
      words_sorted: list of tokens in descending count order
      counts_sorted: np.array of counts in the same order
      probs_sorted:  np.array of normalized frequencies in the same order
    """
    items = counter.most_common()  # already sorted by count desc
    words_sorted = [w for w, c in items]
    counts_sorted = np.array([c for w, c in items], dtype=np.int64)
    total = counts_sorted.sum()
    probs_sorted = counts_sorted / total
    return words_sorted, counts_sorted, probs_sorted


def zipf_probs(V: int, a: float) -> np.ndarray:
    """
    Build a normalized Zipf probability vector of length V for exponent `a`.

    Math (green comments):
    - p(r) = C * r^{-a}, r=1..V, where C = 1 / sum_{r=1}^V r^{-a}
    - We use the generalized harmonic number for normalization.
    """
    ranks = np.arange(1, V + 1, dtype=np.float64)
    denom = np.sum(ranks ** (-a))
    C = 1.0 / denom
    return C * (ranks ** (-a))


def fit_zipf_exponent(probs: np.ndarray, rmin: int = 1, rmax: int | None = None) -> tuple[float, float]:
    """
    Fit exponent a from empirical probabilities by linear regression on log–log:
      log p = log C - a * log r  -> slope = -a

    Args:
      probs: empirical probability array sorted by rank
      rmin:  starting rank to include (>=1)
      rmax:  ending rank to include (<= len(probs)); None = full length

    Returns:
      (a_hat, C_hat)
    """
    V = len(probs)
    if rmax is None:
        rmax = V
    r = np.arange(1, V + 1, dtype=np.float64)
    mask = (r >= rmin) & (r <= rmax) & (probs > 0)
    x = np.log(r[mask])
    y = np.log(probs[mask])

    # Linear fit y = b0 + b1 * x;  b1 ≈ slope = -a
    b1, b0 = np.polyfit(x, y, 1)
    a_hat = -float(b1)
    C_hat = float(np.exp(b0))
    return a_hat, C_hat


def save_freq_table(words, counts, probs, out_csv: Path, top_k: int | None = None):
    """
    Save rank–frequency table to CSV for inspection.
    """
    V = len(words)
    if top_k is None:
        top_k = V
    df = pd.DataFrame({
        "rank": np.arange(1, top_k + 1),
        "word": words[:top_k],
        "count": counts[:top_k],
        "prob": probs[:top_k],
    })
    df.to_csv(out_csv, index=False)


def plot_rank_freq(probs: np.ndarray, out_png: Path, title: str):
    """
    Plot empirical rank–frequency on log–log axes.
    """
    ranks = np.arange(1, len(probs) + 1, dtype=np.float64)

    plt.figure(figsize=(8, 5))
    # Use a light line to keep file size small; scatter on huge V can be heavy.
    plt.loglog(ranks, probs, label="Empirical", linewidth=1.25)
    plt.xlabel("Rank (r)")
    plt.ylabel("Frequency p(r)")
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()


def plot_overlay(probs: np.ndarray, exponents: list[float], a_hat: float,
                 out_png: Path, title: str):
    """
    Overlay empirical curve with several Zipf-law curves (including the fitted a_hat).
    """
    V = len(probs)
    ranks = np.arange(1, V + 1, dtype=np.float64)

    plt.figure(figsize=(8, 5))
    plt.loglog(ranks, probs, label="Empirical", linewidth=1.5)

    # Plot user-specified exponents
    for a in exponents:
        plt.loglog(ranks, zipf_probs(V, a), linestyle="--", label=f"Zipf a={a:.2f}")

    # Plot fitted exponent
    plt.loglog(ranks, zipf_probs(V, a_hat), linewidth=2.0, label=f"Fitted a={a_hat:.3f}")

    plt.xlabel("Rank (r)")
    plt.ylabel("Frequency p(r)")
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()


# ===== Main =====
def main():
    print("[INFO] Loading cleaned tokens from:", CLEAN_DIR)
    counter = load_clean_tokens(CLEAN_DIR)
    words, counts, probs = empirical_rank_freq(counter)
    V = len(words)
    total_tokens = int(counts.sum())
    print(f"[INFO] Vocabulary size V = {V:,d}")
    print(f"[INFO] Total tokens     N = {total_tokens:,d}")
    print(f"[INFO] Sum of probs       = {probs.sum():.6f}")

    # Save top table (you can change top_k if you want fewer rows)
    out_csv = OUT_DIR / "zipf_freqs.csv"
    save_freq_table(words, counts, probs, out_csv, top_k=min(5000, V))
    print(f"[INFO] CSV written -> {out_csv}")

    # Fit exponent (you can tweak the fitting window if needed)
    a_hat, C_hat = fit_zipf_exponent(probs, rmin=1, rmax=None)
    print(f"[INFO] Fitted exponent a_hat = {a_hat:.4f}  (C_hat = {C_hat:.6e})")

    # Plot empirical curve
    plot_rank_freq(
        probs,
        OUT_DIR / "zipf_rank_freq.png",
        title="Zipf: Empirical rank–frequency (Top-20 books)"
    )

    # Overlay with several Zipf exponents + fitted one
    candidate_as = [0.8, 1.0, 1.2]  # <- try more if you like
    plot_overlay(
        probs,
        candidate_as,
        a_hat,
        OUT_DIR / "zipf_overlay.png",
        title="Zipf: empirical vs. Zipf-law models"
    )
    print(f"[INFO] Plots saved -> {OUT_DIR/'zipf_rank_freq.png'} and {OUT_DIR/'zipf_overlay.png'}")


if __name__ == "__main__":
    main()

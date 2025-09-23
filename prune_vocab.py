"""
Vocabulary pruning for Project Gutenberg (Exe 2.5)
"""
import os
import re
import math
import glob
import csv
from collections import Counter

# ---- Configs (can be overridden by env vars if you like) ----
CLEAN_DIR     = os.environ.get("CLEAN_DIR", "data/clean")
OUT_DIR       = os.environ.get("OUT_DIR", "outputs")
MIN_LEN       = int(os.environ.get("MIN_LEN", 3))   # overly short threshold
MAX_LEN       = int(os.environ.get("MAX_LEN", 20))  # overly long threshold
MIN_COUNT     = int(os.environ.get("MIN_COUNT", 4)) # drop words occurring < 4
TOP_PCT_DROP  = float(os.environ.get("TOP_PCT_DROP", 0.01))  # drop top 1%

# ---- Stopwords (NLTK) ----
try:
    from nltk.corpus import stopwords
    _stop = set(w.lower() for w in stopwords.words("english"))
except Exception:
    # Fallback: light list if NLTK data not downloaded yet
    _stop = {
        "the","and","to","of","a","in","that","is","it","was","i","for","on",
        "you","with","as","he","be","at","by","not","are","this","but","had",
        "his","they","from","she","or","which","we","an"
    }

TOKEN_RE = re.compile(r"[a-z]+")

def read_clean_tokens(clean_dir: str) -> Counter:
    counter = Counter()
    files = sorted(glob.glob(os.path.join(clean_dir, "*.txt")))
    if not files:
        raise FileNotFoundError(f"No cleaned files found under {clean_dir}/. "
                                "Run clean_and_vocab.py first.")
    for fp in files:
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().lower()
        # robust extraction (even if files are not whitespace-tokenized)
        toks = TOKEN_RE.findall(text)
        counter.update(toks)
    return counter

def prune(counter: Counter) -> Counter:
    before_total_types = len(counter)

    # (1) remove stopwords
    for sw in list(counter.keys()):
        if sw in _stop:
            del counter[sw]

    # (2) remove overly short/long words
    for w in list(counter.keys()):
        L = len(w)
        if L < MIN_LEN or L > MAX_LEN:
            del counter[w]

    # (3) remove the top 1% most frequent words (from the current vocab)
    V = len(counter)
    k = max(1, math.ceil(TOP_PCT_DROP * V))  # at least 1
    top_words = [w for w, c in counter.most_common(k)]
    for w in top_words:
        del counter[w]

    # (4) remove words occurring < MIN_COUNT
    for w, c in list(counter.items()):
        if c < MIN_COUNT:
            del counter[w]

    after_total_types = len(counter)
    print(f"[INFO] Types before: {before_total_types}  -> after pruning: {after_total_types} "
          f"(removed {before_total_types - after_total_types})")
    return counter

def export_all(counter: Counter, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    all_path = os.path.join(out_dir, "pruned_vocab_all.csv")
    with open(all_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["word", "count"])
        for word, cnt in counter.most_common():
            w.writerow([word, cnt])
    print(f"[INFO] Saved all pruned vocab -> {all_path}")
    return all_path

def export_top100(counter: Counter, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    top_path = os.path.join(out_dir, "pruned_top100.csv")
    with open(top_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "word", "count"])
        for i, (word, cnt) in enumerate(counter.most_common(100), start=1):
            w.writerow([i, word, cnt])
    print(f"[INFO] Saved pruned top-100 -> {top_path}")
    return top_path

def main():
    print("[INFO] Reading cleaned tokens ...")
    counts = read_clean_tokens(CLEAN_DIR)

    print("[INFO] Pruning vocabulary ...")
    pruned = prune(counts)

    export_all(pruned, OUT_DIR)
    export_top100(pruned, OUT_DIR)

    # brief console preview
    preview = list(pruned.most_common(10))
    print("[INFO] Preview (top 10 after pruning):")
    for i, (w, c) in enumerate(preview, 1):
        print(f"  {i:>2}. {w:>15s}  {c}")

if __name__ == "__main__":
    main()

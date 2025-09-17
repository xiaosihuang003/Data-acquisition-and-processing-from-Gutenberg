# clean_and_vocab.py
# Purpose: Clean raw Gutenberg texts (remove header/footer), tokenize and lemmatize,
# remove stopwords/punctuation/digits, then build a unified vocabulary across books
# and export the top-100 frequent words.

import os
import re
import csv
from collections import Counter
from typing import Tuple, List

import nltk

# --- Ensure NLTK data is available (idempotent and robust across versions) ---
def ensure_nltk_data():
    needed = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),  # <-- fix: ensure punkt_tab is available
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
        ("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger"),
    ]
    alt_tagger = ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng")

    for path, pkg in needed:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg)

    try:
        nltk.data.find(alt_tagger[0])
    except LookupError:
        try:
            nltk.download(alt_tagger[1])
        except Exception:
            pass

ensure_nltk_data()

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

RAW_DIR = "data/raw"
CLEAN_DIR = "data/clean"
OUTPUTS_DIR = "outputs"
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

TOP100_CSV = os.path.join(OUTPUTS_DIR, "top100_words.csv")
PERBOOK_STATS_CSV = os.path.join(OUTPUTS_DIR, "per_book_token_counts.csv")

def strip_gutenberg_header_footer(text: str) -> str:
    low = text.lower()
    start_phrase = "start of this project gutenberg ebook"
    end_phrase = "end of this project gutenberg ebook"

    start_idx = low.find(start_phrase)
    end_idx = low.find(end_phrase)

    if start_idx != -1:
        start_line_end = text.find("\n", start_idx)
        start = start_line_end + 1 if start_line_end != -1 else start_idx
    else:
        start = 0

    if end_idx != -1:
        end = end_idx
    else:
        end = len(text)

    cleaned = text[start:end].strip()
    return cleaned if cleaned else text

def nltk_pos_to_wordnet_pos(tag: str) -> str:
    if tag.startswith('J'):
        return 'a'
    if tag.startswith('V'):
        return 'v'
    if tag.startswith('N'):
        return 'n'
    if tag.startswith('R'):
        return 'r'
    return 'n'

def tokenize_and_lemmatize(text: str) -> List[str]:
    # FIX: preserve_line=True to avoid requiring punkt_tab for sentence segmentation
    tokens = word_tokenize(text, preserve_line=True)
    tokens = [t.lower() for t in tokens if t.isalpha()]

    tagged = pos_tag(tokens)

    lemmatizer = WordNetLemmatizer()
    stop = set(stopwords.words("english"))

    lemmas = []
    for tok, tg in tagged:
        if tok in stop:
            continue
        wn_pos = nltk_pos_to_wordnet_pos(tg)
        lemma = lemmatizer.lemmatize(tok, pos=wn_pos)
        if lemma and lemma not in stop:
            lemmas.append(lemma)
    return lemmas

def process_file(path: str) -> Tuple[str, List[str]]:
    base = os.path.basename(path)
    name, _ = os.path.splitext(base)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    core = strip_gutenberg_header_footer(raw)
    tokens = tokenize_and_lemmatize(core)

    clean_path = os.path.join(CLEAN_DIR, f"{name}.clean.txt")
    with open(clean_path, "w", encoding="utf-8") as f:
        f.write(" ".join(tokens))

    return name, tokens

def main():
    print("[INFO] Scanning raw texts ...")
    files = [os.path.join(RAW_DIR, fn) for fn in os.listdir(RAW_DIR) if fn.lower().endswith(".txt")]
    files.sort()
    if not files:
        raise SystemExit("No raw .txt files found under data/raw. Run the crawler first.")

    global_vocab = Counter()
    per_book_counts = []

    for fp in files:
        print(f"[INFO] Processing: {os.path.basename(fp)}")
        name, tokens = process_file(fp)
        cnt = Counter(tokens)
        global_vocab.update(cnt)
        per_book_counts.append({"book": name, "unique_tokens": len(cnt), "total_tokens": sum(cnt.values())})

    with open(PERBOOK_STATS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["book", "unique_tokens", "total_tokens"])
        writer.writeheader()
        writer.writerows(per_book_counts)
    print(f"[INFO] Per-book token stats -> {PERBOOK_STATS_CSV}")

    top100 = global_vocab.most_common(100)
    with open(TOP100_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "word", "count"])
        for i, (w, c) in enumerate(top100, start=1):
            writer.writerow([i, w, c])
    print(f"[INFO] Top-100 vocabulary -> {TOP100_CSV}")

    print("\nTop 20 preview:")
    for i, (w, c) in enumerate(top100[:20], start=1):
        print(f"{i:>2}. {w:<15} {c}")

if __name__ == "__main__":
    main()

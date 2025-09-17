# make_report.py
# Purpose: Generate a Markdown report that includes:
#  - Top-20 books (title + link)
#  - Token stats per book
#  - Global Top-100 words
#  - Methods (pipeline summary)
#  - Reproducible Commands (your terminal steps, read from outputs/operations.md)

import os
import datetime
import pandas as pd

OUTPUTS_DIR = "outputs"
REPORT_PATH = os.path.join(OUTPUTS_DIR, "report.md")
OPS_PATH = os.path.join(OUTPUTS_DIR, "operations.md")  # put your terminal steps here

METHODS_TEXT = """\
## Methods

1. **Crawling**
   - Crawl Project Gutenberg “Top 100 – Last 30 Days” page.
   - Extract the first 20 book entries and resolve their Plain Text (UTF-8) links.
   - Save raw `.txt` files to `data/raw/` and write `outputs/top20_books.csv`.

2. **Cleaning**
   - Remove Project Gutenberg header/footer using markers:
     `*** START OF THIS PROJECT GUTENBERG EBOOK ... ***` and
     `*** END OF THIS PROJECT GUTENBERG EBOOK ... ***`.
   - Keep only the text between these markers.

3. **Tokenization & Lemmatization**
   - NLTK `word_tokenize(..., preserve_line=True)` for tokens; lowercasing; keep alphabetic tokens.
   - POS tagging + WordNet lemmatization (map POS to {n, v, a, r}).
   - Remove English stopwords.

4. **Vocabulary & Statistics**
   - Build a global Counter across all books; export Top-100 (`outputs/top100_words.csv`).
   - For each book, record `total_tokens` and `unique_tokens` (`outputs/per_book_token_counts.csv`).
"""

def main():
    # --- Load data ---
    top20_csv = os.path.join(OUTPUTS_DIR, "top20_books.csv")
    perbook_csv = os.path.join(OUTPUTS_DIR, "per_book_token_counts.csv")
    top100_csv = os.path.join(OUTPUTS_DIR, "top100_words.csv")

    if not all(os.path.exists(p) for p in [top20_csv, perbook_csv, top100_csv]):
        raise SystemExit("Missing CSVs. Run the crawling and cleaning scripts first.")

    df_books = pd.read_csv(top20_csv)
    df_stats = pd.read_csv(perbook_csv)
    df_top100 = pd.read_csv(top100_csv)

    # --- Start writing Markdown ---
    lines = []
    lines.append("# Project Gutenberg Top-20 Analysis\n")
    lines.append(f"_Generated on: {datetime.datetime.now().isoformat(timespec='seconds')}_\n\n")
    lines.append("This report summarizes the 20 most downloaded public-domain ebooks (last 30 days), the per-book token statistics, and the global Top-100 words.\n\n")

    # Methods section
    lines.append(METHODS_TEXT + "\n")

    # Section: Books
    lines.append("## Top-20 Books (Last 30 Days)\n")
    for i, row in enumerate(df_books.itertuples(index=False), start=1):
        lines.append(f"{i}. [{row.title}]({row.book_page})\n")
    lines.append("\n")

    # Section: Per-book stats
    lines.append("## Token Statistics per Book\n")
    lines.append("| Book | Unique Tokens | Total Tokens |\n")
    lines.append("|------|---------------|--------------|\n")
    for row in df_stats.itertuples(index=False):
        lines.append(f"| {row.book} | {row.unique_tokens} | {row.total_tokens} |\n")
    lines.append("\n")

    # Section: Top-100 words
    lines.append("## Global Top-100 Words\n")
    lines.append("| Rank | Word | Count |\n")
    lines.append("|------|------|-------|\n")
    for row in df_top100.itertuples(index=False):
        lines.append(f"| {row.rank} | {row.word} | {row.count} |\n")
    lines.append("\n")

    # Section: Reproducible commands (optional)
    if os.path.exists(OPS_PATH):
        with open(OPS_PATH, "r", encoding="utf-8") as f:
            ops_text = f.read().strip()
        if ops_text:
            lines.append("## Reproducible Commands\n")
            lines.append("The following shell commands document the exact steps executed on the machine:\n\n")
            lines.append("```bash\n")
            lines.append(ops_text + "\n")
            lines.append("```\n")

    # Write file
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[INFO] Markdown report generated: {REPORT_PATH}")
    if os.path.exists(OPS_PATH):
        print(f"[INFO] Included operations from: {OPS_PATH}")
    else:
        print(f"[INFO] To include your terminal steps, put them into: {OPS_PATH}")

if __name__ == "__main__":
    main()

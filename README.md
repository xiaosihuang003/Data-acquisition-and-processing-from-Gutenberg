    # Exercise 2.2 — Data acquisition and processing from Project Gutenberg

    ## Overview
    This project crawls the “Top 100 — Last 30 Days” list from Project Gutenberg, downloads the **top-20** TXT ebooks, cleans out Gutenberg headers/footers, tokenizes and lemmatizes the text, and builds a unified vocabulary across all books. The repository includes code and generated statistics for full reproducibility.

    ## How to reproduce
        # Create and activate a virtual environment
        python3 -m venv .venv
        source .venv/bin/activate

        # Install dependencies
        pip install -r requirements.txt

        # (a)(b) Crawl top-100 (last 30 days) and download top-20 TXT ebooks
        python crawl_and_download.py

        # (c)(d) Clean, tokenize, lemmatize, and compute global vocabulary & stats
        python clean_and_vocab.py

        # Build the Markdown report (outputs/report.md)
        python make_report.py

    ## Outputs
    - `outputs/report.md` — main report (includes Methods and Reproducible Commands).
    - `outputs/top20_books.csv` — book titles, Gutenberg book-page URLs, TXT URLs, local paths.
    - `outputs/per_book_token_counts.csv` — per-book token totals and unique token counts.
    - `outputs/top100_words.csv` — global top-100 words with frequencies.
    - *(git-ignored)* `data/raw/` — raw downloaded TXT files.
    - *(git-ignored)* `data/clean/` — cleaned tokenized text for each book.

    ## Methods (brief)
    1. **Crawling**
       - Parse the “Top 100 — Last 30 Days” section of the scores page.
       - Take the first 20 items; resolve “Plain Text (UTF-8)” download links.
       - Save TXT files under `data/raw/` and write `outputs/top20_books.csv`.
    2. **Cleaning**
       - Remove Project Gutenberg header/footer using the markers:
         `*** START OF THIS PROJECT GUTENBERG EBOOK ... ***` and
         `*** END OF THIS PROJECT GUTENBERG EBOOK ... ***`.
       - Keep only the text between these markers.
    3. **Tokenization & Lemmatization**
       - `nltk.word_tokenize(..., preserve_line=True)`, lowercase, keep alphabetic tokens.
       - POS-tag tokens, map to WordNet POS {n,v,a,r}, lemmatize with WordNetLemmatizer.
       - Remove English stopwords.
    4. **Statistics**
       - Build a global `Counter` across all books; export top-100 words.
       - Record per-book `total_tokens` and `unique_tokens`.

    ## Project structure
    - `crawl_and_download.py` — crawler & downloader for the top-20 TXT ebooks.
    - `clean_and_vocab.py` — cleaning, tokenization, lemmatization, and statistics.
    - `make_report.py` — generates `outputs/report.md` from the CSVs.
    - `requirements.txt` — Python dependencies.
    - `.gitignore` — excludes `.venv/`, `data/raw/`, `data/clean/`, and other non-essential files.
    - `outputs/` — generated CSVs and the final Markdown report.

    ## Reproducible commands (optional)
    You can place your exact terminal session into `outputs/operations.md`, then re-run `python make_report.py` to embed it under a “Reproducible Commands” section in the report.

    ## Notes / Troubleshooting
    - If NLTK raises a `punkt_tab` lookup error, the pipeline auto-downloads required NLTK resources. If needed, run:
          python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
    - Raw and cleaned texts are not committed to keep the repository small; they can be regenerated with the scripts.

    ## Attribution
    Ebooks are from **Project Gutenberg** (public domain). Please review their terms of use: https://www.gutenberg.org/policy/permission.html


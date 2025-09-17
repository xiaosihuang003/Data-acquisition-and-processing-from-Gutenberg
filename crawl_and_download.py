# crawl_and_download.py
# Purpose: Crawl Project Gutenberg "Top 100 - Last 30 Days", pick top-20 ebooks,
# and download their Plain Text (UTF-8) files into data/raw. Also write a CSV
# with title + book page + txt url + local path.

import os
import time
import csv
import re
from typing import List, Tuple, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://www.gutenberg.org"
TOP_URL = f"{BASE_URL}/browse/scores/top"  # page that contains "Top 100 EBooks yesterday/last 7 days/last 30 days"
RAW_DIR = "data/raw"
OUTPUTS_DIR = "outputs"
CSV_PATH = os.path.join(OUTPUTS_DIR, "top20_books.csv")

HEADERS = {
    # Use a friendly UA to avoid being blocked by basic anti-bot filters
    "User-Agent": "Mozilla/5.0 (compatible; gutenberg-class-exercise/1.0; +https://example.edu)"
}

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def fetch(url: str) -> Optional[requests.Response]:
    """Fetch a URL with basic error handling and timeouts."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}")
        return None

def extract_last30_book_links(html: str) -> List[Tuple[str, str]]:
    """
    Parse the Top page and extract the list (title, book_page_url) for "Top 100 EBooks last 30 days".
    Project Gutenberg structures the page with multiple <ol> lists; we find the right header first.
    """
    soup = BeautifulSoup(html, "lxml")

    # Find the header that explicitly mentions "Top 100 EBooks last 30 days"
    header = None
    for h2 in soup.find_all(["h2", "h3"]):
        if h2.get_text(strip=True).lower().startswith("top 100 ebooks last 30 days"):
            header = h2
            break
    if not header:
        raise RuntimeError("Could not find the 'Top 100 EBooks last 30 days' section.")

    # The following <ol> after the header contains the list of books.
    ol = header.find_next("ol")
    if not ol:
        raise RuntimeError("Could not find the <ol> list after the last-30-days header.")

    results = []
    for a in ol.find_all("a", href=True):
        title = a.get_text(" ", strip=True)
        href = a["href"]
        # Normalize book page url
        if href.startswith("/"):
            book_url = BASE_URL + href
        elif href.startswith("http"):
            book_url = href
        else:
            book_url = f"{BASE_URL}/{href}"
        results.append((title, book_url))
    return results

def find_txt_download_url(book_page_html: str) -> Optional[str]:
    """
    From a single book page, try to find a reliable Plain Text (UTF-8) download URL.
    Fallbacks:
      1) Link text containing "Plain Text UTF-8"
      2) Link text containing "Plain Text"
      3) A files page pattern like /files/<id>/<id>-0.txt or similar
    """
    soup = BeautifulSoup(book_page_html, "lxml")

    # Strategy 1: look for explicit "Plain Text UTF-8"
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True).lower()
        if "plain text" in text:  # covers "Plain Text UTF-8" and "Plain Text"
            href = a["href"]
            if href.startswith("/"):
                return BASE_URL + href
            elif href.startswith("http"):
                return href

    # Strategy 2: infer from ebook number and construct a canonical files URL
    # The book page URLs are often like: https://www.gutenberg.org/ebooks/12345
    m = re.search(r"/ebooks/(\d+)", soup.base.get("href", "") if soup.base else "")
    if not m:
        # Try from canonical link tag
        link = soup.find("link", rel="canonical")
        if link and link.get("href"):
            m = re.search(r"/ebooks/(\d+)", link["href"])
    if not m:
        # Try from current URL in <meta property="og:url">
        meta = soup.find("meta", property="og:url")
        if meta and meta.get("content"):
            m = re.search(r"/ebooks/(\d+)", meta["content"])
    if m:
        book_id = m.group(1)
        candidates = [
            f"{BASE_URL}/files/{book_id}/{book_id}-0.txt",
            f"{BASE_URL}/files/{book_id}/{book_id}.txt",
            f"{BASE_URL}/cache/epub/{book_id}/pg{book_id}.txt",
            f"{BASE_URL}/files/{book_id}/pg{book_id}.txt",
        ]
        for url in candidates:
            resp = fetch(url)
            if resp and resp.ok and len(resp.text.strip()) > 0:
                return url

    return None

def download_txt(title: str, book_url: str) -> Tuple[str, Optional[str]]:
    """
    Download the plain text for a given book page URL.
    Returns: (local_path, txt_url_or_none)
    """
    # Fetch book page
    resp = fetch(book_url)
    if not resp:
        return "", None

    txt_url = find_txt_download_url(resp.text)
    if not txt_url:
        print(f"[WARN] No Plain Text link found for: {book_url}")
        return "", None

    # Stream download
    resp_txt = fetch(txt_url)
    if not resp_txt:
        return "", None

    # Sanitize filename
    safe_title = re.sub(r"[^\w\-\. ]+", "_", title).strip()[:120]
    filename = f"{safe_title}.txt" if safe_title else os.path.basename(txt_url) or "book.txt"
    local_path = os.path.join(RAW_DIR, filename)
    with open(local_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(resp_txt.text)

    return local_path, txt_url

def main():
    print("[INFO] Fetching Top 100 page ...")
    resp = fetch(TOP_URL)
    if not resp:
        raise SystemExit("Failed to load top page.")

    print("[INFO] Parsing last-30-days section ...")
    books = extract_last30_book_links(resp.text)
    if not books:
        raise SystemExit("No books found in last-30-days section.")

    # Keep only first 20
    top20 = books[:20]
    print(f"[INFO] Found {len(top20)} books (top-20 of last 30 days).")

    rows = []
    for title, book_url in tqdm(top20, desc="Downloading", unit="book"):
        local_path, txt_url = download_txt(title, book_url)
        rows.append(
            {
                "title": title,
                "book_page": book_url,
                "txt_url": txt_url or "",
                "local_path": local_path or "",
            }
        )
        time.sleep(1)  # be polite

    # Write CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "book_page", "txt_url", "local_path"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[INFO] Done. CSV written to: {CSV_PATH}")
    print(f"[INFO] Raw texts saved under: {RAW_DIR}")

if __name__ == "__main__":
    main()

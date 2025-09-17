Last login: Sun Sep 14 06:06:04 on ttys005
xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ touch requirements.txt
xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ code .
xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ python3 -m venv .venv
xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ source .venv/bin/activate
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ pip install -r requirements.txt
Collecting requests
  Downloading requests-2.32.5-py3-none-any.whl (64 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.7/64.7 kB 2.3 MB/s eta 0:00:00
Collecting beautifulsoup4
  Downloading beautifulsoup4-4.13.5-py3-none-any.whl (105 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 105.1/105.1 kB 7.1 MB/s eta 0:00:00
Collecting lxml
  Downloading lxml-6.0.1-cp310-cp310-macosx_10_9_universal2.whl (8.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.4/8.4 MB 22.2 MB/s eta 0:00:00
Collecting nltk
  Downloading nltk-3.9.1-py3-none-any.whl (1.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/1.5 MB 22.4 MB/s eta 0:00:00
Collecting pandas
  Downloading pandas-2.3.2-cp310-cp310-macosx_11_0_arm64.whl (10.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.8/10.8 MB 24.4 MB/s eta 0:00:00
Collecting tqdm
  Downloading tqdm-4.67.1-py3-none-any.whl (78 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.5/78.5 kB 10.1 MB/s eta 0:00:00
Collecting urllib3<3,>=1.21.1
  Downloading urllib3-2.5.0-py3-none-any.whl (129 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 129.8/129.8 kB 11.4 MB/s eta 0:00:00
Collecting certifi>=2017.4.17
  Downloading certifi-2025.8.3-py3-none-any.whl (161 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 161.2/161.2 kB 10.7 MB/s eta 0:00:00
Collecting charset_normalizer<4,>=2
  Downloading charset_normalizer-3.4.3-cp310-cp310-macosx_10_9_universal2.whl (207 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 207.7/207.7 kB 12.9 MB/s eta 0:00:00
Collecting idna<4,>=2.5
  Using cached idna-3.10-py3-none-any.whl (70 kB)
Collecting typing-extensions>=4.0.0
  Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.6/44.6 kB 5.0 MB/s eta 0:00:00
Collecting soupsieve>1.2
  Downloading soupsieve-2.8-py3-none-any.whl (36 kB)
Collecting regex>=2021.8.3
  Downloading regex-2025.9.1-cp310-cp310-macosx_11_0_arm64.whl (286 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 286.6/286.6 kB 15.9 MB/s eta 0:00:00
Collecting click
  Downloading click-8.2.1-py3-none-any.whl (102 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 102.2/102.2 kB 11.5 MB/s eta 0:00:00
Collecting joblib
  Downloading joblib-1.5.2-py3-none-any.whl (308 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 308.4/308.4 kB 18.1 MB/s eta 0:00:00
Collecting tzdata>=2022.7
  Downloading tzdata-2025.2-py2.py3-none-any.whl (347 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 347.8/347.8 kB 17.1 MB/s eta 0:00:00
Collecting python-dateutil>=2.8.2
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Collecting pytz>=2020.1
  Downloading pytz-2025.2-py2.py3-none-any.whl (509 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 509.2/509.2 kB 19.0 MB/s eta 0:00:00
Collecting numpy>=1.22.4
  Downloading numpy-2.2.6-cp310-cp310-macosx_14_0_arm64.whl (5.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.3/5.3 MB 24.4 MB/s eta 0:00:00
Collecting six>=1.5
  Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: pytz, urllib3, tzdata, typing-extensions, tqdm, soupsieve, six, regex, numpy, lxml, joblib, idna, click, charset_normalizer, certifi, requests, python-dateutil, nltk, beautifulsoup4, pandas
Successfully installed beautifulsoup4-4.13.5 certifi-2025.8.3 charset_normalizer-3.4.3 click-8.2.1 idna-3.10 joblib-1.5.2 lxml-6.0.1 nltk-3.9.1 numpy-2.2.6 pandas-2.3.2 python-dateutil-2.9.0.post0 pytz-2025.2 regex-2025.9.1 requests-2.32.5 six-1.17.0 soupsieve-2.8 tqdm-4.67.1 typing-extensions-4.15.0 tzdata-2025.2 urllib3-2.5.0

[notice] A new release of pip is available: 23.0.1 -> 25.2
[notice] To update, run: pip install --upgrade pip

(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ mkdir -p data/raw data/clean outputs

(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ ls
data			outputs			requirements.txt
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ touch crawl_and_download.py
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ ls
crawl_and_download.py	outputs
data			requirements.txt
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ tree
.
├── crawl_and_download.py
├── data
│   ├── clean
│   └── raw
├── outputs
└── requirements.txt

5 directories, 2 files
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ python crawl_and_download.py
[INFO] Fetching Top 100 page ...
[INFO] Parsing last-30-days section ...
[INFO] Found 20 books (top-20 of last 30 days).
Downloading: 100%|████████████████████████████| 20/20 [01:06<00:00,  3.30s/book]
[INFO] Done. CSV written to: outputs/top20_books.csv
[INFO] Raw texts saved under: data/raw
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ tree
.
├── crawl_and_download.py
├── data
│   ├── clean
│   └── raw
│       ├── A Room with a View by E. M.  Forster _57478_.txt
│       ├── Alice_s Adventures in Wonderland by Lewis Carroll _60624_.txt
│       ├── Beowulf_ An Anglo-Saxon Epic Poem _52640_.txt
│       ├── Cranford by Elizabeth Cleghorn Gaskell _40784_.txt
│       ├── Dracula by Bram Stoker _47752_.txt
│       ├── Frankenstein_ Or_ The Modern Prometheus by Mary Wollstonecraft Shelley _117668_.txt
│       ├── History of Tom Jones_ a Foundling by Henry Fielding _39646_.txt
│       ├── How to Observe_ Morals and Manners by Harriet Martineau _51437_.txt
│       ├── Little Women_ Or_ Meg_ Jo_ Beth_ and Amy by Louisa May Alcott _53318_.txt
│       ├── Middlemarch by George Eliot _55252_.txt
│       ├── Moby Dick_ Or_ The Whale by Herman Melville _120117_.txt
│       ├── Pride and Prejudice by Jane Austen _71294_.txt
│       ├── Romeo and Juliet by William Shakespeare _81275_.txt
│       ├── The Adventures of Ferdinand Count Fathom _ Complete by T.  Smollett _40314_.txt
│       ├── The Blue Castle_ a novel by L. M.  Montgomery _45401_.txt
│       ├── The Complete Works of William Shakespeare by William Shakespeare _56211_.txt
│       ├── The Enchanted April by Elizabeth Von Arnim _45511_.txt
│       ├── The Expedition of Humphry Clinker by T.  Smollett _40226_.txt
│       ├── The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson _44586_.txt
│       └── Twenty years after by Alexandre Dumas and Auguste Maquet _39708_.txt
├── outputs
│   └── top20_books.csv
└── requirements.txt

5 directories, 23 files
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ ls
crawl_and_download.py	outputs
data			requirements.txt
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ cd outputs 
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/outputs $ ls
top20_books.csv
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/outputs $ cat top20_books.csv

(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ touch clean_and_vocab.py
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ ls
clean_and_vocab.py	data			requirements.txt
crawl_and_download.py	outputs
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ python clean_and_vocab.py
[nltk_data] Downloading package punkt to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.
[nltk_data] Downloading package stopwords to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data]   Unzipping corpora/stopwords.zip.
[nltk_data] Downloading package wordnet to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data] Downloading package omw-1.4 to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data] Downloading package averaged_perceptron_tagger to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data]   Unzipping taggers/averaged_perceptron_tagger.zip.
[nltk_data] Downloading package averaged_perceptron_tagger_eng to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data]   Unzipping taggers/averaged_perceptron_tagger_eng.zip.
[INFO] Scanning raw texts ...
[INFO] Processing: A Room with a View by E. M.  Forster _57478_.txt
Traceback (most recent call last):
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/clean_and_vocab.py", line 190, in <module>
    main()
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/clean_and_vocab.py", line 163, in main
    name, tokens = process_file(fp)
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/clean_and_vocab.py", line 142, in process_file
    tokens = tokenize_and_lemmatize(core)
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/clean_and_vocab.py", line 110, in tokenize_and_lemmatize
    tokens = word_tokenize(text)
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/lib/python3.10/site-packages/nltk/tokenize/__init__.py", line 142, in word_tokenize
    sentences = [text] if preserve_line else sent_tokenize(text, language)
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/lib/python3.10/site-packages/nltk/tokenize/__init__.py", line 119, in sent_tokenize
    tokenizer = _get_punkt_tokenizer(language)
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/lib/python3.10/site-packages/nltk/tokenize/__init__.py", line 105, in _get_punkt_tokenizer
    return PunktTokenizer(language)
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/lib/python3.10/site-packages/nltk/tokenize/punkt.py", line 1744, in __init__
    self.load_lang(lang)
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/lib/python3.10/site-packages/nltk/tokenize/punkt.py", line 1749, in load_lang
    lang_dir = find(f"tokenizers/punkt_tab/{lang}/")
  File "/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/lib/python3.10/site-packages/nltk/data.py", line 579, in find
    raise LookupError(resource_not_found)
LookupError: 
**********************************************************************
  Resource punkt_tab not found.
  Please use the NLTK Downloader to obtain the resource:

  >>> import nltk
  >>> nltk.download('punkt_tab')
  
  For more information see: https://www.nltk.org/data.html

  Attempted to load tokenizers/punkt_tab/english/

  Searched in:
    - '/Users/xiaosihuang/nltk_data'
    - '/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/nltk_data'
    - '/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/share/nltk_data'
    - '/Users/xiaosihuang/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg/.venv/lib/nltk_data'
    - '/usr/share/nltk_data'
    - '/usr/local/share/nltk_data'
    - '/usr/lib/nltk_data'
    - '/usr/local/lib/nltk_data'
**********************************************************************

(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ python clean_and_vocab.py

[nltk_data] Downloading package punkt_tab to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt_tab.zip.
[nltk_data] Downloading package wordnet to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data]   Package wordnet is already up-to-date!
[nltk_data] Downloading package omw-1.4 to
[nltk_data]     /Users/xiaosihuang/nltk_data...
[nltk_data]   Package omw-1.4 is already up-to-date!
[INFO] Scanning raw texts ...
[INFO] Processing: A Room with a View by E. M.  Forster _57478_.txt
[INFO] Processing: Alice_s Adventures in Wonderland by Lewis Carroll _60624_.txt
[INFO] Processing: Beowulf_ An Anglo-Saxon Epic Poem _52640_.txt
[INFO] Processing: Cranford by Elizabeth Cleghorn Gaskell _40784_.txt
[INFO] Processing: Dracula by Bram Stoker _47752_.txt
[INFO] Processing: Frankenstein_ Or_ The Modern Prometheus by Mary Wollstonecraft Shelley _117668_.txt
[INFO] Processing: History of Tom Jones_ a Foundling by Henry Fielding _39646_.txt
[INFO] Processing: How to Observe_ Morals and Manners by Harriet Martineau _51437_.txt
[INFO] Processing: Little Women_ Or_ Meg_ Jo_ Beth_ and Amy by Louisa May Alcott _53318_.txt
[INFO] Processing: Middlemarch by George Eliot _55252_.txt
[INFO] Processing: Moby Dick_ Or_ The Whale by Herman Melville _120117_.txt
[INFO] Processing: Pride and Prejudice by Jane Austen _71294_.txt
[INFO] Processing: Romeo and Juliet by William Shakespeare _81275_.txt
[INFO] Processing: The Adventures of Ferdinand Count Fathom _ Complete by T.  Smollett _40314_.txt
[INFO] Processing: The Blue Castle_ a novel by L. M.  Montgomery _45401_.txt
[INFO] Processing: The Complete Works of William Shakespeare by William Shakespeare _56211_.txt
[INFO] Processing: The Enchanted April by Elizabeth Von Arnim _45511_.txt
[INFO] Processing: The Expedition of Humphry Clinker by T.  Smollett _40226_.txt
[INFO] Processing: The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson _44586_.txt
[INFO] Processing: Twenty years after by Alexandre Dumas and Auguste Maquet _39708_.txt
[INFO] Per-book token stats -> outputs/per_book_token_counts.csv
[INFO] Top-100 vocabulary -> outputs/top100_words.csv

Top 20 preview:
 1. say             16700
 2. would           10635
 3. one             9805
 4. make            9430
 5. go              9299
 6. come            9175
 7. know            8083
 8. good            7649
 9. see             7108
10. shall           6913
11. thou            6794
12. take            6635
13. think           6372
14. like            6281
15. could           6141
16. give            6083
17. well            6061
18. man             5761
19. upon            5737
20. must            5498
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ 
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ touch make_report.py
(.venv) xiaosihuang@Xiaosis-MacBook-Pro ~/gitwork/StatisticalMethodsforTextDataAnalysis/exe2_2.2gutenberg $ python make_report.py

[INFO] Markdown report generated: outputs/report.md
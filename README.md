# Weibo Comment Analysis

This repository contains a simple demo for collecting and analyzing Weibo
comments related to sports celebrities. The goal is to study how public
reaction reflects national pride and sentiment.

## Structure

- `src/weibo_scraper.py` – download comments for a specific Weibo post.
  Requires a valid logged-in cookie. Data are saved as CSV.
- `src/analyze_comments.py` – perform sentiment analysis, generate a
  word cloud and topic models, and save plots under `figures/`.
- `data/sample_comments.csv` – small example data set.

## Usage

1. Install Python dependencies (see below).
2. Optionally scrape real comments with `python3 src/weibo_scraper.py`.
   Update `POST_ID` and `COOKIE` in the script before running.
3. Run the analysis:

   ```bash
   python3 src/analyze_comments.py
   ```

4. Generated figures will be in the `figures/` directory.

### Dependencies

```bash
pip install jieba pandas matplotlib seaborn gensim wordcloud snownlp requests
```

The analysis is for demonstration only. When scraping real data, please
respect Weibo's terms of service and privacy policies.

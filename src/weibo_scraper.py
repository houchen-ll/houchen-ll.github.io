"""Basic script to collect Weibo comments for a given post.

This script uses the unofficial mobile API endpoint. You must provide
valid cookies from a logged-in Weibo account. Scraping is subject to
Weibo's terms of service.
"""

from __future__ import annotations

import csv
import requests


def fetch_comments(post_id: str, cookie: str, page: int = 1) -> list[str]:
    """Fetch a single page of comments for ``post_id``.

    Parameters
    ----------
    post_id : str
        The Weibo post ID.
    cookie : str
        Cookie string from a logged-in browser session.
    page : int
        Page number to retrieve.

    Returns
    -------
    list[str]
        A list of comment texts.
    """
    url = (
        f"https://m.weibo.cn/comments/hotflow?id={post_id}&mid={post_id}"
        "&max_id_type=0"
    )
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie,
    }
    params = {"page": page}
    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("data", {}).get("data", [])
    return [item.get("text", "") for item in items]


def crawl(post_id: str, cookie: str, pages: int = 5, out_file: str = "data/comments.csv") -> None:
    """Crawl multiple pages of comments and save them to ``out_file``.
    
    Parameters
    ----------
    post_id : str
        The target Weibo post ID.
    cookie : str
        Cookie string from a logged-in browser session.
    pages : int
        How many pages to retrieve.
    out_file : str
        Destination CSV file path.
    """
    comments: list[str] = []
    for page in range(1, pages + 1):
        comments.extend(fetch_comments(post_id, cookie, page))

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["comment"])
        for text in comments:
            writer.writerow([text])


if __name__ == "__main__":
    # Example usage
    POST_ID = "000000"  # replace with real post id
    COOKIE = "your_cookie_here"  # replace with cookie from your browser
    crawl(POST_ID, COOKIE)

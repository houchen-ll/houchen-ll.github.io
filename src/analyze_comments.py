"""Analyze Weibo comments for sentiment and topics."""

from __future__ import annotations

import os
from pathlib import Path

import jieba
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gensim import corpora, models
from wordcloud import WordCloud
from snownlp import SnowNLP


def load_comments(csv_path: str) -> pd.Series:
    """Load comments from a CSV file."""
    df = pd.read_csv(csv_path)
    return df["comment"].dropna()


def segment_comments(comments: pd.Series) -> list[list[str]]:
    """Segment Chinese text using ``jieba``."""
    return [list(jieba.cut(c)) for c in comments]


def sentiment_scores(comments: pd.Series) -> pd.Series:
    """Return sentiment scores using ``SnowNLP`` (0-1)."""
    return comments.apply(lambda c: SnowNLP(c).sentiments)


def plot_sentiment(scores: pd.Series, out_dir: str) -> None:
    """Save a sentiment distribution plot."""
    plt.figure(figsize=(6, 4))
    sns.histplot(scores, bins=20, kde=True, color="skyblue")
    plt.title("Sentiment Distribution")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "sentiment.png"))
    plt.close()


def generate_wordcloud(tokens: list[list[str]], out_dir: str) -> None:
    """Create and save a word cloud image."""
    all_words = " ".join([" ".join(t) for t in tokens])
    wc = WordCloud(font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                   background_color="white",
                   width=800,
                   height=400).generate(all_words)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    wc.to_file(os.path.join(out_dir, "wordcloud.png"))


def topic_model(tokens: list[list[str]], num_topics: int = 3) -> models.LdaModel:
    """Fit an LDA topic model using ``gensim``."""
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(text) for text in tokens]
    lda = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, random_state=42)
    return lda


def plot_topic_distribution(lda: models.LdaModel, out_dir: str) -> None:
    """Plot the top words for each topic."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    topics = lda.show_topics(num_topics=-1, formatted=False)
    for idx, topic in topics:
        words, weights = zip(*topic)
        plt.figure(figsize=(6, 4))
        sns.barplot(x=list(weights), y=list(words), color="salmon")
        plt.title(f"Topic {idx}")
        plt.xlabel("Weight")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"topic_{idx}.png"))
        plt.close()


def main() -> None:
    comments = load_comments("data/sample_comments.csv")
    tokens = segment_comments(comments)
    scores = sentiment_scores(comments)
    plot_sentiment(scores, "figures")
    generate_wordcloud(tokens, "figures")
    lda = topic_model(tokens)
    plot_topic_distribution(lda, "figures")
    print("Analysis complete. Figures saved to ./figures/")


if __name__ == "__main__":
    main()

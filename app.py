""" This script reads all markdown files in a directory, extracts the text, performs sentiment analysis on the text, and visualises the sentiment over time. """

import os
import markdown
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)


def find_markdown_files(directory: str) -> List[str]:
    """Find all markdown files in a directory and return a list of file paths."""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files


def markdown_to_text(markdown_file) -> List[Dict]:
    """Read a markdown file and return the text content."""
    with open(markdown_file, "r", encoding="utf-8") as file:
        text = file.read()
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()

    return text


def semantic_analysis(text) -> float:
    """Run semantic analysis on the text and return the sentiment."""
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment


def visualise(all_text):
    """Visualise the sentiment analysis over time with a scatter plot."""

    dates = []

    for record in all_text:
        try:
            dates.append(mdates.datestr2num(record["date"]))
        except:
            logging.error(f"dodgy date found: {record['date']}")

    sentiments = [record["semantics"] for record in all_text]

    plt.figure(figsize=(10, 5))
    plt.scatter(dates, sentiments, c=sentiments, cmap="RdYlGn", alpha=0.5)
    plt.colorbar(label="Sentiment")
    plt.title("Sentiment Analysis Over Time")
    plt.xlabel("Month")
    plt.ylabel("Sentiment")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().tick_params(axis="x", labelsize=8)  # reduce x-axis label size
    plt.xticks(rotation="vertical")
    plt.show()


if __name__ == "__main__":
    """ Kicks everything off """
    markdown_files = find_markdown_files("C:\Obsidian\james-things\Daily thoughts")

    all_text = []

    for file in markdown_files:
        text = markdown_to_text(file)
        file_date = file.split("\\")[-1].split(".")[0]  # remove .md extension

        semantics = semantic_analysis(text)
        record = {"date": file_date, "semantics": semantics}
        all_text.append(record)

    visualise(all_text)

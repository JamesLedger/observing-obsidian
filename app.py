import os
import markdown
from bs4 import BeautifulSoup


def find_markdown_files(directory):
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files


def markdown_to_text(markdown_file):
    with open(markdown_file, "r", encoding="utf-8") as file:
        text = file.read()
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()
    file_date = markdown_file.split("\\")[-1]
    return {file_date: text}


if __name__ == "__main__":
    markdown_files = find_markdown_files("C:\Obsidian\james-things\Daily thoughts")

    all_text = {}

    for file in markdown_files:
        text = markdown_to_text(file)
        all_text.update(text)

    print(all_text)

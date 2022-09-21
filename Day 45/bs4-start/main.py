from bs4 import BeautifulSoup
import requests

with requests.get("https://news.ycombinator.com/") as r:
    response = r.text

soup = BeautifulSoup(response, "html.parser")
articles = soup.findAll(name="a", class_="titlelink")
article_texts = [article.getText() for article in articles]
article_links = [article.get("href") for article in articles]
article_upvotes = [int(score.getText().split()[0]) for score in soup.findAll(name="span", class_="score")]

print(article_texts)
print(article_links)
print(article_upvotes)

max_upvotes = max(article_upvotes)
max_upvotes_index = article_upvotes.index(max_upvotes)
print(article_texts[max_upvotes_index])
print(article_links[max_upvotes_index])

# article_upvote = soup.find(name="span", class_="score").getText()
# print(article_upvote)

from bs4 import BeautifulSoup
import requests

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

with requests.get(URL) as r:
    content = r.text

soup = BeautifulSoup(content, "html.parser")  # parser is like a content interpreter
all_movies = [movie.getText() for movie in soup.findAll(name="h3", class_="title")]  # creating list of movies from soup
all_movies = all_movies[::-1]  # reversing the order using the splice operator (start:stop:step)
print(all_movies)

with open("list_of_movies.txt", mode="w") as w:
    for movie in all_movies:
        w.write(f"{movie}\n")


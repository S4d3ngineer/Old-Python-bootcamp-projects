import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


URL = "https://www.billboard.com/charts/hot-100/"
# date = "2000-01-01"  # for testing purposes

date = input("Which year do you want to travel to? Please enter date in following format: YYYY-MM-DD\n")
with requests.get(f"{URL}{date}/") as r:
    content = r.text
soup = BeautifulSoup(content, "html.parser")
raw_titles = soup.select("li.o-chart-results-list__item h3.c-title")
raw_artists = soup.select("li.o-chart-results-list__item h3.c-title ~ span.c-label")
song_titles = [song.getText().strip("\n") for song in raw_titles]
artist_list = [artist.getText().strip("\n") for artist in raw_artists]
print(song_titles)
print(artist_list)

# print(soup.prettify())

# scope = "streaming"
# # it looks like class SOA is finding environmental variables on its own
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# sp.add_to_queue(uri="https://open.spotify.com/track/2w09i8WQjzVIIPEcU3TJM4?si=3036f8fbe6b7498e")

scope = "playlist-modify-private"
# it looks like class SOA is finding environmental variables on its own
# SOA class will look for a cache path to find token - if it doesn't exist it is going to try and create new token
# if possible
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        show_dialog=True,
        cache_path="token.txt"))

user_id = sp.current_user()["id"]

song_ids = []
for n in range(len(song_titles)):
    try:
        result = sp.search(q=f"track: {song_titles[n]}, artist: {artist_list[n]}",
                           type="track")["tracks"]["items"][0]["id"]
        song_ids.append(result)
    except IndexError:
        print(f"Song {song_titles[n]} has not been found!")
print(song_ids)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description="")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_ids, position=None)

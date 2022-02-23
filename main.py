import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# SPOTIPY PARAMS

SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = "http://example.com"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_secret=SPOTIPY_CLIENT_SECRET,
        client_id=SPOTIPY_CLIENT_ID,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

# MAIN CODE

date = input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD: ")

year = date[:4]
month = date[4:6]
day = date [6:8]

endpoint = "https://www.officialcharts.com/charts/singles-chart/" + year + month + day

response = requests.get(endpoint)
billboard_web_page = response.text

soup = BeautifulSoup(billboard_web_page, "html.parser")

titles_soup = soup.find_all("div", class_="title")

titles = [title.get_text() for title in titles_soup]
titles = [title.replace("\n", "") for title in titles]

print(titles)

song_uris = []
for title in titles:
    result = sp.search(f"track:{title} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{title} doesn't exist in Spotify. Skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{year}/{month}/{day} Billboard100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
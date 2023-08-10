from bs4 import BeautifulSoup
from dotenv import loadenv
import requests, os
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pprint
loadenv()
date = input("Which year do you want to travel to? Enter the date in this format YYYY-MM-DD ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
CLIENT_ID_SPOTIFY = os.getenv("CLIENT_ID_SPOTIFY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
redirect_URI = "http://example.com"
USERNAME = os.getenv("USERNAME")
CODE = os.getenv("CODE")
response = requests.get(url=URL)
content = response.text


soup = BeautifulSoup(content, "html.parser")
artists = soup.find_all(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")

# get artist names in order
artists_name = [artist.getText() for artist in artists]
artists_name = [string.strip().replace('\n', '').replace('\t', '') for string in artists_name]
songs = soup.find_all("h3", "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only","title-of-a-story")
# get songs in the same order
songs_list = [song.getText() for song in songs]
songs_list = [string.strip().replace('\n','').replace('\t', '') for string in songs_list]

# create a dictionnary with song titles and artists

playlist = {key:value for (key, value) in zip(artists_name, songs_list)}

# pass data to Spotify

spotify_request = SpotifyOAuth(client_id=CLIENT_ID_SPOTIFY, client_secret=CLIENT_SECRET, redirect_uri=redirect_URI, scope="playlist-modify-private", username=USERNAME)

# create a list of specified URI's for list of songs
sp = spotipy.Spotify(auth_manager=spotify_request)
songs_uri = []
for song in songs_list:
    brute_data = sp.search(q=song, type="track", limit=1)
    songs_uri.append(brute_data["tracks"]["items"][0]["uri"])

spotify_playlist = sp.user_playlist_create(user=USERNAME,name=f"{date} Billboard 100",public=False)
playlist_id = spotify_playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=songs_uri)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

def play_song(song_name):
    results = sp.search(q=song_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        print(f"🎵 Playing: {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}")
    else:
        print("Song not found")


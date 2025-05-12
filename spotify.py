import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from pathlib import Path
from eleven_labs_voice import speak
import os
import re

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


def extract_song_query(prompt):
    prompt = str(prompt).lower().strip()

    # Remove punctuation
    prompt = re.sub(r'[^\w\s]', '', prompt)

    # Remove filler phrases
    filler_phrases = ["play the song", "play", "can you", "could you", "please", "i want to hear", "the song"]
    for phrase in filler_phrases:
        if phrase in prompt:
            prompt = prompt.replace(phrase, "")

    prompt = prompt.strip()

    # Try to split by "by" to get song and artist
    if " by " in prompt:
        song, artist = prompt.split(" by ", 1)
        return song.strip(), artist.strip()
    if " from " in prompt:
        song, album = prompt.split(" from ",1)
        return song.strip(), album.strip()

    return prompt.strip(), ""


def play_song(prompt):
    prompt = str(prompt).lower()
    song, second = extract_song_query(prompt)

    if " from " in prompt.lower():
        query = f"track:{song} album:{second}"
    elif second:
        query = f"track:{song} artist:{second}"
    else:
        query = f"track:{song}"

    results = sp.search(q=query, type="track", limit=5)
    if results["tracks"]["items"]:
        track = results['tracks']['items'][0]
        track_uri = track['uri']
        details = f"Playing: {track['name']} by {track['artists'][0]['name']}"
        print(f"🎵 {details}")
        speak(details)

        devices = sp.devices()
        if not devices["devices"]:
            return print("No active devices found")

        device_id = devices["devices"][0]["id"]
        sp.start_playback(device_id=device_id, uris=[track_uri])
    else:
        print("❌ Song not found.")

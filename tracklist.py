"""Module for extracting and processing Spotify playlist tracks.

This module provides functionality to extract track information from Spotify
playlists using the Spotify Web API.
"""

import os
import re
from typing import List, Dict, Optional

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Setup auth manager
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
spotify_client = spotipy.Spotify(auth_manager=auth_manager)


def extract_playlist_id(playlist_url: str) -> Optional[str]:
    """Extract the playlist ID from a Spotify playlist URL.

    Args:
        playlist_url: The full URL of the Spotify playlist.

    Returns:
        The playlist ID if found, None otherwise.
    """
    match = re.search(r"playlist\/([a-zA-Z0-9]+)", playlist_url)
    return match.group(1) if match else None


def get_playlist_tracks(playlist_url: str) -> List[Dict[str, str]]:
    """Retrieve all tracks from a Spotify playlist.

    Args:
        playlist_url: The full URL of the Spotify playlist.

    Returns:
        A list of dictionaries containing track information including title,
        artist, album, album artist, and album art URL.
    """
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("Invalid playlist URL")
        return []

    results = spotify_client.playlist_items(playlist_id)
    tracks = []

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                track_name = track['name']
                artist_names = ', '.join(
                    [artist['name'] for artist in track['artists']]
                )
                album_name = track['album']['name']
                album_art_url = (
                    track['album']['images'][0]['url']
                    if track['album']['images']
                    else None
                )

                tracks.append({
                    "title": track_name,
                    "artist": artist_names,
                    "album": album_name,
                    "album_artist": artist_names,
                    "album_art_url": album_art_url
                })

        if results['next']:
            results = spotify_client.next(results)
        else:
            break

    return tracks

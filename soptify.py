from pytubefix import YouTube, Search
from pytubefix.cli import on_progress
from tracklist import get_playlist_tracks
from mutagen.mp4 import MP4, MP4Cover
import os
import time
import requests
import re

def sanitize_filename(name):
    '''
    Remove illegal characters from song filename
    '''
    return re.sub(r'[\\/*?:"<>|]', "", name)

def embed_album_art(file_path, image_url, metadata=None):
    '''
    Embed album art and metadata into the audio file (adds artist, album, and title tags)
    '''
    try:
        audio = MP4(file_path)

        # Album art
        if image_url:
            img_data = requests.get(image_url).content
            audio["covr"] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]
            print("🖼️  Album art embedded.")

        # Metadata
        if metadata:
            audio["©nam"] = metadata.get("title", "")
            audio["©ART"] = metadata.get("artist", "")
            audio["aART"] = metadata.get("album_artist", metadata.get("artist", ""))
            audio["©alb"] = metadata.get("album", "")
            print("🎵 Metadata embedded.")

        audio.save()

    except Exception as e:
        print(f"⚠️  Failed to embed metadata: {e}")

def download(url, title=None, image_url=None, metadata=None):
    '''
    Download the audio from the given URL and save it to the specified path.

    '''
    PATH = "./music/"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    yt = YouTube(url, on_progress_callback=on_progress)
    audio_stream = yt.streams.get_audio_only()
    title = sanitize_filename(title or yt.title)
    output_path = os.path.join(PATH, title + ".m4a")
    audio_stream.download(output_path=PATH, filename=title + ".m4a")
    print(f"✅ Saved as: {output_path}")

    embed_album_art(output_path, image_url, metadata)

def search_and_download(query, image_url=None, metadata=None):
    '''
    Search for the video on YouTube and download it.
    ''' 
    results = Search(query).results
    if not results:
        print(f"❌ No results found for: {query}")
        return

    video = results[0]
    print(f"⬇️  Downloading: {video.title}")
    download(video.watch_url, title=video.title, image_url=image_url, metadata=metadata)

if __name__ == "__main__":
    playlist_url = input("Enter Spotify playlist link: ")
    songs = get_playlist_tracks(playlist_url)

    for index, track in enumerate(songs, start=1):
        query = f"{track['title']} by {track['artist']} Official Audio"
        print(f"\n🎧 {index}/{len(songs)}: Searching for {query}")
        search_and_download(query, track["album_art_url"], metadata=track)
        time.sleep(1.5)

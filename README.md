# Spotify to YouTube Music Downloader

A Python script that allows you to download songs from YouTube based on a Spotify playlist. The script maintains metadata and album art from Spotify while downloading the audio from YouTube.

## Features

- Download songs from YouTube using Spotify playlist links
- Preserve song metadata (artist, album, title)
- Embed album art from Spotify
- Automatic YouTube search and download
- Progress tracking during downloads

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Spotify Developer Account

## Installation

1. Clone or download this repository to your local machine

2. Set up Spotify API credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Log in with your Spotify account
   - Click "Create App"
   - Fill in the app details (name and description)
   - Accept the terms and conditions
   - Once created, you'll see your Client ID and Client Secret
   - Click "Edit Settings"
   - Add `http://localhost:8888/callback` to the Redirect URIs
   - Save the changes

3. Create a `.env` file in the root directory:
   ```bash
   # Copy the sample file
   cp .env.sample .env
   ```
   Then edit the `.env` file and add your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python soptify.py
   ```

2. When prompted, enter your Spotify playlist URL
   - The URL should be in the format: `https://open.spotify.com/playlist/...`

3. The script will:
   - Fetch all tracks from your Spotify playlist
   - Search for each song on YouTube
   - Download the audio
   - Embed metadata and album art
   - Save the files in a `music` folder

## Output

- Downloaded songs will be saved in the `./music/` directory
- Files are saved in M4A format with embedded metadata and album art
- Progress is shown in the terminal during download

## Note

This tool is for personal use only. Please respect copyright laws and terms of service of both Spotify and YouTube.

## Dependencies

- pytubefix: YouTube video downloading
- python-dotenv: Environment variable management
- mutagen: Audio metadata handling
- requests: HTTP requests for album art 
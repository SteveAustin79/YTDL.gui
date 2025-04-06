# YTDL - YouTube Downloader 1.0
Download one, multiple or all videos from a specific YouTube channel in any available resolution as mp4.

Restricted video download possible, but requires authentication via accounts.google.com/device.

### Features
- channel config file with default filters
- filters:
    - max resolution
    - min_duration_in_minutes
    - max_duration_in_minutes
    - minimum_year
    - maximum_year
    - skip_restricted
    - only_restricted
    - minimum_views
    - year_subfolders
    - exclude_video_ids
    - include_video_ids
    - filter_words
- channels.txt: YouTube Channels list
- video resolutions > 1080p only provided as webm by YouTube -> converted to mp4 after downloading
- auto download highest available resolution (can be limited)
- skipping already downloaded videos

### History
- 20250404 - v1.0 - Initial version

## Disclaimer
- this app is meant only for non-copyright/non-protected videos, or for backup purposes

## Prerequisites
- Git (https://git-scm.com/downloads)
- Python (https://www.python.org)
- FFMPG (https://ffmpeg.org)
- NodeJS (https://nodejs.org)

## Installation (Linux)
1. Clone repository:
```diff
git clone https://github.com/SteveAustin79/YTDL.gui.git
```
2. Change directory
```diff
cd YTDL.gui
```
3. Install python environment
```diff
python3 -m venv venv
venv/scripts/activate
```
4. Install dependencies
```diff
sudo apt-get install python3-tk (Windows: pip install tk)
```
```diff
sudo venv/bin/python3 -m pip install pytubefix ffmpeg-python customtkinter pillow requests
```
5. Create and modify config.json
```diff
cp config.example.json config.json
nano config.json
```
6. Add channel URLs to channels.txt (optional)
```diff
nano channels.txt
```
7. Run the application
```diff
venv/bin/python3 main.py
```

## Update
```diff
git pull https://github.com/SteveAustin79/YTDL.gui.git
```

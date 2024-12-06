# Video Downloader

A simple GUI application for downloading videos and audio from various platforms including YouTube, Vimeo, Facebook, Instagram, and TikTok.

## Features

- Support for multiple video platforms
- Download options for video quality and format
- Playlist support with item limits
- Progress tracking
- Custom save location
- Status updates and error reporting

## Requirements

- Python 3.6 or higher
- FFmpeg (required for audio/video processing)
- Required packages listed in requirements.txt

## Installation

1. Clone or download this repository
2. Install FFmpeg:
   - Windows: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add to PATH
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`
3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python video_downloader.py
```

1. Enter the URL of the video/audio you want to download
2. Select the platform (or leave as Auto Detect)
3. Choose your download options:
   - Media limit for playlists
   - Format and quality
   - Save location
4. Click "Start Download"

## Supported Formats

- Best Quality (Video + Audio)
- Video Only (Best Quality)
- Audio Only (Best Quality)
- Compressed (480p)
- Mobile Quality (360p)

## Notes

- Download speed depends on your internet connection
- Some platforms may have restrictions on downloads
- Always respect copyright and terms of service of the platforms

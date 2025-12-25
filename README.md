# Project Seadog

Seadog is a desktop GUI application for downloading music and videos  
from YouTube using yt-dlp.

## **Important:** Playlist downloads may temporarily fail due to YouTube changes.

SeaDog relies on yt-dlp for downloading content.

From time to time, YouTube makes server-side changes that can temporarily break playlist access — even when playlists still exist and work in a browser.

What to do?

- Try again later — these issues are often resolved upstream
- Test the URL directly with yt-dlp to confirm
- For some playlists (unlisted, YouTube Music, account-restricted), browser cookies may be required

SeaDog will continue to work once yt-dlp regains access.

## Latest Release
**v0.2.1** – Just added an app icon 
[Download](https://github.com/earache757/seadog/releases)

## Features

- Music downloads (MP3)
- Video downloads
- Playlist support
- Optional Kid3 integration
- Optional Gotify notifications
- Dark mode UI
- No terminal required

## Installation (Linux)

Download the latest binary from **GitHub Releases**.

### To run

```bash
chmod +x seadog-v0.2.0-linux-x86_64
./seadog-v0.2.0-linux-x86_64
```
## Upcoming Features

- A much improved UI (I know, it's ugly right now, but it works!)
- Configurable delay between playlist items
- YouTube and YouTube Music playlist monitoring
- Windows build
- Additional user-configurable UI options
- Display cover art / posters during downloads

## Screenshots

### Music Downloader
![Music Tab](screenshots/musictab.png)

### Video Downloader
![Video Tab](screenshots/videotab.png)

### Settings
![Settings Tab](screenshots/settingstab.png)


### For Developers
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```



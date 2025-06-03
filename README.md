# project1_videodownloader_and_player

This is the repository for the Project I ET3290 at HUST, guided by Dr. Đặng Quang Hiếu.

## Overview

This application allows you to:
- Download videos using torrent hashes (integrated with qBittorrent)
- Play videos with a built-in player (using VLC)
- Manage your video library with a modern Qt-based interface
- Login or use as a guest

## Features

- Torrent-based video downloading (qBittorrent API)
- Video playback (VLC backend)
- User-friendly interface (PySide6/Qt)
- Dashboard and login system

## Requirements

- Python 3.11
- VLC media player (must be installed and accessible in your system PATH)
- qBittorrent (portable version included, or install separately)
- The following Python libraries (see `requirements.txt`):
  - PySide6
  - python-vlc
  - qbittorrent-api
  - requests
  - beautifulsoup4
  - lxml
  - sqlalchemy
  - certifi
  - charset-normalizer
  - idna
  - packaging
  - urllib3

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/project1_videodownloader_and_player.git
   cd project1_videodownloader_and_player
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install VLC and qBittorrent:**
   - [Download VLC](https://www.videolan.org/vlc/) and install it.
   - [Download qBittorrent](https://www.qbittorrent.org/download.php) or use the included portable version.

5. **Set up qBittorrent Web UI:**
   To enable the Web UI in qBittorrent:
   1. Open qBittorrent.
   2. Go to **Tools > Options > Web UI**.
   3. Check the box for **Web User Interface (Remote Control)**.
   4. Set a username and password (default: `admin` / `adminadmin`).
   5. Ensure the Web UI is running on port `8080` (default).

   If qBittorrent stops unexpectedly, ensure it is not blocked by your firewall or antivirus software.

## Running the Application

1. **Start the app:**
   ```bash
   python main.py
   ```

2. **Login or use as guest.**
   - Use username: "admin", password: "password123" for test
3. **Use the dashboard to:**
   - Search and download videos via torrent hash
   - Play downloaded videos
   - Manage your video library

## Notes

- The default qBittorrent Web UI credentials are `admin` / `adminadmin`.
- Downloaded videos are saved to your default Downloads folder (can be changed in the app).
- If you encounter issues with VLC or qBittorrent, ensure they are installed and accessible in your system PATH.

## License

This project is for educational purposes.
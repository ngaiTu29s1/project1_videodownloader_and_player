import os
import sqlite3

DB_FOLDER = os.path.join("core", "db")
MOVIE_DB_FILE = os.path.join(DB_FOLDER, "movie.db")

def get_movies_page(page=0, page_size=3):
    conn = sqlite3.connect(MOVIE_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies ORDER BY id LIMIT ? OFFSET ?", (page_size, page * page_size))
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    # Convert to list of dicts
    return [dict(zip(columns, row)) for row in rows]

class DashboardModel:
    def __init__(self):
        self.data = {}

    def load_data(self):
        """
        Optionally, you can use this to load a welcome message or other static info.
        """
        self.data = {"welcomeMessage": "Search here"}
        return self.data

class PlayerModel:
    def __init__(self):
        self.video_files = []

    def load_videos_from_folder(self, folder_path):
        """Recursively load video files from the specified folder and subfolders"""
        self.video_files = []
        if not folder_path:
            return []

        video_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith((".mp4", ".avi", ".mkv")):
                    full_path = os.path.join(root, file)
                    video_files.append((file, full_path))
        self.video_files = video_files
        return video_files

    def get_video_path(self, index):
        """Get the full path of a video by index"""
        if 0 <= index < len(self.video_files):
            return self.video_files[index][1]
        return None
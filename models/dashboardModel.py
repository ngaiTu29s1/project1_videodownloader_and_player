import requests
import os
from core.constants import OMDB_API_KEY, OMDB_API_URL, OMDB_SEARCH_TERM

class DashboardModel:
    def __init__(self):
        self.data = {}

    def load_data(self):
        """
        Load movies from the OMDb API using the provided API key.
        This example uses a fixed search term "movie" and returns the first three results.
        """
        api_key =  OMDB_API_KEY
        url = f"{OMDB_API_URL}?s={OMDB_SEARCH_TERM}&apikey={api_key}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            movies_data = data.get("Search", [])[:3]
            updated_movies = []
            for movie in movies_data:
                title = movie.get("Title", "Unknown Title")
                poster = movie.get("Poster", "N/A")
                updated_movies.append({"Title": title, "Poster": poster})
                # In DashboardModel.load_data()
                print("Fetched movies:", updated_movies)
            self.data = {"movies": updated_movies, "welcomeMessage": "Search here"}
        except Exception as e:
            print(f"Error fetching movies from OMDb API: {e}")
            self.data = {"movies": [], "welcomeMessage": "Error loading movies"}
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
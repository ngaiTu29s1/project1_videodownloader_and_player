import requests
import os

class DashboardModel:
    def __init__(self):
        self.data = {}

    def load_data(self):
        """
        Load movies from the OMDb API using the provided API key.
        This example uses a fixed search term "movie" and returns the first three results.
        """
        api_key = "124d5c6f"  # Replace with your actual OMDb API key
        url = f"http://www.omdbapi.com/?s=movie&apikey={api_key}"
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
        """Load video files from the specified folder"""
        self.video_files = []
        if not folder_path:
            return []
            
        video_files = []
        for file in os.listdir(folder_path):
            if file.lower().endswith((".mp4", ".avi", ".mkv")):
                full_path = os.path.join(folder_path, file)
                video_files.append((file, full_path))
        
        self.video_files = video_files
        return video_files
    
    def get_video_path(self, index):
        """Get the full path of a video by index"""
        if 0 <= index < len(self.video_files):
            return self.video_files[index][1]
        return None
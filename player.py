import os
import tkinter as tk
from tkinter import filedialog
import vlc

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")

        self.video_listbox = tk.Listbox(self.root, height=15, width=50)
        self.video_listbox.pack(pady=10)

        browse_button = tk.Button(self.root, text="Browse Folder", command=self.browse_folder)
        browse_button.pack()

        play_button = tk.Button(self.root, text="Play Video", command=self.play_video)
        play_button.pack()

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.load_videos(folder_path)

    def load_videos(self, folder_path):
        self.video_listbox.delete(0, tk.END)
        self.video_files = []
        for file in os.listdir(folder_path):
            if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                self.video_files.append(os.path.join(folder_path, file))
                self.video_listbox.insert(tk.END, file)

    def play_video(self):
        selected_index = self.video_listbox.curselection()
        if selected_index:
            video_path = self.video_files[selected_index[0]]
            self.play_video_file(video_path)

    def play_video_file(self, video_path):
        media = self.instance.media_new(video_path)
        self.player.set_media(media)

        # Create a new window for VLC video output
        self.vlc_player = vlc.MediaPlayer()
        self.vlc_player.set_media(media)

        # Get the window ID where to render VLC's video output
        win_id = self.root.winfo_id()
        self.vlc_player.set_hwnd(win_id)
        self.vlc_player.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()

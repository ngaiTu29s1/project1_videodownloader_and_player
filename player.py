import vlc
import tkinter as tk
from tkinter import filedialog
import os

class VLCPlayer:
    def __init__(self, video_path, on_exit=None):
        self.root = tk.Tk()
        self.root.title("VLC Media Player")
        self.root.geometry("800x600")
        self.on_exit = on_exit

        # Initialize VLC
        self.instance = vlc.Instance('--vout=opengl', '--video-on-top')
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(video_path)
        self.player.set_media(self.media)
        self.is_embedded = True

        # Create GUI
        self.create_gui()

        # Start playing
        self.player.play()
        self.play_button.config(text="Pause")
        self.root.title(f"VLC Media Player - {os.path.basename(video_path)}")

        # Update seek bar
        self.root.after(1000, self.update_seek_bar)

        # Đảm bảo khi đóng cửa sổ sẽ dừng player
        self.root.protocol("WM_DELETE_WINDOW", self.exit_player)

        self.root.mainloop()

    def create_gui(self):
        # Video frame
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.root.update()
        self.player.set_hwnd(self.video_frame.winfo_id())

        # Control frame
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, pady=5)

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.seek_scale = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.seek)
        self.seek_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.volume_label = tk.Label(self.control_frame, text="Volume:")
        self.volume_label.pack(side=tk.LEFT)
        self.volume_scale = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        self.rewind_button = tk.Button(self.control_frame, text="<< -10s", command=self.rewind)
        self.rewind_button.pack(side=tk.LEFT, padx=5)
        self.forward_button = tk.Button(self.control_frame, text="+10s >>", command=self.forward)
        self.forward_button.pack(side=tk.LEFT, padx=5)

        self.fullscreen_button = tk.Button(self.control_frame, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.LEFT, padx=5)

        # Exit button
        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.exit_player)
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.play_button.config(text="Play")
        else:
            self.player.play()
            self.play_button.config(text="Pause")

    def seek(self, value):
        if self.media:
            self.player.set_position(float(value) / 100.0)

    def set_volume(self, value):
        self.player.audio_set_volume(int(value))

    def rewind(self):
        if self.media:
            current_time = self.player.get_time()
            self.player.set_time(max(0, current_time - 10000))

    def forward(self):
        if self.media:
            current_time = self.player.get_time()
            duration = self.player.get_length()
            self.player.set_time(min(duration, current_time + 10000))

    def toggle_fullscreen(self):
        if self.player.get_fullscreen() or self.root.attributes('-fullscreen'):
            self.player.set_fullscreen(False)
            self.root.attributes('-fullscreen', False)
            self.is_embedded = True
            self.video_frame.pack(fill=tk.BOTH, expand=True)
            self.control_frame.pack(fill=tk.X, pady=5)
            self.player.set_hwnd(self.video_frame.winfo_id())
            self.fullscreen_button.config(text="Fullscreen")
        else:
            self.is_embedded = False
            self.player.set_hwnd(0)
            self.video_frame.pack_forget()
            self.control_frame.pack_forget()
            self.root.attributes('-fullscreen', True)
            self.player.toggle_fullscreen()
            self.fullscreen_button.config(text="Exit Fullscreen")

    def update_seek_bar(self):
        if self.player.is_playing():
            pos = self.player.get_position() * 100
            self.seek_scale.set(pos)
        self.root.after(1000, self.update_seek_bar)

    def exit_player(self):
        self.player.stop()
        self.root.destroy()
        if self.on_exit:
            self.on_exit()
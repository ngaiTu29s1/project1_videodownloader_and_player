from PySide6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QProgressDialog, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, QEvent, QObject
from models.dashboardModel import DashboardModel, PlayerModel
from views.py.mainDashboardView import DashboardWindow, PlayerView
from qbit import start_qbittorrent, add_torrent_by_hash, stop_qbittorrent, DEFAULT_DOWNLOAD_LOCATION
import qbittorrentapi
import requests
import vlc
import sys


class DashboardController(QObject):
    def __init__(self):
        super().__init__()  # Required for QObject
        self.model = DashboardModel()
        self.view = DashboardWindow()
        self.ui = self.view.ui
        self.qb_process = None  # Process for qBittorrent
        self.timer = None       # QTimer for updating torrent status
        self.status_dialog = None
        
        # Initialize the player controller with the playerWidget from our view
        self.player_controller = PlayerController(self.ui.playerWidget)
        
        self.initialize()
        # Install event filter to lower the popup when main window is activated
        self.view.installEventFilter(self)

    def initialize(self):
        # Load initial data from the model
        data = self.model.load_data()
        self.ui.searchbarLE.setPlaceholderText(data.get("welcomeMessage", ""))
        # Connect the download button to the download logic
        self.ui.downloadButton.clicked.connect(self.handle_download)
        # Display initial movies from the model (if any)
        self.display_movies(data.get("movies", []))

    def display_movies(self, movies):
        widgets = [
            self.ui.movieCardWidget_1,
            self.ui.movieCardWidget_2,
            self.ui.movieCardWidget_3,
        ]
        print("Displaying movies:", movies)
        for widget in widgets:
            # Clear the layout if any
            layout = widget.layout()
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            else:
                widget.setLayout(QVBoxLayout())
        for movie, widget in zip(movies, widgets):
            layout = widget.layout()
            # Add movie title
            title_label = QLabel(movie.get("Title", "Unknown Title"))
            layout.addWidget(title_label)
            # Add poster if available
            poster_url = movie.get("Poster")
            if poster_url and poster_url != "N/A":
                try:
                    response = requests.get(poster_url)
                    response.raise_for_status()
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    poster_label = QLabel()
                    poster_label.setPixmap(pixmap.scaled(120, 180, Qt.KeepAspectRatio))
                    layout.addWidget(poster_label)
                except Exception as e:
                    print(f"Error fetching poster for {movie.get('Title')}: {e}")

    def handle_download(self):
        """
        Handle the download button click event.
        """
        hash_info = self.ui.hashInputLE.text().strip()
        if not hash_info:
            QMessageBox.warning(self.view, "Error", "Please enter a valid torrent hash.")
            return

        try:
            # Start qBittorrent if not running
            if not self.qb_process:
                self.qb_process = start_qbittorrent()

            # Connect to qBittorrent Web API
            qb = qbittorrentapi.Client(host="localhost", port=8080, username="admin", password="adminadmin")
            qb.auth_log_in()

            # Add torrent by hash
            add_torrent_by_hash(qb, hash_info, DEFAULT_DOWNLOAD_LOCATION)

            QMessageBox.information(self.view, "Success", f"Torrent with hash {hash_info} added successfully!")

            # Show status popup using QProgressDialog (non-modal)
            self.status_dialog = QProgressDialog("Waiting for torrent status...", "Cancel", 0, 100, self.view)
            self.status_dialog.setWindowModality(Qt.NonModal)  # Allow interaction with the main window
            self.status_dialog.setWindowTitle("qBittorrent Status")
            # Connect the cancel signal so user can cancel download
            self.status_dialog.canceled.connect(self.cancel_download)
            self.status_dialog.show()

            # Start QTimer to update torrent status every 2 seconds
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self.update_torrent_status(qb, hash_info))
            self.timer.start(2000)
        except qbittorrentapi.LoginFailed as e:
            QMessageBox.critical(self.view, "Login Failed", f"Failed to connect to qBittorrent: {e}")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"An error occurred: {e}")

    def update_torrent_status(self, qb, hash_info):
        """
        Query the torrent progress and update the progress dialog with detailed info.
        """
        try:
            torrents = qb.torrents_info(torrent_hashes=hash_info)
            if torrents:
                torrent = torrents[0]
                progress_value = int(torrent.progress * 100)
                details = (
                    f"Name: {torrent.name}\n"
                    f"Progress: {progress_value}%\n"
                    f"State: {torrent.state}\n"
                    f"Download Speed: {torrent.dlspeed / 1024:.2f} KB/s\n"
                    f"Upload Speed: {torrent.upspeed / 1024:.2f} KB/s\n"
                    f"ETA: {torrent.eta if hasattr(torrent, 'eta') else 'N/A'}"
                )
                self.status_dialog.setValue(progress_value)
                self.status_dialog.setLabelText(details)
                # If torrent is completed or in a state indicating completion, stop the timer
                if progress_value >= 100 or torrent.state in ['completed', 'uploading', 'stalledUP']:
                    self.timer.stop()
                    self.status_dialog.setValue(100)
                    QMessageBox.information(self.view, "Download Complete", f"Torrent {torrent.name} completed.")
            else:
                self.status_dialog.setLabelText("Torrent not found. Retrying...")
        except Exception as e:
            print(f"Error updating torrent status: {e}")

    def cancel_download(self):
        """
        Called when the user clicks the Cancel button on the progress dialog.
        Stops the timer and terminates the qBittorrent process.
        """
        if self.timer:
            self.timer.stop()
        if self.qb_process:
            stop_qbittorrent(self.qb_process)
            self.qb_process = None
        QMessageBox.information(self.view, "Download Canceled", "All downloads have been canceled.")
        self.status_dialog.close()

    def eventFilter(self, obj, event):
        """
        When the main dashboard is activated, lower the progress dialog so it goes into the background.
        """
        if obj == self.view and event.type() == QEvent.WindowActivate:
            if self.status_dialog is not None:
                self.status_dialog.lower()
            return False
        return super().eventFilter(obj, event)

    def show_dashboard(self):
        """
        Show the dashboard window.
        """
        self.view.show()
        self.view.raise_()

    def __del__(self):
        """
        Ensure that qBittorrent is stopped when the controller is deleted.
        """
        if self.qb_process:
            stop_qbittorrent(self.qb_process)

class PlayerController:
    def __init__(self, view):
        self.view = view  # PlayerView instance
        self.model = PlayerModel()
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Connect signals from view to handler methods
        self.view.browse_clicked.connect(self.handle_browse)
        self.view.video_selected.connect(self.handle_video_selected)
        self.view.fullscreen_clicked.connect(self.toggle_fullscreen)
        self.view.skip_forward_clicked.connect(self.skip_forward)
        self.view.skip_backward_clicked.connect(self.skip_backward)
        self.view.volume_changed.connect(self.set_volume)

    def handle_browse(self):
        default_folder = "D:/Phim"  # Set your default folder here
        folder_path = QFileDialog.getExistingDirectory(self.view, "Select Folder", default_folder)
        if folder_path:
            videos = self.model.load_videos_from_folder(folder_path)
            self.view.update_video_list(videos)

    def handle_video_selected(self, index):
        video_path = self.model.get_video_path(index)
        if video_path:
            media = self.instance.media_new(video_path)
            self.player.set_media(media)
            # Set the video output window id
            if sys.platform.startswith('win'):
                self.player.set_hwnd(self.view.videoWidget.winId())
            else:
                self.player.set_xwindow(self.view.videoWidget.winId())
            self.player.play()

    def toggle_fullscreen(self):
        main_window = self.view.window()
        if main_window.isFullScreen():
            main_window.showNormal()
        else:
            main_window.showFullScreen()

    def skip_forward(self):
        current_time = self.player.get_time()
        self.player.set_time(current_time + 10000)  # 10 seconds

    def skip_backward(self):
        current_time = self.player.get_time()
        self.player.set_time(max(0, current_time - 10000))  # 10 seconds

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)
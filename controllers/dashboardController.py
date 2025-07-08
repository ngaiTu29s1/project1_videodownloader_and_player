from PySide6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QProgressDialog, QFileDialog, QWidget, QPushButton, QDialog, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, QEvent, QObject
from models.dashboardModel import DashboardModel, PlayerModel, get_movies_page, MOVIE_DB_FILE
from views.py.mainDashboardView import DashboardWindow
from qbit import start_qbittorrent, add_torrent_by_hash, stop_qbittorrent, DEFAULT_DOWNLOAD_LOCATION
import qbittorrentapi
import requests
import vlc
import sys
from player import VLCPlayer
import threading
from views.py.movieDetails import MovieDetailsDialog
import sqlite3


class DashboardController(QObject):
    def __init__(self):
        super().__init__()
        self.model = DashboardModel()
        self.view = DashboardWindow()
        self.ui = self.view.ui
        self.qb_process = None
        self.timer = None
        self.status_dialog = None
        self.search_mode = False
        self.search_text = ""

        self.player_controller = PlayerController(self.ui.playerWidget)

        # --- Pagination state ---
        self.current_page = 0
        self.page_size = 3

        # Connect pagination buttons
        self.ui.prevButton.clicked.connect(self.prev_page)
        self.ui.nextButton.clicked.connect(self.next_page)

        self.initialize()
        self.view.installEventFilter(self)

    def initialize(self):
        # Load initial data from the model (for welcome message, etc.)
        data = self.model.load_data()
        self.ui.searchbarLE.setPlaceholderText(data.get("welcomeMessage", ""))
        
        # Connect the search button to the search_movies method
        self.ui.searchButton.clicked.connect(self.search_movies)
        
        # Connect the download button
        self.ui.downloadButton.clicked.connect(self.handle_download)
        
        # Show the first page of movies from the database
        self.load_page()

    def next_page(self):
        self.current_page += 1
        if self.search_mode:
            self.search_movies()
        else:
            self.load_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            if self.search_mode:
                self.search_movies()
            else:
                self.load_page()

    def load_page(self):
        self.search_mode = False
        movies = get_movies_page(self.current_page, self.page_size)
        self.display_movies(movies)
        self.update_page_label()

    def display_movies(self, movies):
        """
        Display a list of movies in the 3 slots on the dashboard.
        """
        # Widgets for the 3 slots
        widgets = [
            self.ui.movieCardWidget_1,
            self.ui.movieCardWidget_2,
            self.ui.movieCardWidget_3,
        ]
        
        # Clear existing content in the movie card widgets
        for widget in widgets:
            layout = widget.layout()
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            else:
                widget.setLayout(QVBoxLayout())
        
        # Populate the widgets with movie data
        for movie, widget in zip(movies, widgets):
            layout = widget.layout()
            
            # Movie title (bold, centered)
            title_label = QLabel(movie.get("title", "Unknown Title"))
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #FFD700;")
            layout.addWidget(title_label)
            
            # Poster
            poster_url = movie.get("poster")
            if poster_url and poster_url != "N/A":
                try:
                    response = requests.get(poster_url)
                    response.raise_for_status()
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    poster_label = QLabel()
                    poster_label.setPixmap(pixmap.scaled(120, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    poster_label.setAlignment(Qt.AlignCenter)
                    layout.addWidget(poster_label)
                except Exception as e:
                    print(f"Error fetching poster for {movie.get('title')}: {e}")
            
            # "View More" button
            view_more_btn = QPushButton("View More")
            view_more_btn.setStyleSheet("background-color: #444; color: white; border-radius: 8px; padding: 6px;")
            view_more_btn.clicked.connect(lambda checked, m=movie: self.show_movie_details(m))
            layout.addWidget(view_more_btn, alignment=Qt.AlignCenter)
            
    
    def show_movie_details(self, movie):
        """
        Show detailed information about the selected movie.
        """
        dialog = MovieDetailsDialog(movie, self.view)
        dialog.exec()
    
    def update_page_label(self):
        conn = sqlite3.connect(MOVIE_DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM movies")
        total_movies = cursor.fetchone()[0]
        conn.close()
        total_pages = max(1, (total_movies + self.page_size - 1) // self.page_size)
        self.ui.pageLabel.setText(f"Page {self.current_page + 1}/{total_pages}")
        self.ui.prevButton.setEnabled(self.current_page > 0)
        self.ui.nextButton.setEnabled(self.current_page < total_pages - 1)

    def update_search_page_label(self, search_text):
        # Đếm tổng số phim khớp search
        conn = sqlite3.connect(MOVIE_DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM movies WHERE title LIKE ?", (f"%{search_text}%",))
        total_movies = cursor.fetchone()[0]
        conn.close()
        total_pages = max(1, (total_movies + self.page_size - 1) // self.page_size)
        self.ui.pageLabel.setText(f"Search '{search_text}': Page {self.current_page + 1}/{total_pages}")
        self.ui.prevButton.setEnabled(self.current_page > 0)
        self.ui.nextButton.setEnabled(self.current_page < total_pages - 1)

    def load_page(self):
        movies = get_movies_page(self.current_page, self.page_size)
        self.display_movies(movies)
        self.update_page_label()

    def search_movies(self):
        """
        Search for movies in the database that contain the search string.
        Display the results in the 3 slots on the dashboard.
        """
        search_text = self.ui.searchbarLE.text().strip()
        if not search_text:
            # Nếu rỗng, hiển thị tất cả phim với phân trang như mặc định
            self.current_page = 0
            self.load_page()
            self.search_mode = False
            return

        # Query the database for movies containing the search string
        conn = sqlite3.connect(MOVIE_DB_FILE)
        cursor = conn.cursor()
        query = """
            SELECT title, poster, year, genre, director, actors, plot, imdb_rating
            FROM movies
            WHERE title LIKE ?
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (f"%{search_text}%", self.page_size, self.current_page * self.page_size))
        movies = cursor.fetchall()
        conn.close()

        # Convert the result into a list of dictionaries
        movie_list = [
            {
                "title": row[0],
                "poster": row[1],
                "year": row[2],
                "genre": row[3],
                "director": row[4],
                "actors": row[5],
                "plot": row[6],
                "imdb_rating": row[7],
            }
            for row in movies
        ]

        # Lưu trạng thái search
        self.search_mode = True
        self.search_text = search_text
        self.display_movies(movie_list)
        self.update_search_page_label(search_text)

        # Display the search results in the 3 slots
        self.display_movies(movie_list)
        self.ui.pageLabel.setText(f"Search Results for '{search_text}'")
        

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
                    f"ETA: {(torrent.eta//60) if hasattr(torrent, 'eta') and torrent.eta > 0 else 'N/A'} m"
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
        self.is_fullscreen = False

        # Connect signals from view to handler methods
        self.view.browse_clicked.connect(self.handle_browse)
        self.view.video_selected.connect(self.handle_video_selected)

    def handle_browse(self):
        default_folder = "D:/Phim"  # Set your default folder here
        folder_path = QFileDialog.getExistingDirectory(self.view, "Select Folder", default_folder)
        if folder_path:
            videos = self.model.load_videos_from_folder(folder_path)
            self.view.update_video_list(videos)

    def handle_video_selected(self, index):
        video_path = self.model.get_video_path(index)
        if video_path:
            # Mở player ở thread mới để không block giao diện Qt
            threading.Thread(target=VLCPlayer, args=(video_path,), daemon=True).start()

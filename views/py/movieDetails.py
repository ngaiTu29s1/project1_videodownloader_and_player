from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton
from PySide6.QtGui import QPixmap
import requests
import webbrowser

class MovieDetailsDialog(QDialog):
    def __init__(self, movie, parent=None):
        super().__init__(parent)
        self.setWindowTitle(movie.get("title", "Movie Details"))
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        # Poster and title
        top_layout = QHBoxLayout()
        poster_url = movie.get("poster")
        if poster_url and poster_url != "N/A":
            try:
                response = requests.get(poster_url)
                response.raise_for_status()
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                poster_label = QLabel()
                poster_label.setPixmap(pixmap.scaled(150, 220))
                top_layout.addWidget(poster_label)
            except Exception as e:
                print(f"Error loading poster: {e}")

        title_label = QLabel(f"<b>{movie.get('title', 'Unknown Title')}</b>")
        title_label.setWordWrap(True)
        top_layout.addWidget(title_label)
        layout.addLayout(top_layout)

        # Year and other main info
        year = movie.get("year", "Unknown Year")
        layout.addWidget(QLabel(f"Year: {year}"))

        # All details (except poster)
        details = ""
        for key, value in movie.items():
            if key != "poster":
                details += f"<b>{key}:</b> {value}<br>"
        details_label = QLabel(details)
        details_label.setWordWrap(True)
        layout.addWidget(details_label)

        search_button = QPushButton("Search on ThePirateBay")
        search_button.clicked.connect(lambda: self.search_on_tpb(movie.get("title", "")))
        layout.addWidget(search_button)

    def search_on_tpb(self, title):
        if title:
            url = f"https://thepiratebay.org/search/{title.replace(' ', '%20')}/1/99/0"
            webbrowser.open(url)
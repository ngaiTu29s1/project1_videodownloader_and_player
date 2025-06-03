from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests
import webbrowser

class MovieDetailsDialog(QDialog):
    def __init__(self, movie, parent=None):
        super().__init__(parent)
        self.setWindowTitle(movie.get("title", "Movie Details"))
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)

        # Poster and title
        top_layout = QHBoxLayout()
        poster_url = movie.get("poster")
        poster_label = QLabel()
        poster_label.setFixedSize(150, 220)
        poster_label.setStyleSheet("border: 1px solid #444; background: #222;")
        if poster_url and poster_url != "N/A":
            try:
                response = requests.get(poster_url)
                response.raise_for_status()
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                poster_label.setPixmap(pixmap.scaled(150, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except Exception as e:
                poster_label.setText("No Image")
        top_layout.addWidget(poster_label)

        title_label = QLabel(f"<b>{movie.get('title', 'Unknown Title')}</b>")
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFD700;")
        top_layout.addWidget(title_label)
        layout.addLayout(top_layout)

        # Year and other main info
        year = movie.get("year", "Unknown Year")
        year_label = QLabel(f"Year: {year}")
        year_label.setStyleSheet("font-size: 14px; color: #AAA;")
        layout.addWidget(year_label)

        # Scrollable details
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details = ""
        for key, value in movie.items():
            if key not in ("poster", "title", "year"):
                details += f"<b>{key.capitalize()}:</b> {value}<br>"
        details_label = QLabel(details)
        details_label.setWordWrap(True)
        details_label.setStyleSheet("font-size: 13px; color: #DDD;")
        details_layout.addWidget(details_label)
        scroll.setWidget(details_widget)
        layout.addWidget(scroll)

        # Search button
        search_button = QPushButton("Search on ThePirateBay")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #0057b8; color: white; border-radius: 8px; padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFD700; color: #222;
            }
        """)
        search_button.clicked.connect(lambda: self.search_on_tpb(movie.get("title", "")))
        layout.addWidget(search_button, alignment=Qt.AlignCenter)

    def search_on_tpb(self, title):
        if title:
            url = f"https://thepiratebay.org/search/{title.replace(' ', '%20')}/1/99/0"
            webbrowser.open(url)
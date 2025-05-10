from PySide6.QtCore import QCoreApplication, QMetaObject, Signal, Qt

from PySide6.QtWidgets import (QGridLayout, QLineEdit, QMainWindow, QMenuBar, QPushButton,
                               QStatusBar, QTabWidget, QWidget, QVBoxLayout
                               , QHBoxLayout, QSizePolicy, QListWidget, QWidget
                               , QSlider, QVBoxLayout, QPushButton, QListWidget)

from core.constants import WINDOW_HEIGHT, WINDOW_WIDTH

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(571, 512)
        
        # Central widget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create a main tab widget
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(0, 0, 571, 451)
        
        # ----- Dashboard Tab -----
        self.DashboardTab = QWidget()
        self.DashboardTab.setObjectName("DashboardTab")
        
        # Set a vertical layout for DashboardTab
        self.dashboardLayout = QVBoxLayout(self.DashboardTab)
        self.dashboardLayout.setContentsMargins(10, 10, 10, 10)
        self.dashboardLayout.setSpacing(10)
        
        # Top controls: Search bar and download controls in a horizontal layout
        self.topControls = QHBoxLayout()
        self.searchbarLE = QLineEdit()
        self.searchbarLE.setObjectName("searchbarLE")
        self.searchbarLE.setPlaceholderText("Search here")
        self.searchButton = QPushButton()
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Search")
        self.hashInputLE = QLineEdit()
        self.hashInputLE.setObjectName("hashInputLE")
        self.hashInputLE.setPlaceholderText("Enter torrent hash info")
        self.downloadButton = QPushButton()
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.setText("Download")
        
        self.topControls.addWidget(self.searchbarLE)
        self.topControls.addWidget(self.searchButton)
        self.topControls.addWidget(self.hashInputLE)
        self.topControls.addWidget(self.downloadButton)
        self.dashboardLayout.addLayout(self.topControls)
        
        # Grid area for movie cards
        self.gridContainer = QWidget()
        self.gridContainer.setObjectName("gridContainer")
        self.gridLayout = QGridLayout(self.gridContainer)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(15)
        
        # Create three movie card widgets and ensure each gets its own layout
        self.movieCardWidget_1 = QWidget()
        self.movieCardWidget_1.setObjectName("movieCardWidget_1")
        self.movieCardWidget_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movieCardWidget_1.setLayout(QVBoxLayout())
        
        self.movieCardWidget_2 = QWidget()
        self.movieCardWidget_2.setObjectName("movieCardWidget_2")
        self.movieCardWidget_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movieCardWidget_2.setLayout(QVBoxLayout())
        
        self.movieCardWidget_3 = QWidget()
        self.movieCardWidget_3.setObjectName("movieCardWidget_3")
        self.movieCardWidget_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movieCardWidget_3.setLayout(QVBoxLayout())
        
        self.gridLayout.addWidget(self.movieCardWidget_1, 0, 0)
        self.gridLayout.addWidget(self.movieCardWidget_2, 0, 1)
        self.gridLayout.addWidget(self.movieCardWidget_3, 0, 2)
        
        self.dashboardLayout.addWidget(self.gridContainer)
        
        # Add the DashboardTab to the tab widget
        self.tabWidget.addTab(self.DashboardTab, "Dashboard")
        
        # ----- Player Tab -----
        self.PlayerTab = QWidget()
        self.PlayerTab.setObjectName("PlayerTab")
        # Create a vertical layout for PlayerTab and embed PlayerView (not PlayerWidget)
        self.playerLayout = QVBoxLayout(self.PlayerTab)
        self.playerWidget = PlayerView(self.PlayerTab)  # Changed from PlayerWidget to PlayerView
        self.playerLayout.addWidget(self.playerWidget)
        self.PlayerTab.setLayout(self.playerLayout)
        self.tabWidget.addTab(self.PlayerTab, "Player")
        
        # Set central widget and menu/status bars
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Ensure the central widget uses a layout
        layout = QVBoxLayout(self.ui.centralwidget)
        self.ui.centralwidget.setLayout(layout)
        layout.addWidget(self.ui.tabWidget)

class PlayerView(QWidget):
    # Define signals for controller to connect to
    browse_clicked = Signal()
    video_selected = Signal(int)

    # Controller functions
    fullscreen_clicked = Signal()
    skip_forward_clicked = Signal()
    skip_backward_clicked = Signal()
    volume_changed = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.videoWidget = QWidget(self)
        self.layout.addWidget(self.videoWidget, stretch=1)  # This makes videoWidget expand

        # Video widget where videos will be rendered
        self.videoWidget = QWidget(self)
        self.videoWidget.setMinimumHeight(300)
        self.layout.addWidget(self.videoWidget)

        # Browse button
        self.openButton = QPushButton("Browse Folder")
        self.openButton.clicked.connect(self.on_browse_clicked)
        self.layout.addWidget(self.openButton)

        # Video list
        self.videoList = QListWidget()
        self.videoList.itemDoubleClicked.connect(self.on_video_selected)
        self.layout.addWidget(self.videoList)
        
        self.fullscreenBtn = QPushButton("Full Screen")
        self.skipFwdBtn = QPushButton(">> 10s")
        self.skipBackBtn = QPushButton("<< 10s")
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)

        controls = QHBoxLayout()
        controls.addWidget(self.fullscreenBtn)
        controls.addWidget(self.skipBackBtn)
        controls.addWidget(self.skipFwdBtn)
        controls.addWidget(self.volumeSlider)
        self.layout.addLayout(controls)

        self.fullscreenBtn.clicked.connect(self.fullscreen_clicked)
        self.skipFwdBtn.clicked.connect(self.skip_forward_clicked)
        self.skipBackBtn.clicked.connect(self.skip_backward_clicked)
        self.volumeSlider.valueChanged.connect(self.volume_changed)

    def on_browse_clicked(self):
        """Emit signal when browse button is clicked"""
        self.browse_clicked.emit()
        
    def on_video_selected(self, item):
        """Emit signal with selected video index when a video is double-clicked"""
        index = self.videoList.row(item)
        self.video_selected.emit(index)
        
    def update_video_list(self, videos):
        """Update the list widget with video names"""
        self.videoList.clear()
        for video_name, _ in videos:
            self.videoList.addItem(video_name)

    def keyPressEvent(self, event):
        """Keyboard shortcuts for player controls."""
        if event.key() == Qt.Key_F:
            self.fullscreen_clicked.emit()
        elif event.key() == Qt.Key_Right:
            self.skip_forward_clicked.emit()
        elif event.key() == Qt.Key_Left:
            self.skip_backward_clicked.emit()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        """Mouse wheel to control volume."""
        delta = event.angleDelta().y() // 120  # 1 for each notch
        new_volume = self.volumeSlider.value() + delta * 5
        new_volume = max(0, min(100, new_volume))
        self.volumeSlider.setValue(new_volume)
        self.volume_changed.emit(new_volume)
        super().wheelEvent(event)

    def focusInEvent(self, event):
        """Ensure the widget receives key events when focused."""
        self.setFocus(Qt.ActiveWindowFocusReason)
        super().focusInEvent(event)
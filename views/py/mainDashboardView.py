from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QGridLayout, QLineEdit, QMainWindow, QMenuBar, QPushButton,
                               QStatusBar, QTabWidget, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy)

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
        
        # (Optional) Create a second (empty) tab
        self.PlayerTab = QWidget()
        self.PlayerTab.setObjectName("PlayerTab")
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
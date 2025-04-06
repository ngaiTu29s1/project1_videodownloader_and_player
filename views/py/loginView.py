# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginScreen.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,
    QPixmap, QPalette, QBrush)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

from core.constants import (WINDOW_HEIGHT, WINDOW_WIDTH, INPUT_WIDTH,
    LOGIN_BUTTON_HEIGHT, LOGIN_BUTTON_WIDTH, GUEST_BUTTON_HEIGHT, GUEST_BUTTON_WIDTH,
    FONT_SIZE_LABEL, FONT_FAMILY, LAYOUT_HORIZONTAL_SPACING)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(350, 250)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.usernameLE = QLineEdit(self.centralwidget)
        self.usernameLE.setObjectName(u"usernameLE")

        self.gridLayout.addWidget(self.usernameLE, 0, 1, 1, 2)

        self.passwordLE = QLineEdit(self.centralwidget)
        self.passwordLE.setObjectName(u"passwordLE")
        self.passwordLE.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.passwordLE, 1, 1, 1, 2)

        self.usenameLabel = QLabel(self.centralwidget)
        self.usenameLabel.setObjectName(u"usenameLabel")

        self.gridLayout.addWidget(self.usenameLabel, 0, 0, 1, 1)

        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")

        self.gridLayout.addWidget(self.loginButton, 2, 0, 1, 2)

        self.guestButton = QPushButton(self.centralwidget)
        self.guestButton.setObjectName(u"guestButton")

        self.gridLayout.addWidget(self.guestButton, 2, 2, 1, 1)

        self.passwordLabel = QLabel(self.centralwidget)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.gridLayout.addWidget(self.passwordLabel, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.usenameLabel.raise_()
        self.usernameLE.raise_()
        self.passwordLabel.raise_()
        self.passwordLE.raise_()
        self.guestButton.raise_()
        self.loginButton.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 545, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.usernameLE.setText("")
        self.usenameLabel.setText(QCoreApplication.translate("MainWindow", u"Username:", None))
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.guestButton.setText(QCoreApplication.translate("MainWindow", u"Use as guest", None))
        self.passwordLabel.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
    # retranslateUi

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Manual configuration
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("Login - TorrentStream")

        # Set background image using QPixmap
        background_pixmap = QPixmap("resources/login.jpg")
        scaled_pixmap = background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        palette = self.palette()
        palette.setBrush(self.backgroundRole(), QBrush(scaled_pixmap))
        self.setPalette(palette)

        # Label styling
        self.ui.gridLayout.setHorizontalSpacing(LAYOUT_HORIZONTAL_SPACING)
        label_font = QFont(FONT_FAMILY, FONT_SIZE_LABEL)
        self.ui.usenameLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ui.passwordLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ui.usenameLabel.setFont(label_font)
        self.ui.passwordLabel.setFont(label_font)

        # Input handling
        self.ui.usernameLE.setFixedWidth(INPUT_WIDTH)
        self.ui.passwordLE.setFixedWidth(INPUT_WIDTH)
        self.ui.usernameLE.returnPressed.connect(self.ui.passwordLE.setFocus)
        self.ui.passwordLE.returnPressed.connect(self.ui.loginButton.click)


        # Button sizing
        self.ui.loginButton.setFixedSize(LOGIN_BUTTON_WIDTH, LOGIN_BUTTON_HEIGHT)
        self.ui.guestButton.setFixedSize(GUEST_BUTTON_WIDTH, GUEST_BUTTON_HEIGHT)
        self.ui.gridLayout.setAlignment(self.ui.loginButton, Qt.AlignHCenter)
        self.ui.gridLayout.setAlignment(self.ui.guestButton, Qt.AlignHCenter)

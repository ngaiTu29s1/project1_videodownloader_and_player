import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Simple Window")
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        button = QPushButton("Click Me")
        layout.addWidget(button)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())

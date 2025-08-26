import sys
from PyQt6.QtWidgets import QApplication
from main_window import GPTClientUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPTClientUI()
    window.show()
    sys.exit(app.exec())

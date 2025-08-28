# src/janet_twin/__main__.py

def main():
    """
    Main entry point for the application.
    It initializes and runs the PyQt application.
    """
    import sys
    from .app import GPTClientUI
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GPTClientUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
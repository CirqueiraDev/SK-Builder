import sys, time
from PyQt5.QtWidgets import QApplication
from src.main_window import MainWindow
from src.pages.splash import SplashScreen

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    splash = SplashScreen()
    splash.start()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
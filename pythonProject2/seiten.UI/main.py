from PyQt5.QtWidgets import QApplication, QDialog
from loginpage import LoginRegisterPage
import sys
from fonctionalitee import VoyageApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterPage()
    window.show()
    sys.exit(app.exec_())

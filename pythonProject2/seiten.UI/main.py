import sys
from PyQt5.QtWidgets import QApplication
from loginpage import LoginRegisterPage


def main():

    app = QApplication(sys.argv)
    login_page = LoginRegisterPage()
    login_page.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

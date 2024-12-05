from PyQt5.QtWidgets import QMessageBox
import re
from PyQt5.QtGui import QPixmap

def resize_image(image_path, width, height):
    pixmap = QPixmap(image_path)
    return pixmap.scaled(width, height)

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def show_warning_message(title , message):
    warning_box = QMessageBox()
    warning_box.setWindowTitle(title)
    warning_box.setText(message)
    warning_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #ffe6e6;
                        border: 1px solid #ff4d4d;
                    }
                    QLabel {
                        font-size: 14px;
                        color: #cc0000;
                        font-weight: bold;
                    }
                    QPushButton {
                        background-color: #ff4d4d;
                        color: white;
                        padding: 8px;
                        border-radius: 5px;
                        width: 50px;
                    }
                    QPushButton:hover {
                        background-color: #cc0000;
                    }
                """)
    warning_box.exec_()

def show_success_message(title, message):
    success_box = QMessageBox()
    success_box.setWindowTitle(title)
    success_box.setText(message)
    success_box.setStyleSheet("""
                QMessageBox {
                    background-color: #e6ffed;
                    border: 1px solid #4CAF50;
                }
                QLabel {
                    font-size: 16px;
                    color: #2e7d32;
                    font-weight: bold;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
            """)
    success_box.exec_()

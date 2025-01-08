from PyQt5.QtWidgets import QMessageBox
import re


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
def is_valid_street(street):
    pattern = r"^[A-Za-z\s]+\s+\d+$"
    #\d repräsentiert jede beliebige Ziffer(0–9)
    #+ gibt an,  dass das Element einmal  oder mehrmals oder mehrmals
    return re.match(pattern, street) is not None

def is_valid_postcode(postcode):
    pattern = r"^[0-9]{5}$"
    return re.match(pattern, postcode) is not None

def is_valid_phone(phone):
    pattern = r"^(\+49|0)\s?[0-9]{9,}$"
    return re.match(pattern, phone) is not None
def is_valid_bank_details(bank_details):
    pattern = r"^[A-Z]{2}[0-9]{20}$"
    return re.match(pattern, bank_details) is not None
def is_valid_credit_card(credit_card):
    pattern = r"^\d{16}$"
    return re.match(pattern, credit_card) is not None

def is_valid_cvv(cvv):
    pattern =r"^\d{3}$"
    return re.match(pattern, cvv) is not None
def is_valid_city(city):
    pattern = r"^[a-zA-ZÀ-ÿ\s\-]+$"
    return re.match(pattern, city) is not None


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
def show_return_date_error(title, mess,info):
    message = QMessageBox()
    message.setIcon(QMessageBox.Warning)
    message.setWindowTitle(title)
    message.setText(mess)
    message.setInformativeText(info)
    message.setStyleSheet("""
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
    message.setStandardButtons(QMessageBox.Ok)
    message.accept()
    message.exec_()


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


def clear_layout(layout):
    """Löscht alle Widgets eines Layouts."""
    if layout is not None:
        while layout.count():  # Überprüft, ob er Widgets enthält
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    else:
        print("Layout is None, nothing to clear.")
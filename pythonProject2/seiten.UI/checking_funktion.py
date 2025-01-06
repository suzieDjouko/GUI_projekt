import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog
import re
from PyQt5.QtGui import QPixmap


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
def is_valid_street(street):
    pattern = r"^[A-Za-z\s]+\s+\d+$"
    #\d represente n'importe quel chiffre numerique
    #+indique que l'eliment peut apparaitre une ou plusieurs fois
    return re.match(pattern, street) is not None

def is_valid_postcode(postcode):
    pattern = r"^[0-9]{5}$"
    return re.match(pattern, postcode) is not None

def is_valid_phone(phone):
    pattern = r"^(\+49|0)\s?[0-9]{9,}$"
    return re.match(pattern, phone) is not None
def is_valid_bank_details(bank_details):
    #^DE[0-9]{20}$
    #pattern = r"^[A-Z]{2}[0-9]{2}[A-Za-z0-9\s\-]+$"
    pattern = r"^[A-Za-z0-9\s\-]+$"
    return re.match(pattern, bank_details) is not None
def is_valid_credit_card(credit_card):

    # Pattern pour les cartes Visa, MasterCard, American Express, Discover
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
    """   Zeigt eine Fehlermeldung an, wenn das Rückgabedatum inkompatibel ist.    """
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


def download_booking_file(self):
    """
    Ermöglicht dem Benutzer das Herunterladen der Buchungsdatei
    """
    try:
        # Path to the existing booking file
        file_path = "bookings.txt"

        # Check if the file exists
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Error", "The booking file does not exist.")
            return

        # Open a file dialog to select the download location
        save_path, _ = QFileDialog.getSaveFileName(self, "Save As", "booking.txt", "Text Files (*.txt)")

        # If a location is selected, copy the file
        if save_path:
            with open(file_path, "r") as original_file, open(save_path, "w") as new_file:
                new_file.write(original_file.read())

            QMessageBox.information(self, "Success", "The booking file has been downloaded successfully.")
    except Exception as e:
        QMessageBox.critical(self, "Error", f"An error occurred: {e}")

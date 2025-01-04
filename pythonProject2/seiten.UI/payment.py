from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QComboBox

from styles import *
from checking_funktion import *
class PurchaseDialog(QDialog):
    def __init__(self, trip_data, cabin_type, cabin_price, user_balance , user_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Purchase")
        self.resize(800, 600)


        self.trip_data = trip_data
        self.cabin_type = cabin_type
        self.cabin_price = cabin_price
        self.user_balance = user_balance
        self.user_name = user_name

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Zusammenfassung der Buchungsinformationen
        layout.addWidget(QLabel(f"<b>Trip Number:</b> {trip_data['Reisenummer']}"))
        layout.addWidget(QLabel(f"<b>Cabin Type:</b> {cabin_type}"))
        layout.addWidget(QLabel(f"<b>Price:</b> {int(cabin_price)} €"))
        #layout.addWidget(QLabel(f"<b>Remaining Balance:</b> {user_balance - cabin_price:} €"))
        layout.addWidget(QLabel(f"<b>Remaining Balance:</b> {int(user_balance - cabin_price)} €<br>"))


        # Felder für Benutzerdaten
        self.street_input = QLineEdit()
        self.street_input.setPlaceholderText("Enter your street")
        self.street_input.setStyleSheet(loginmainstyle)
        layout.addWidget(QLabel("Street and Number:"))
        layout.addWidget(self.street_input)

        self.postal_code_input = QLineEdit()
        self.postal_code_input.setPlaceholderText("Enter your postal code")
        self.postal_code_input.setStyleSheet(loginmainstyle)
        layout.addWidget(QLabel("Postal Code:"))
        layout.addWidget(self.postal_code_input)

        self.country_input = QLineEdit()
        self.country_input.setText("Germany")
        self.country_input.setStyleSheet(loginmainstyle)
        self.country_input.setReadOnly(True)
        layout.addWidget(QLabel("Country:"))
        layout.addWidget(self.country_input)

        self.phone_input = QLineEdit()
        self.phone_input.setStyleSheet(loginmainstyle)
        self.phone_input.setPlaceholderText("Enter your phone number")
        layout.addWidget(QLabel("Phone:"))
        layout.addWidget(self.phone_input)

        # Auswahl der Zahlungsmethode
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.setStyleSheet(style_box)
        self.payment_method_combo.addItems(["Bank Transfer", "Credit Card", "PayPal"])
        self.payment_method_combo.currentTextChanged.connect(self.update_payment_fields)
        layout.addWidget(QLabel("Payment Method:"))
        layout.addWidget(self.payment_method_combo)

        # Dynamische Felder für Zahlungsinformationen
        self.dynamic_payment_layout = QVBoxLayout()
        self.payment_input = QLineEdit()
        self.payment_input.setStyleSheet(loginmainstyle)
        self.payment_input.setPlaceholderText("Enter your bank details")
        self.dynamic_payment_layout.addWidget(QLabel("Bank Details:"))
        self.dynamic_payment_layout.addWidget(self.payment_input)

        self.card_number_input = QLineEdit()
        self.card_number_input.setStyleSheet(loginmainstyle)
        self.card_number_input.setPlaceholderText("Enter your card number")

        self.cvv_input = QLineEdit()
        self.cvv_input.setStyleSheet(loginmainstyle)
        self.cvv_input.setPlaceholderText("Enter your CVV")
        self.cvv_input.setMaxLength(3)

        self.paypal_email_input = QLineEdit()
        self.paypal_email_input.setPlaceholderText("Enter your PayPal email")

        layout.addLayout(self.dynamic_payment_layout)

        # Buttons, um den Kauf zu bestätigen oder abzubrechen
        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(cancelstyle)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setEnabled(False)
        self.confirm_button.setStyleSheet(confirmbtnstyledisable)
        self.confirm_button.clicked.connect(self.confirm_purchase)
        button_layout.addWidget(self.confirm_button)

        self.street_input.textChanged.connect(self.check_fields)
        self.postal_code_input.textChanged.connect(self.check_fields)
        self.phone_input.textChanged.connect(self.check_fields)
        self.payment_input.textChanged.connect(self.check_fields)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_payment_fields(self):
        """
        Aktualisiert die angezeigten Felder entsprechend der gewählten Zahlungsmethode.
        """
        method = self.payment_method_combo.currentText()

        # Dynamisches Layout löschen
        for i in reversed(range(self.dynamic_payment_layout.count())):
            widget = self.dynamic_payment_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        if method == "Bank Transfer":
            self.payment_input = QLineEdit()
            self.payment_input.setPlaceholderText("Enter your bank details")
            self.dynamic_payment_layout.addWidget(QLabel("Bank Details:"))
            self.dynamic_payment_layout.addWidget(self.payment_input)
        elif method == "Credit Card":
            self.card_number_input = QLineEdit()
            self.card_number_input.setPlaceholderText("Enter your card number")
            self.cvv_input = QLineEdit()
            self.cvv_input.setPlaceholderText("Enter your CVV")
            self.cvv_input.setMaxLength(3)
            self.dynamic_payment_layout.addWidget(QLabel("Card Number:"))
            self.dynamic_payment_layout.addWidget(self.card_number_input)
            self.dynamic_payment_layout.addWidget(QLabel("CVV:"))
            self.dynamic_payment_layout.addWidget(self.cvv_input)
        elif method == "PayPal":
            self.paypal_email_input = QLineEdit()
            self.paypal_email_input.setPlaceholderText("Enter your PayPal email")
            self.dynamic_payment_layout.addWidget(QLabel("PayPal Email:"))
            self.dynamic_payment_layout.addWidget(self.paypal_email_input)

        self.check_fields()

    def check_fields(self):
        """
        Überprüft, ob alle notwendigen Felder ausgefüllt und gültig sind, und aktiviert die Schaltfläche „Confirm“..
        """
        street_valid = is_valid_street(self.street_input.text().strip())
        postal_code_valid = is_valid_postcode(self.postal_code_input.text().strip())
        phone_valid = is_valid_phone(self.phone_input.text().strip())

        method = self.payment_method_combo.currentText()
        payment_valid = False

        if method == "Bank Transfer":
            payment_valid =is_valid_bank_details(self.payment_input.text().strip())
        elif method == "Credit Card":
            payment_valid = (
                is_valid_credit_card(self.card_number_input.text().strip())
                and is_valid_cvv(self.cvv_input.text().strip())
            )
        elif method == "PayPal":
            payment_valid = is_valid_email(self.paypal_email_input.text().strip())

        if street_valid and postal_code_valid and phone_valid and self.payment_input.text().strip():
            if payment_valid:
                self.confirm_button.setEnabled(True)
        else:
            self.confirm_button.setEnabled(False)

    def confirm_purchase(self):
        #strip entfernt einseitige Ausdrücke am Anfang und am Ende
        street = self.street_input.text().strip()
        postal_code = self.postal_code_input.text().strip()
        phone = self.phone_input.text().strip()
        bank_details = self.payment_method_combo.currentText()

        with open("bookings.txt", "a") as file:
            file.write(f"Name: {self.user_name}\n")
            file.write(f"Trip Number: {self.trip_data['Reisenummer']}\n")
            file.write(f"Cabin Type: {self.cabin_type}\n")
            file.write(f"Price: {self.cabin_price:} €\n")
            file.write(f"Address: {street}, {postal_code}, Germany\n")
            file.write(f"Phone: {phone}\n")
            file.write(f"Bank Details: {bank_details}\n")
            file.write("-" * 50 + "\n")
        QMessageBox.information(self, "Purchase Successful", "Your booking has been confirmed!")

        # Schließen Sie den Dialog erfolgreich ab
        self.accept()

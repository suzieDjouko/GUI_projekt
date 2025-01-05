from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtWidgets import QLabel
from styles import *
from checking_funktion import *



class PaymentPage(QWidget):
    def __init__(self, trip_data, cabin_type, cabin_price, user_balance, user_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Purchase")
        self.resize(800, 600)
        #self.confirm_button = None


        # Initialisation des données
        self.trip_data = trip_data
        self.cabin_type = cabin_type
        self.cabin_price = cabin_price
        self.user_balance = user_balance
        self.user_name = user_name

        # Création du layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Résumé des informations
        layout.addWidget(QLabel(f"<b>Trip Number:</b> {trip_data['Reisenummer']}"))
        layout.addWidget(QLabel(f"<b>Cabin Type:</b> {cabin_type}"))
        layout.addWidget(QLabel(f"<b>Price:</b> {int(cabin_price)} €"))
        layout.addWidget(QLabel(f"<b>Remaining Balance:</b> {int(user_balance - cabin_price)} €"))

        # Champs pour les données utilisateur
        self.street_input = self.create_input_field("Street and Number:")

        self.postal_code_input = self.create_input_field("Postal Code:")

        layout.addWidget(self.street_input)
        self.street_input.textChanged.connect(self.check_fields)

        layout.addWidget(self.postal_code_input)
        self.postal_code_input.textChanged.connect(self.check_fields)


        self.country_input = QLineEdit("Germany")
        self.country_input.setReadOnly(True)
        self.country_input.setStyleSheet(loginmainstyle)
        layout.addWidget(QLabel("Country:"))
        layout.addWidget(self.country_input)

        self.phone_input = self.create_input_field("Phone:")
        layout.addWidget(self.phone_input)
        self.phone_input.textChanged.connect(self.check_fields)


        # Méthode de paiement
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.setStyleSheet(style_box)
        self.payment_method_combo.addItems(["Bank Transfer", "Credit Card", "PayPal"])
        self.payment_method_combo.currentTextChanged.connect(self.update_payment_fields)
        layout.addWidget(QLabel("Payment Method:"))
        layout.addWidget(self.payment_method_combo)

        # Section pour les champs dynamiques
        self.dynamic_payment_layout = QVBoxLayout()
        layout.addLayout(self.dynamic_payment_layout)
        self.update_payment_fields()  # Initialiser les champs dynamiques

        # Boutons pour confirmer ou annuler
        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(cancelstyle)
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setEnabled(False)
        self.confirm_button.setStyleSheet(confirmbtnstyledisable)
        self.confirm_button.clicked.connect(self.confirm_purchase)
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)

        # Validation des champs

        self.setLayout(layout)

    def create_input_field(self, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setStyleSheet(loginmainstyle)
        return field

    def update_payment_fields(self):
        """Met à jour les champs dynamiques en fonction de la méthode de paiement sélectionnée."""
        for i in reversed(range(self.dynamic_payment_layout.count())):
            widget = self.dynamic_payment_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()

        method = self.payment_method_combo.currentText()
        if method == "Bank Transfer":
            self.payment_input = self.create_input_field("Enter your bank details")
            self.dynamic_payment_layout.addWidget(QLabel("Bank Details:"))
            self.dynamic_payment_layout.addWidget(self.payment_input)
        elif method == "Credit Card":
            self.card_number_input = self.create_input_field("Enter your card number")
            self.cvv_input = self.create_input_field("Enter your CVV")
            self.cvv_input.setMaxLength(3)
            self.dynamic_payment_layout.addWidget(QLabel("Card Number:"))
            self.dynamic_payment_layout.addWidget(self.card_number_input)
            self.dynamic_payment_layout.addWidget(QLabel("CVV:"))
            self.dynamic_payment_layout.addWidget(self.cvv_input)
        elif method == "PayPal":
            self.paypal_email_input = self.create_input_field("Enter your PayPal email")
            self.dynamic_payment_layout.addWidget(QLabel("PayPal Email:"))
            self.dynamic_payment_layout.addWidget(self.paypal_email_input)

        # Connecter les champs dynamiques à la vérification
        self.check_fields()

    def check_fields(self):
        """Vérifie si tous les champs nécessaires sont valides."""
        street_valid = is_valid_street(self.street_input.text().strip())
        postal_code_valid = is_valid_postcode(self.postal_code_input.text().strip())
        phone_valid = is_valid_phone(self.phone_input.text().strip())

        method = self.payment_method_combo.currentText()
        payment_valid = False

        if method == "Bank Transfer" and hasattr(self, 'payment_input'):
            payment_valid = is_valid_bank_details(self.payment_input.text().strip())
        elif method == "Credit Card" and hasattr(self, 'card_number_input') and hasattr(self, 'cvv_input'):
            payment_valid = (
                    is_valid_credit_card(self.card_number_input.text().strip())
                    and is_valid_cvv(self.cvv_input.text().strip())
            )
        elif method == "PayPal" and hasattr(self, 'paypal_email_input'):
            payment_valid = is_valid_email(self.paypal_email_input.text().strip())

        if hasattr(self, 'confirm_button'):
            if street_valid and postal_code_valid and phone_valid and payment_valid:
                self.confirm_button.setEnabled(True)
                self.confirm_button.setStyleSheet(confirmbtnstyle)
            else:
                self.confirm_button.setEnabled(False)
                self.confirm_button.setStyleSheet(confirmbtnstyledisable)

    def confirm_purchase(self):
        """Confirme l'achat et sauvegarde les détails."""
        try:
            street = self.street_input.text().strip()
            postal_code = self.postal_code_input.text().strip()
            phone = self.phone_input.text().strip()
            payment_info = ""
            method = self.payment_method_combo.currentText()

            if method == "Bank Transfer":
                payment_info = self.payment_input.text().strip()
            elif method == "Credit Card":
                payment_info = f"{self.card_number_input.text().strip()} (CVV: {self.cvv_input.text().strip()})"
            elif method == "PayPal":
                payment_info = self.paypal_email_input.text().strip()

            # Sauvegarde dans un fichier
            with open("bookings.txt", "a") as file:
                file.write(f"Name: {self.user_name}\n")
                file.write(f"Trip Number: {self.trip_data['Reisenummer']}\n")
                file.write(f"Cabin Type: {self.cabin_type}\n")
                file.write(f"Price: {self.cabin_price} €\n")
                file.write(f"Address: {street}, {postal_code}, Germany\n")
                file.write(f"Phone: {phone}\n")
                file.write(f"Payment Method: {method}, {payment_info}\n")
                file.write("-" * 50 + "\n")

            QMessageBox.information(self, "Purchase Successful", "Your booking has been confirmed!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

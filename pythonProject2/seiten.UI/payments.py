from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QHBoxLayout, QLabel, QPushButton
from styles import *
from checking_funktion import *


class PaymentPage(QWidget):
    def __init__(self, trip_data, cabin_type, cabin_price, user_balance, user_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Purchase")
        self.resize(800, 600)

        # Données utilisateur
        self.trip_data = trip_data
        self.cabin_type = cabin_type
        self.cabin_price = cabin_price
        self.user_balance = user_balance
        self.user_name = user_name

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Résumé des informations
        layout.addWidget(QLabel(f"<b>Trip Number:</b> {trip_data['Reisenummer']}"))
        layout.addWidget(QLabel(f"<b>Cabin Type:</b> {cabin_type}"))
        layout.addWidget(QLabel(f"<b>Price:</b> {int(cabin_price)} €"))
        layout.addWidget(QLabel(f"<b>Remaining Balance:</b> {int(user_balance - cabin_price)} €"))

        # Champs utilisateur
        self.street_input = self.create_input_field("Street and Number:")
        self.postal_code_input = self.create_input_field("Postal Code:")
        self.phone_input = self.create_input_field("Phone:")

        # Ajouter les champs au layout
        for field in [self.street_input, self.postal_code_input, self.phone_input]:
            layout.addWidget(field)
            field.textChanged.connect(self.validate_fields)

        # Pays (readonly)
        self.country_input = QLineEdit("Germany")
        self.country_input.setReadOnly(True)
        self.country_input.setStyleSheet(loginmainstyle)
        layout.addWidget(QLabel("Country:"))
        layout.addWidget(self.country_input)

        # Méthode de paiement
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.setStyleSheet(style_box)
        self.payment_method_combo.addItems(["Bank Transfer", "Credit Card", "PayPal"])
        layout.addWidget(QLabel("Payment Method:"))
        layout.addWidget(self.payment_method_combo)
        self.payment_method_combo.currentTextChanged.connect(self.update_payment_fields)

        # Champs dynamiques pour la méthode de paiement
        self.dynamic_payment_layout = QVBoxLayout()
        layout.addLayout(self.dynamic_payment_layout)
        self.update_payment_fields()

        # Boutons
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
            self.payment_input.textChanged.connect(self.validate_fields)
        elif method == "Credit Card":
            self.card_number_input = self.create_input_field("Enter your card number")
            self.cvv_input = self.create_input_field("Enter your CVV")
            self.cvv_input.setMaxLength(3)
            self.dynamic_payment_layout.addWidget(QLabel("Card Number:"))
            self.dynamic_payment_layout.addWidget(self.card_number_input)
            self.dynamic_payment_layout.addWidget(QLabel("CVV:"))
            self.dynamic_payment_layout.addWidget(self.cvv_input)
            self.card_number_input.textChanged.connect(self.validate_fields)
            self.cvv_input.textChanged.connect(self.validate_fields)
        elif method == "PayPal":
            self.paypal_email_input = self.create_input_field("Enter your PayPal email")
            self.dynamic_payment_layout.addWidget(QLabel("PayPal Email:"))
            self.dynamic_payment_layout.addWidget(self.paypal_email_input)
            self.paypal_email_input.textChanged.connect(self.validate_fields)

        self.validate_fields()

    def validate_fields(self):
        """Valide les champs obligatoires et active/désactive le bouton Confirm."""
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
        """Confirme l'achat."""
        show_success_message("Purchase Confirmed", "Your booking has been successfully completed!")
        self.close()

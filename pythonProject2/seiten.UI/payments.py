from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QHBoxLayout, QLabel, QPushButton, QScrollArea, \
    QFileDialog
from styles import *
from checking_funktion import *
from database_action import update_user_balance


class PaymentPage(QWidget):
    def __init__(self, trip_data, cabin_type, cabin_price, user_balance, user_name,
                 stacked_widget, konto_edit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Purchase")

        self.trip_data = trip_data
        self.cabin_type = cabin_type
        self.cabin_price = cabin_price
        self.user_balance = user_balance
        self.user_name = user_name
        self.stacked_widget = stacked_widget
        self.konto_edit = konto_edit


        layout = QVBoxLayout()
        layout.setSpacing(20)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.verticalScrollBar().setStyleSheet(city_section_style)

        scrollable_widget = QWidget()
        scrollable_layout = QVBoxLayout(scrollable_widget)
        scroll_area.setWidget(scrollable_widget)
        scrollable_layout.setContentsMargins(20, 0, 20, 40)



        scrollable_layout.addWidget(QLabel(f"<b>Trip Number:</b> {trip_data['Reisenummer']}"))
        scrollable_layout.addWidget(QLabel(f"<b>Cabin Type:</b> {cabin_type}"))
        scrollable_layout.addWidget(QLabel(f"<b>Price:</b> {int(cabin_price)} €"))
        scrollable_layout.addWidget(QLabel(f"<b>Remaining Balance:</b> {int(user_balance - cabin_price)} €"))

        scrollable_layout.addWidget(QLabel("Street and Number:"))
        self.street_input = self.create_input_field("Enter your street and number")
        scrollable_layout.addWidget(self.street_input)
        self.street_input.textChanged.connect(self.validate_fields)

        scrollable_layout.addWidget(QLabel("Postal Code:"))
        self.postal_code_input = self.create_input_field("Enter your postal code")
        scrollable_layout.addWidget(self.postal_code_input)
        self.postal_code_input.textChanged.connect(self.validate_fields)

        scrollable_layout.addWidget(QLabel("City:"))
        self.city_input = self.create_input_field("Enter your city")
        scrollable_layout.addWidget(self.city_input)
        self.city_input.textChanged.connect(self.validate_fields)

        scrollable_layout.addWidget(QLabel("Phone:"))
        self.phone_input = self.create_input_field("Enter your phone number")
        scrollable_layout.addWidget(self.phone_input)
        self.phone_input.textChanged.connect(self.validate_fields)

        # Pays (readonly)
        scrollable_layout.addWidget(QLabel("Country:"))
        self.country_input = QLineEdit("Germany")
        self.country_input.setReadOnly(True)
        self.country_input.setStyleSheet(loginmainstyle)
        scrollable_layout.addWidget(self.country_input)

        scrollable_layout.addWidget(QLabel("Payment Method:"))
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.setStyleSheet(style_box)
        self.payment_method_combo.addItems(["Bank Transfer", "Credit Card", "PayPal"])
        scrollable_layout.addWidget(self.payment_method_combo)
        self.payment_method_combo.currentTextChanged.connect(self.update_payment_fields)

        self.dynamic_payment_layout = QVBoxLayout()
        scrollable_layout.addLayout(self.dynamic_payment_layout)
        self.update_payment_fields()

        button_layout = QHBoxLayout()


        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(cancelstyle)
        self.cancel_button.clicked.connect(self.cancel_payment)
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setEnabled(False)
        self.confirm_button.setStyleSheet(confirmbtnstyledisable)
        self.confirm_button.clicked.connect(self.confirm_purchase)
        button_layout.addWidget(self.confirm_button)

        layout.addWidget(scroll_area)
        layout.addSpacing(30)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_input_field(self, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setStyleSheet(loginmainstyle)
        return field

    def update_payment_fields(self):
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
        street_valid = is_valid_street(self.street_input.text().strip())
        postal_code_valid = is_valid_postcode(self.postal_code_input.text().strip())
        city_valid = is_valid_city(self.city_input.text().strip())
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
            if street_valid and postal_code_valid and city_valid  and phone_valid and payment_valid:
                self.confirm_button.setEnabled(True)
                self.confirm_button.setStyleSheet(confirmbtnstyle)
            else:
                self.confirm_button.setEnabled(False)
                self.confirm_button.setStyleSheet(confirmbtnstyledisable)

    def confirm_purchase(self):
        try:
            new_balance = self.user_balance - self.cabin_price

            update_user_balance(self.user_name, new_balance)
            if self.konto_edit:
                self.konto_edit.setText(f"{new_balance:} €")

            show_success_message("Purchase Confirmed", "Your booking has been successfully completed!")

            self.save_booking_as_text()

            show_success_message("Saved", "Booking details have been saved successfully!")
            if self.stacked_widget:
                self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(0))


        except Exception as e:
            show_warning_message("Error", f"An error occurred during the purchase: {e}")

    def cancel_payment(self):
        if self.stacked_widget:
            previous_page_index = self.stacked_widget.currentIndex() - 3
            self.stacked_widget.setCurrentIndex(previous_page_index)

    def save_booking_as_text(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Booking as Text",
                            f"{self.user_name}_bookingconfirmation.txt", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "w") as file:
                    file.write(f"Name: {self.user_name}\n")
                    file.write(f"Trip Number: {self.trip_data['Reisenummer']}\n")
                    file.write(f"Cabin Type: {self.cabin_type}\n")
                    file.write(f"Price: {self.cabin_price} €\n")
                    file.write(
                        f"Address: {self.street_input.text().strip()}, "
                        f"{self.postal_code_input.text().strip()} {self.city_input.text().strip()}, Germany\n")
                    file.write(f"Phone: {self.phone_input.text().strip()}\n")
                    file.write(f"Payment Method: {self.payment_method_combo.currentText()}\n")
                    if hasattr(self, 'payment_input'):
                        file.write(f"Bank Details: {self.payment_input.text().strip()}\n")
                    if hasattr(self, 'card_number_input') and hasattr(self, 'cvv_input'):
                        file.write(
                            f"Card Number: {self.card_number_input.text().strip()} (CVV:"
                            f" {self.cvv_input.text().strip()})\n")
                    if hasattr(self, 'paypal_email_input'):
                        file.write(f"PayPal Email: {self.paypal_email_input.text().strip()}\n")

        except Exception:
            return

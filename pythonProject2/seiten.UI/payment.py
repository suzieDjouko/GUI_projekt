from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit


class PaymentProcessor:
    def __init__(self, username, total_price, payment_method, get_user_balance, update_user_balance):
        self.username = username
        self.total_price = total_price
        self.payment_method = payment_method
        self.get_user_balance = get_user_balance  # Fonction pour obtenir le solde de l'utilisateur
        self.update_user_balance = update_user_balance  # Fonction pour mettre à jour le solde de l'utilisateur

    def process_payment(self):
        """
        Gère le processus de paiement : validation du solde et mise à jour.
        """
        try:
            user_balance = self.get_user_balance(self.username)

            if user_balance is None:
                self.show_error("User not found.")
                return

            if self.total_price > user_balance:
                self.show_error("Insufficient balance.")
                return

            # Si le solde est suffisant, mettre à jour le solde
            new_balance = user_balance - self.total_price
            self.update_user_balance(self.username, new_balance)

            # Afficher un message de succès
            self.show_success(f"Your payment of {self.total_price} € using {self.payment_method} was successful.")
            return new_balance  # Retourne le nouveau solde après le paiement
        except Exception as e:
            self.show_error(f"Error processing payment: {e}")

    def show_error(self, message):
        """Affiche un message d'erreur dans une boîte de dialogue."""
        QMessageBox.warning(None, "Payment Error", message)

    def show_success(self, message):
        """Affiche un message de succès dans une boîte de dialogue."""
        QMessageBox.information(None, "Payment Successful", message)


class PurchasedProductDialog(QDialog):
    def __init__(self, trip_data, user_data, balance, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gekauftes Produkt")

        self.trip_data = trip_data
        self.user_data = user_data
        self.balance = balance

        # Layout pour le dialogue
        layout = QVBoxLayout()

        # Afficher les informations sur la réservation
        trip_info = QLabel(f"Reise Nummer: {self.trip_data['Reisenummer']}\n"
                           f"Schiffstyp: {self.trip_data['Schiffstyp']}\n"
                           f"Kabinenart: {self.trip_data['Kabinentyp']}\n"
                           f"Reisedaten: {self.trip_data['Reisedatum']}\n"
                           f"Reisepreis: {self.trip_data['Preis']} €")
        layout.addWidget(trip_info)

        # Afficher les villes visitées (ici, on les affiche toutes en même temps ou une par une)
        cities_layout = QHBoxLayout()
        if self.user_data['show_cities_together']:
            for city in self.trip_data['Besuchte_Städte']:
                city_label = QLabel(city)
                cities_layout.addWidget(city_label)
        else:
            self.city_index = 0
            self.city_label = QLabel(self.trip_data['Besuchte_Städte'][self.city_index])
            next_button = QPushButton("Nächste Stadt")
            next_button.clicked.connect(self.show_next_city)
            cities_layout.addWidget(self.city_label)
            cities_layout.addWidget(next_button)

        layout.addLayout(cities_layout)

        # Bouton pour acheter et entrer les données utilisateur
        buy_button = QPushButton("Reise kaufen")
        buy_button.clicked.connect(self.purchase_trip)
        layout.addWidget(buy_button)

        self.setLayout(layout)

    def show_next_city(self):
        """Affiche la prochaine ville dans la liste"""
        if self.city_index < len(self.trip_data['Besuchte_Städte']) - 1:
            self.city_index += 1
            self.city_label.setText(self.trip_data['Besuchte_Städte'][self.city_index])

    def purchase_trip(self):
        """Confirme l'achat et affiche le formulaire de données utilisateur"""
        self.accept()  # Ferme le dialogue actuel
        self.show_user_data_dialog()

    def show_user_data_dialog(self):
        """Affiche le dialogue pour les données utilisateur"""
        user_data_dialog = UserDataDialog(self.user_data, self.trip_data, self.balance)
        user_data_dialog.exec_()


class UserDataDialog(QDialog):
    def __init__(self, user_data, trip_data, balance, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Benutzerdaten für die Buchung")

        self.user_data = user_data
        self.trip_data = trip_data
        self.balance = balance

        layout = QVBoxLayout()

        # Formulaire pour les données utilisateur
        self.name_input = QLineEdit()
        self.name_input.setText(self.user_data['name'])
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        self.address_input = QLineEdit()
        layout.addWidget(QLabel("Adresse:"))
        layout.addWidget(self.address_input)

        self.phone_input = QLineEdit()
        layout.addWidget(QLabel("Handynummer:"))
        layout.addWidget(self.phone_input)

        self.bank_input = QLineEdit()
        layout.addWidget(QLabel("Bankdaten:"))
        layout.addWidget(self.bank_input)

        # Confirmation de l'achat
        confirm_button = QPushButton("Bestätigen")
        confirm_button.clicked.connect(self.confirm_purchase)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def confirm_purchase(self):
        """Confirme l'achat et enregistre les données utilisateur"""
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        bank_details = self.bank_input.text()

        # Enregistre les données dans un fichier texte
        with open("buchung.txt", "a") as file:
            file.write(f"Name: {name}\n")
            file.write(f"Reisenummer: {self.trip_data['Reisenummer']}\n")
            file.write(f"Kabinenart: {self.trip_data['Kabinentyp']}\n")
            file.write(f"Preis: {self.trip_data['Preis']} €\n")
            file.write(f"Adresse: {address}\n")
            file.write(f"Handynummer: {phone}\n")
            file.write(f"Bankdaten: {bank_details}\n")
            file.write("\n")

        # Mise à jour du solde
        new_balance = self.balance - self.trip_data['Preis']
        self.user_data['balance'] = new_balance

        # Affiche un message de confirmation
        QMessageBox.information(self, "Erfolgreich", "Ihre Reise wurde erfolgreich gebucht!")
        self.accept()

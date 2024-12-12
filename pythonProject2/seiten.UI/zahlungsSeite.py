from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt


class PaymentPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paiement - MasterCard/Visa")
        self.setGeometry(200, 200, 600, 600)
        self.init_ui()

    def init_ui(self):
        # Création du layout principal
        main_layout = QVBoxLayout()

        # Header
        header = QLabel("Header Placeholder")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: #f0f0f0; font-size: 16px; padding: 10px;")
        main_layout.addWidget(header)

        # Layout central pour le formulaire de paiement
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(20, 20, 20, 20)

        # Titre de la page
        title_label = QLabel("Page de Paiement")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        central_layout.addWidget(title_label)

        # Champ pour le nom complet
        name_layout = QHBoxLayout()
        name_label = QLabel("Nom complet:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        central_layout.addLayout(name_layout)

        # Champ pour le numéro de carte
        card_layout = QHBoxLayout()
        card_label = QLabel("Numéro de carte:")
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        card_layout.addWidget(card_label)
        card_layout.addWidget(self.card_input)
        central_layout.addLayout(card_layout)

        # Champ pour la date d'expiration
        expiry_layout = QHBoxLayout()
        expiry_label = QLabel("Date d'expiration:")
        self.expiry_input = QLineEdit()
        self.expiry_input.setPlaceholderText("MM/AA")
        expiry_layout.addWidget(expiry_label)
        expiry_layout.addWidget(self.expiry_input)
        central_layout.addLayout(expiry_layout)

        # Champ pour le code CVV
        cvv_layout = QHBoxLayout()
        cvv_label = QLabel("Code CVV:")
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("123")
        self.cvv_input.setEchoMode(QLineEdit.Password)
        cvv_layout.addWidget(cvv_label)
        cvv_layout.addWidget(self.cvv_input)
        central_layout.addLayout(cvv_layout)

        # Menu déroulant pour le type de carte
        card_type_layout = QHBoxLayout()
        card_type_label = QLabel("Type de carte:")
        self.card_type_combo = QComboBox()
        self.card_type_combo.addItems(["MasterCard", "Visa"])
        card_type_layout.addWidget(card_type_label)
        card_type_layout.addWidget(self.card_type_combo)
        central_layout.addLayout(card_type_layout)

        # Ajouter un espace extensible pour rendre le layout responsive
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        central_layout.addSpacerItem(spacer)

        # Bouton pour confirmer le paiement
        self.pay_button = QPushButton("Payer")
        self.pay_button.setStyleSheet("background-color: green; color: white; font-size: 16px; padding: 10px;")
        self.pay_button.clicked.connect(self.process_payment)
        central_layout.addWidget(self.pay_button)

        # Ajouter le layout central au layout principal
        main_layout.addLayout(central_layout)

        # Footer
        footer = QLabel("Footer Placeholder")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("background-color: #f0f0f0; font-size: 14px; padding: 10px;")
        main_layout.addWidget(footer)

        # Appliquer le layout principal
        self.setLayout(main_layout)

    def process_payment(self):
        """
        Valider les informations entrées et afficher un message factice.
        """
        name = self.name_input.text()
        card = self.card_input.text()
        expiry = self.expiry_input.text()
        cvv = self.cvv_input.text()
        card_type = self.card_type_combo.currentText()

        # Validation basique des champs
        if not name or not card or not expiry or not cvv:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        if len(card.replace("-", "").replace(" ", "")) != 16 or not card.replace("-", "").isdigit():
            QMessageBox.warning(self, "Erreur", "Le numéro de carte est invalide.")
            return

        if len(cvv) != 3 or not cvv.isdigit():
            QMessageBox.warning(self, "Erreur", "Le code CVV est invalide.")
            return

        QMessageBox.information(self, "Succès", f"Paiement avec {card_type} réussi (factice) !")
        self.close()


# Exemple pour lancer la fenêtre si ce fichier est exécuté directement
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = PaymentPage()
    window.show()
    sys.exit(app.exec_())

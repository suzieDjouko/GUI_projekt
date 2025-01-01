from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class UserInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profil de l'utilisateur")
        self.setMinimumSize(400, 300)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Labels pour les informations utilisateur
        self.username_label = QLabel("Nom d'utilisateur :")
        self.username_label.setAlignment(Qt.AlignLeft)
        self.username_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        self.email_label = QLabel("Email :")
        self.email_label.setAlignment(Qt.AlignLeft)
        self.email_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        self.kontostand_label = QLabel("Solde :")
        self.kontostand_label.setAlignment(Qt.AlignLeft)
        self.kontostand_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        # Ajouter les labels au layout principal
        self.main_layout.addWidget(self.username_label)
        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.kontostand_label)

    def update_user_info(self, user_data):
        """
        Met à jour les informations utilisateur affichées sur la page.
        :param user_data: dict contenant les informations utilisateur.
        """
        self.username_label.setText(f"Nom d'utilisateur : {user_data.get('username', 'N/A')}")
        self.email_label.setText(f"Email : {user_data.get('email', 'N/A')}")
        self.kontostand_label.setText(f"Solde : {user_data.get('kontostand', 'N/A')} €")

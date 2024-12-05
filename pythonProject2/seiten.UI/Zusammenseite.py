from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt


class KreuzfahrtZusammenfassung(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Buchung - Zusammenfassung")
        self.setGeometry(200, 100, 900, 700)

        # Layout principal
        hauptlayout = QVBoxLayout(self)
        hauptlayout.setContentsMargins(10, 10, 10, 10)

        # Header
        header_label = QLabel("Buchung - Zusammenfassung")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        hauptlayout.addWidget(header_label)

        # Layout horizontal pour images et formulaire
        horizontal_layout = QHBoxLayout()

        # Barre latérale gauche (Images)
        image_layout = QVBoxLayout()
        image_layout.setSpacing(20)

        # Première image
        image1_label = QLabel("Image 1 ")
        image1_label.setFixedSize(400, 300)  # Taille du cadre
        image1_label.setStyleSheet("border: 1px solid black; background-color: lightgray;")
        image_layout.addWidget(image1_label, alignment=Qt.AlignCenter)

        # Deuxième image
        image2_label = QLabel("Image 2")
        image2_label.setFixedSize(400, 300)  # Taille du cadre
        image2_label.setStyleSheet("border: 1px solid black; background-color: lightgray;")
        image_layout.addWidget(image2_label, alignment=Qt.AlignCenter)

        horizontal_layout.addLayout(image_layout)

        # Partie scrollable
        scroll_area = QScrollArea()
        scroll_widget = QWidget()  # Création de contenu dans l'aire scrollable

        # Contenu principal (Reiseinformationen, Schiffsdaten, Zusammenfassung)
        hauptinhalt = QVBoxLayout(scroll_widget)
        hauptinhalt.setSpacing(20)

        # 1. Reiseinformationen
        reiseinfos_frame = self.create_section("Reiseinformationen", [
            ("Abfahrt", "z.B. 25.12.2024"),
            ("Ankunft", "z.B. 31.12.2024"),
            ("Nächte", "Anzahl der Nächte eingeben"),
        ])
        hauptinhalt.addWidget(reiseinfos_frame)

        # 2. Schiffsdaten
        schiffsdaten_frame = self.create_section("Schiffsdaten", [
            ("Schiffstyp", "z.B. Kreuzfahrtschiff"),
            ("Kabinenklasse", "z.B. Deluxe, Standard"),
        ])
        hauptinhalt.addWidget(schiffsdaten_frame)

        # 3. Zusammenfassung
        zusammenfassung_frame = self.create_section("Zusammenfassung", [
            ("Besuchte Städte", "Liste der Städte eingeben"),
            ("Gesamtpreis", "Preis eingeben"),
        ])
        hauptinhalt.addWidget(zusammenfassung_frame)

        # Configuration du ScrollArea
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        horizontal_layout.addWidget(scroll_area)

        hauptlayout.addLayout(horizontal_layout)

        # Footer avec boutons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        zurueck_button = QPushButton("Zurück")
        zurueck_button.setStyleSheet(
            "background-color: red; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        zurueck_button.setFixedSize(200, 50)
        zurueck_button.clicked.connect(self.rueckkehr_bestaetigen)
        button_layout.addWidget(zurueck_button)

        buchung_button = QPushButton("Zahlung")
        buchung_button.setStyleSheet(
            "background-color: blue; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )
        buchung_button.setFixedSize(200, 50)
        buchung_button.clicked.connect(self.buchung_bestaetigen)
        button_layout.addWidget(buchung_button)
        hauptlayout.addLayout(button_layout)

    def create_section(self, titel, felder):
        """Fonction d'aide pour créer une section avec des champs de saisie."""
        frame = QFrame()
        frame.setStyleSheet("border: 1px solid black; padding: 10px;")
        layout = QVBoxLayout(frame)

        # Titre
        label = QLabel(titel)
        label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        label.setFixedWidth(300)  # Réduction de la largeur
        layout.addWidget(label, alignment=Qt.AlignLeft)

        # Champs
        for feld_name, placeholder in felder:
            feld_label = QLabel(feld_name + ":")
            feld_label.setStyleSheet("font-size: 14px;")
            feld_label.setFixedWidth(300)  # largeur fixe
            layout.addWidget(feld_label, alignment=Qt.AlignLeft)

            feld_input = QLineEdit()
            feld_input.setPlaceholderText(placeholder)
            feld_input.setStyleSheet("padding: 5px; border: 1px solid gray;")
            feld_input.setFixedWidth(300)  # largeur fixe
            layout.addWidget(feld_input)

        return frame

    def buchung_bestaetigen(self):
        print("Buchung wurde bestätigt!")

    def rueckkehr_bestaetigen(self):
        print("Rückkehr wurde bestätigt!")


if __name__ == "__main__":
    app = QApplication([])
    fenster = KreuzfahrtZusammenfassung()
    fenster.show()
    app.exec_()

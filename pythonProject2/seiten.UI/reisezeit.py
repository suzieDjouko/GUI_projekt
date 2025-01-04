import os

from PyQt5.QtCore import QDate, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QDateEdit, QHBoxLayout, QPushButton, QMessageBox, QFrame, QScrollArea, QStackedWidget
)


class ReisezeitPage(QWidget):
    def __init__(self, stacked_widget, payment_page, cabin_page, get_filtered_results):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.payment_page = payment_page
        self.cabin_page = cabin_page
        self.get_filtered_results = get_filtered_results
        #self.filtered_results = df
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        dataframe = self.get_filtered_results()


        # Title
        title_label = QLabel("Choose Your Travel Dates and Explore Cities")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)
        layout.addWidget(QLabel("Cities Included in Your Trip:"))
        self.carousel_widget = QStackedWidget()
        self.carousel_widget.setFixedHeight(200)
        self.populate_carousel(dataframe)
        layout.addWidget(self.carousel_widget)


        # Datum der Abreise
        layout.addWidget(QLabel("Departure Date:"))
        self.departure_date_edit = QDateEdit()
        self.departure_date_edit.setCalendarPopup(True)
        self.departure_date_edit.setMinimumDate(QDate(2025, 5, 1))
        self.departure_date_edit.setMaximumDate(QDate(2025, 10, 31))
        self.departure_date_edit.dateChanged.connect(self.on_departure_date_changed)
        layout.addWidget(self.departure_date_edit)

        # Datum der Rückkehr
        layout.addWidget(QLabel("Return Date:"))
        self.return_date_edit = QDateEdit()
        self.return_date_edit.setCalendarPopup(True)
        self.return_date_edit.setMinimumDate(QDate(2025, 5, 2))
        self.return_date_edit.setMaximumDate(QDate(2025, 10, 31))
        layout.addWidget(self.return_date_edit)

        # Abschnitt für das Karussell
        # Füllt das Karussell mit den gefilterten Städten.

        # Automatisches Scrollen
        self.carousel_timer = QTimer(self)
        self.carousel_timer.timeout.connect(self.show_next_city)
        self.carousel_timer.start(3000)  # Change d'image toutes les 3 secondes

        # Boutons
        button_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm_selection)
        button_layout.addWidget(back_button)
        button_layout.addWidget(confirm_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def populate_carousel(self, filtered_results):
        """
        Fügt die Bilder der gefilterten Städte dem Karussell hinzu.
        """
        visited_cities = filtered_results["Besuchte_Städte"].dropna().unique()
        cities = set(city.strip() for cities in visited_cities for city in cities.split(","))

        extensions = [".jpg", ".JPG", ".jpeg"]

        for city in sorted(cities):
            city_label = QLabel()
            city_label.setAlignment(Qt.AlignCenter)
            image_path = None

            for ext in extensions:
                potential_path = f"../images/Hafenstaedte/{city}{ext}"
                if os.path.exists(potential_path):
                    image_path = potential_path
                    break

            if image_path:
                pixmap = QPixmap(image_path).scaled(300, 200, Qt.KeepAspectRatio)
                city_label.setPixmap(pixmap)
            else:
                city_label.setText(f"No image for {city}")

            self.carousel_widget.addWidget(city_label)

    def show_next_city(self):
        """
        Springt zum nächsten Bild im Karussell.
        """
        current_index = self.carousel_widget.currentIndex()
        next_index = (current_index + 1) % self.carousel_widget.count()
        self.carousel_widget.setCurrentIndex(next_index)

    def on_departure_date_changed(self, date):
        """
        Passt die Optionen für das Rückreisedatum an das Abreisedatum an.
        """
        self.return_date_edit.setMinimumDate(date.addDays(1))  # Das Rückreisedatum muss mindestens 1 Tag später liegen

    def confirm_selection(self):
        """
        Bestätigt die gewählten Daten.
        """
        departure_date = self.departure_date_edit.date().toString("yyyy-MM-dd")
        return_date = self.return_date_edit.date().toString("yyyy-MM-dd")

        if self.return_date_edit.date() <= self.departure_date_edit.date():
            QMessageBox.warning(self, "Error", "The return date must be after the departure date.")
            return

        QMessageBox.information(
            self,
            "Confirmation",
            f"Dates confirmed:\nDeparture: {departure_date}\nReturn: {return_date}"
        )
        self.stacked_widget.setCurrentWidget(self.payment_page)  # Zur Zahlungsseite navigieren

    def go_back(self):
        """
        Kehrt zur vorherigen Seite zurück.
        """
        self.stacked_widget.setCurrentWidget(self.cabin_page)
import os

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap, QTextCharFormat, QColor
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QDateEdit, QHBoxLayout, QPushButton, QMessageBox, QFrame, QScrollArea, QStackedWidget
)
from styles import Datestyle , validbtnstyle ,cancelstyle,back_button_style,confirmbtnstyledisable,confirmbtnstyle
from checking_funktion import show_return_date_error , clear_layout
from payments import PaymentPage
from database_action import get_user_balance



class ReisezeitPage(QWidget):
    def __init__(self,trip_data, cabin_type, cabin_price, user_balance,user_name, stacked_widget, konto_edit, payment_page, cabin_page,parent=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.payment_page = payment_page
        self.cabin_page = cabin_page        #self.filtered_results = df
        self.trip_data = trip_data
        self.cabin_type = cabin_type
        self.cabin_price = cabin_price
        self.user_balance = user_balance
        self.user_name = user_name
        self.konto_edit = konto_edit

        layout = QVBoxLayout()

        # Title
        title = QLabel("<h2>Adjust Your Travel Time</h2>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)


        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Container für scrollbare Inhalte
        scrollable_widget = QWidget()

        self.trip_details_label = QLabel()
        self.trip_details_label.setStyleSheet("font-size: 18px; margin-bottom: 20px;")
        layout.addWidget(self.trip_details_label)

        # Abschnitt für Städte
        layout.addWidget(QLabel("Cities Included in Your Trip:"))
        self.city_scroll_area = QScrollArea()
        self.city_scroll_area.setWidgetResizable(True)
        layout.addWidget(self.city_scroll_area)

        # Bilder von Bootstypen und Kabinen
        self.ship_cabin_layout = QHBoxLayout()

        ship_layout = QVBoxLayout()
        ship_layout.addWidget(QLabel("Ship Type:"))
        self.ship_image_label = QLabel()
        self.ship_image_label.setFixedSize(300, 250)
        self.ship_image_label.setAlignment(Qt.AlignCenter)
        ship_layout.addWidget(self.ship_image_label)
        self.ship_cabin_layout.addLayout(ship_layout)

        cabin_layout = QVBoxLayout()
        cabin_layout.addWidget(QLabel("Cabin:"))
        self.cabin_image_label = QLabel()
        self.cabin_image_label.setFixedSize(300, 250)
        self.cabin_image_label.setAlignment(Qt.AlignCenter)
        cabin_layout.addWidget(self.cabin_image_label)
        self.ship_cabin_layout.addLayout(cabin_layout)

        layout.addLayout(self.ship_cabin_layout)

        # Datum der Abreise
        layout.addWidget(QLabel("Departure Date:"))
        self.departure_date_edit = QDateEdit()
        self.departure_date_edit.setStyleSheet(Datestyle)
        self.departure_date_edit.setCalendarPopup(True)
        self.departure_date_edit.setMinimumDate(QDate(2025, 5, 1))
        self.departure_date_edit.setMaximumDate(QDate(2025, 10, 31))
        self.departure_date_edit.dateChanged.connect(self.on_departure_date_changed)
        layout.addWidget(self.departure_date_edit)

        # Datum der Rückkehr
        layout.addWidget(QLabel("Return Date:"))
        self.return_date_edit = QDateEdit()
        self.return_date_edit.setStyleSheet(Datestyle)
        self.return_date_edit.setCalendarPopup(True)
        self.return_date_edit.setMinimumDate(QDate(2025, 5, 2))
        self.return_date_edit.setMaximumDate(QDate(2025, 10, 31))
        layout.addWidget(self.return_date_edit)

        date_button_layout = QHBoxLayout()
        date_button_layout.addStretch()

        self.validate_date_button = QPushButton("Valid")
        self.validate_date_button.setFixedSize(150, 40)
        self.validate_date_button.setStyleSheet(validbtnstyle)
        self.validate_date_button.clicked.connect(self.on_validate_date_clicked)
        date_button_layout.addWidget(self.validate_date_button)

        self.cancel_date_button = QPushButton("Cancel")
        self.cancel_date_button.setFixedSize(150, 40)
        self.cancel_date_button.setStyleSheet(cancelstyle)
        self.cancel_date_button.clicked.connect(self.on_cancel_date_clicked)
        date_button_layout.addWidget(self.cancel_date_button)

        layout.addLayout(date_button_layout)

        # Abschnitt für gekaufte Reisen

        layout.addWidget(QLabel("<b>Purchased Products</b>"))
        self.gekauft_scroll_area = QScrollArea()
        self.gekauft_scroll_area.setWidgetResizable(True)

        self.date_layout = QVBoxLayout()

        self.gekauft_container = QWidget()

        self.gekauft_layout = QVBoxLayout(self.gekauft_container)
        # self.gekauft_layout.addLayout(self.date_layout)
        self.gekauft_layout.setContentsMargins(20, 10, 20, 10)
        self.gekauft_layout.setSpacing(15)

        self.gekauft_scroll_area.setWidget(self.gekauft_container)
        layout.addWidget(self.gekauft_scroll_area)

        scroll_area.setWidget(scrollable_widget)
        ############self.reisezeit_page_layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        self.reisezeit_return_button = QPushButton("Return")
        self.reisezeit_return_button.setStyleSheet(back_button_style)
        self.reisezeit_return_button.clicked.connect(self.on_back_to_cabin_clicked)

        self.reisezeit_confirm_button = QPushButton("Confirm")
        self.reisezeit_confirm_button.setEnabled(False)
        self.reisezeit_confirm_button.setStyleSheet(confirmbtnstyledisable)

        self.reisezeit_confirm_button.clicked.connect(self.on_confirm_date_selection)

        button_layout.addWidget(self.reisezeit_return_button)
        button_layout.addWidget(self.reisezeit_confirm_button)

        layout.addLayout(button_layout)

        # Seite Reisezeit einrichten
        #########self.reisezeit_page.setLayout(self.reisezeit_page_layout)

        self.setLayout(layout)



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

    def on_validate_date_clicked(self):
        departure_date = self.departure_date_edit.date()
        return_date = self.return_date_edit.date()
        minimum_return_date = departure_date.addDays(5)
        #nights = self.selected_trip_data.get('Übernachtungen')
        #calculated_return_date = self.departure_date_edit.date().addDays(nights)
       #if return_date < calculated_return_date:
        if return_date < minimum_return_date:
            #show_return_date_error("Invalid Return Date","The selected return date is incompatible.",f"The return date must account for the number of nights of your trip.\n"
        #f"The minimum return date should be: {calculated_return_date.toString('dd-MM-yyyy')}.")
            show_return_date_error(
                "Invalid Return Date",
                "The selected return date is incompatible.",
                f"The return date must be at least 5 days after the departure date.\n"
                f"The earliest valid return date is: {minimum_return_date.toString('dd-MM-yyyy')}."
            )
            self.return_date_edit.setDate(minimum_return_date)
            return_date = minimum_return_date

            #return_date = calculated_return_date
            #self.return_date_edit.setDate(return_date)
        departure_date_str = departure_date.toString("dd-MM-yyyy")

        return_date_str = return_date.toString("dd-MM-yyyy")

        self.update_gekauft_container(departure_date_str, return_date_str)
        self.reisezeit_confirm_button.setEnabled(True)
        self.reisezeit_confirm_button.setStyleSheet(confirmbtnstyle)

        print(f"Dates validées : Departure: {departure_date_str}, Return: {return_date}")


    def on_cancel_date_clicked(self):
        self.reset_dates()
        clear_layout(self.gekauft_layout)
        clear_layout(self.date_layout)
        self.departure_date_edit.setDate(QDate(2025, 5, 1))
        self.return_date_edit.setDate(QDate(2025, 5, 2))
        previous_page_index = self.stacked_widget.currentIndex() - 2
        self.stacked_widget.setCurrentIndex(previous_page_index)
        #self.stacked_widget.setCurrentWidget(self.selection_page)


    def update_gekauft_container(self, departure_date, return_date):
        clear_layout(self.date_layout)
        self.gekauft_layout.addWidget(self.trip_details_label)
        departure_label = QLabel(f"<b>Departure Date:</b> {departure_date}")
        return_label = QLabel(f"<b>Return Date:</b> {return_date}")
        departure_label.setStyleSheet("font-size: 16px; margin-bottom: 5px;")
        return_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.date_layout.addWidget(departure_label)
        self.date_layout.addWidget(return_label)
        self.gekauft_layout.addLayout(self.date_layout)
        self.gekauft_scroll_area.setWidget(self.gekauft_container)

    def reset_dates(self):

        default_departure_date = QDate(2025, 5, 1)
        default_return_date = QDate(2025, 5, 2)

        self.departure_date_edit.setDate(default_departure_date)
        self.return_date_edit.setDate(default_return_date)

    def on_back_to_cabin_clicked(self):
        self.cabin_type = None
        self.stacked_widget.setCurrentWidget(self.cabin_page)

    def on_confirm_date_selection(self):

        try:
            self.payment_page = PaymentPage(
                trip_data=self.trip_data,
                cabin_type=self.cabin_type,
                cabin_price=self.cabin_price,
                user_balance= get_user_balance(self.user_name.text()),
                user_name=self.user_name.text(),
                stacked_widget=self.stacked_widget,
                konto_edit=self.konto_edit,
                parent=self
            )
            self.stacked_widget.addWidget(self.payment_page)
            self.stacked_widget.setCurrentWidget(self.payment_page)

        except Exception as e:
            print(f"Err : {e}")

    def update_reisezeit_page(self):

        try:
            if self.city_scroll_area is None:
                self.city_scroll_area = QScrollArea()

            # Reisedetails aktualisieren
            trip_details = (
                f"<b>Trip number:</b> {self.trip_data['Reisenummer']}<br>"
                f"<b>Sea:</b> {self.trip_data['Meerart']}<br>"
                f"<b>Number of nights:</b> {self.trip_data['Übernachtungen']}<br>"
                f"<b>Cities:</b> {self.trip_data['Besuchte_Städte']}<br>"
                f"<b>Ship type:</b> {self.trip_data['Schiffstyp']}<br>"
                f"<b>Selected Cabin:</b> {self.cabin_type}<br>"
                f"<b>Price:</b> {self.cabin_price} €"
            )
            self.trip_details_label.setText(trip_details)
            self.apply_date_restrictions()

            # Bilder von Städten leeren und aktualisieren
            city_layout = QHBoxLayout()
            for city in self.trip_data['Besuchte_Städte'].split(','):
                city = city.strip()
                city_label = QLabel()
                image_path = f"../images/Hafenstaedte/{city}.jpg"
                if os.path.exists(image_path):
                    city_label.setPixmap(QPixmap(image_path).scaled(150, 100, Qt.KeepAspectRatio))
                else:
                    city_label.setText(f"No image for {city}")
                city_label.setAlignment(Qt.AlignCenter)
                city_layout.addWidget(city_label)
            city_widget = QWidget()
            city_widget.setLayout(city_layout)
            self.city_scroll_area.setWidget(city_widget)
            self.city_scroll_area.setFixedHeight(150)

            # Bild des Schiffstyps aktualisieren
            ship_image_path = f"../images/Schiffstypen/Schiffstyp {self.trip_data['Schiffstyp']}.jpg"
            if os.path.exists(ship_image_path):
                self.ship_image_label.setPixmap(QPixmap(ship_image_path).scaled(300, 250, Qt.KeepAspectRatio))
            else:
                self.ship_image_label.setText("No image available")

            # Das Bild der ausgewählten Kabine aktualisieren
            cabin_image_path = f"../images/Kabinentypen/{self.cabin_type}.jpg"
            if os.path.exists(cabin_image_path):
                self.cabin_image_label.setPixmap(
                    QPixmap(cabin_image_path).scaled(300, 250, Qt.KeepAspectRatio))
            else:
                self.cabin_image_label.setText("No cabin selected")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la page Reisezeit : {e}")



    def apply_date_restrictions(self):
        try:
            # Abfahrtstage nach Schiffstyp
            ship_type = self.trip_data.get('Schiffstyp')
            nights = self.trip_data.get('Übernachtungen')
            ship_departure_days = {
                'A': [1],  # Monday
                'B': [2],  # Tuesday
                'C': [3],  # Wednesday
                'D': [4],  # Thursday
                'E': [5],  # Friday
                'F': [6],  # Saturday
                'G': [7],  # Sunday
                'H': [7],  # Sunday
                'I': [7],  # Sunday
                'J': [1, 3],  # First Monday and Wednesday of each month
                'K': [1, 3],  # First Monday and Wednesday of each month
                'X': [1],  # First day of each month
            }

            valid_days = ship_departure_days.get(ship_type, [])
            disabled_format = QTextCharFormat()
            disabled_format.setForeground(QColor(200, 200, 200))  # Grau für ungültige Daten

            enabled_format = QTextCharFormat()
            enabled_format.setForeground(QColor(0, 0, 0))  # Schwarz für gültige Daten

            # Einschränkungen auf den Kalender anwenden
            current_date = QDate(2025, 5, 1)
            while current_date <= QDate(2025, 10, 31):
                if current_date.dayOfWeek() not in valid_days:
                    self.departure_date_edit.calendarWidget().setDateTextFormat(current_date, disabled_format)
                else:
                    # self.departure_date_edit.calendarWidget().setDateTextFormat(current_date, enabled_format)
                    return_date = current_date.addDays(nights)
                    if return_date > QDate(2025, 10, 31):
                        self.departure_date_edit.calendarWidget().setDateTextFormat(current_date, disabled_format)
                    else:
                        self.departure_date_edit.calendarWidget().setDateTextFormat(current_date, enabled_format)

                current_date = current_date.addDays(1)
        except Exception as e:
            print(f"Err: {e}")



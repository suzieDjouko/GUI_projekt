import os
import sys
import pandas as pd
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTableWidget, QPushButton, QComboBox,
    QSpinBox,
    QListWidget, QScrollArea, QGridLayout
)
from PyQt5.QtCore import Qt
from index import loadData_and_clean_data, getSea, filterBySea, filterBySeaAndByNight , display_selected_ship_image ,getVacanciesByNigthRange
from index import load_ship_types , schiffstyp_folder , getImagesForFilteredCities,filter_cities_by_criteria,getImageByCityName
from utiles import clear_layout
from utiles import display_cities_in_grid
from cities_utiles import update_city_selection , populate_cities
from index import update_table , reset_table




class ReiseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sélection de voyages en bateau")
        self.setGeometry(100, 100, 1900, 1200)
        file_path = "../Schiffsreisen.xlsx"

        self.dataFrame = loadData_and_clean_data(file_path)
        self.dataFrame['Meerart'] = self.dataFrame['Meerart'].str.replace(" ", "")

        self.hafenstaedte_folder = "../images/Hafenstaedte"


        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # Section des types de mer
        sea_selection_layout = QHBoxLayout()
        self.sea_combo = QComboBox()
        self.sea_combo.addItem('All Sea')
        self.sea_combo.addItems(getSea(self.dataFrame))
        self.sea_combo.currentTextChanged.connect(self.on_sea_changed)
        sea_selection_layout.addWidget(QLabel("Meerart:"))
        sea_selection_layout.addWidget(self.sea_combo)
        layout.addLayout(sea_selection_layout)

        # Section du nombre de nuits
        nights_layout = QHBoxLayout()
        self.nights_spin = QSpinBox()
        self.nights_spin.setRange(2, 30)
        self.nights_spin.setSuffix(" nights")
        self.nights_spin.valueChanged.connect(self.on_criteria_changed)
        nights_layout.addWidget(QLabel("Anzahl von Übernachtung"))
        nights_layout.addWidget(self.nights_spin)
        layout.addLayout(nights_layout)

        city_label = QLabel('Cities:')
        layout.addWidget(city_label)
        self.city_selection_scroll = QScrollArea()
        self.city_selection_widget = QWidget()  # Container pour les villes
        self.city_selection_layout = QGridLayout(self.city_selection_widget)
        self.city_selection_scroll.setWidget(self.city_selection_widget)
        self.city_selection_scroll.setWidgetResizable(True)
        layout.addWidget(self.city_selection_scroll)
        populate_cities(self.hafenstaedte_folder, self.city_selection_layout)

        #Section des types de navires
        ship_selection_layout = QHBoxLayout()
        self.ship_combo = QComboBox()
        self.ship_combo.addItem("Sélectionnez un type de navire")
        self.load_ship_types2()
        self.ship_combo.currentTextChanged.connect(self.on_ship_selected)

        self.ship_image_label = QLabel()
        self.ship_image_label.setAlignment(Qt.AlignCenter)
        self.ship_image_label.setFixedSize(350, 200)
        self.ship_image_label.setStyleSheet("border: 1px solid black;")

        ship_selection_layout.addWidget(QLabel("Type de navire"))
        ship_selection_layout.addWidget(self.ship_combo)
        ship_selection_layout.addWidget(self.ship_image_label)
        layout.addLayout(ship_selection_layout)

        # Section des types de cabines
        #cabin_selection_layout = QHBoxLayout()
        #self.cabin_combo = QComboBox()
        #self.cabin_combo.addItem("Sélectionnez un type de cabine")
        #self.load_cabin_types()
        #self.cabin_combo.currentTextChanged.connect(self.display_selected_cabin_image)

        self.cabin_image_label = QLabel()
        self.cabin_image_label.setAlignment(Qt.AlignCenter)
        self.cabin_image_label.setFixedSize(300, 200)
        self.cabin_image_label.setStyleSheet("border: 1px solid black;")

        #cabin_selection_layout.addWidget(QLabel("Type de cabine"))
        #cabin_selection_layout.addWidget(self.cabin_combo)
        #cabin_selection_layout.addWidget(self.cabin_image_label)
        #layout.addLayout(cabin_selection_layout)

        # Boutons Réinitialiser et Rechercher
        buttons_layout = QHBoxLayout()
        reset_button = QPushButton("Réinitialiser")
        #reset_button.clicked.connect(self.reset_form)
        search_button = QPushButton("Rechercher")
        #search_button.clicked.connect(self.filter_results)
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(search_button)
        layout.addLayout(buttons_layout)

        #results_label = QLabel("Résultats :")
        #layout.addWidget(results_label)
        #self.results_list = QListWidget()
        #layout.addWidget(self.results_list)

        # Tableau des résultats
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.dataFrame.columns))
        self.table.setHorizontalHeaderLabels(self.dataFrame.columns)
        layout.addWidget(self.table)


        # Configurer la fenêtre principale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        print("Valeurs uniques de la colonne 'Meerart':", self.dataFrame['Meerart'].unique())

    def filter_by_sea(self, selected_sea):
        if self.sea_combo.currentText() == "All Sea" and self.nights_spin.value() ==2:
            update_table(self.table, self.dataFrame)
            # Appliquer le filtre de mer
        else:
            filtered_results = filterBySea(self.dataFrame, selected_sea)
            update_table(self.table, filtered_results)
            print(filtered_results)

        #self.update_ship_image(selected_sea)

    def on_ship_selected(self, ship_name):
        """Fonction pour appeler display_selected_ship_image"""
        display_selected_ship_image(ship_name, self.ship_image_label)

    def load_ship_types2(self):
        """Charge les types de navires dans la barre déroulante."""
        ship_types = load_ship_types(schiffstyp_folder)  # Appel de la fonction importée

        if not ship_types:
            self.ship_combo.addItem("Aucun navire disponible")
            return

        for ship_name in ship_types:
            self.ship_combo.addItem(ship_name)

    def apply_filters(self, sea, nights):
        filtered_data = self.dataFrame
        if sea == "All Sea":
            filtered_data = self.dataFrame

        # Filtre par mer
        if sea != "All Sea":
            self.filter_by_sea(sea)
            #filtered_data = filtered_data[filtered_data['Meerart'] == sea]
            update_city_selection(
                filtered_data, self.hafenstaedte_folder, sea, nights, self.city_selection_layout
            )
            print(f"Données filtrées par mer ({sea}): {len(filtered_data)} lignes")

        # Filtre par nuits
        if nights:
            filtered_data = getVacanciesByNigthRange(filtered_data, nights)
            update_city_selection(
                filtered_data, self.hafenstaedte_folder, sea, nights, self.city_selection_layout
            )
            print(f"Données filtrées par nuits ({nights}): {len(filtered_data)} lignes")

        return filtered_data


    def on_sea_changed(self, sea):
       try:
           print(f"Sea selected: {sea}")
           nights = self.nights_spin.value()
           filtered_data = self.apply_filters(sea, nights)
           # Mettre à jour les sélections de villes (si nécessaire)
           update_city_selection(
               filtered_data, self.hafenstaedte_folder, sea, nights, self.city_selection_layout
           )
           # Mettre à jour le tableau avec les données filtrées
           update_table(self.table, filtered_data)
       except Exception as e:
           print(f"Error in on_sea_changed: {e}")

    def on_criteria_changed(self):
        try:
            sea = self.sea_combo.currentText()
            nights = self.nights_spin.value()
            print(f"Critères mis à jour - Sea: {sea}, Nights: {nights}")
            filtered_data = self.apply_filters(sea, nights)
            # Mettre à jour le tableau avec les données filtrées
            update_city_selection(
                filtered_data, self.hafenstaedte_folder, sea, nights, self.city_selection_layout
            )
            update_table(self.table, filtered_data)
        except Exception as e:
            print(f"Error in on_criteria_changed: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReiseApp()
    window.show()
    sys.exit(app.exec_())

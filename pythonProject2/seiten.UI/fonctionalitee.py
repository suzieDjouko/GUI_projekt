import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMessageBox,
    QTableWidget, QTableWidgetItem, QScrollArea, QGridLayout, QPushButton, QComboBox, QSpinBox, QListWidgetItem,
    QListWidget
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize


from ..backend.index import loadData_and_clean_data



class VoyageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sélection de voyages en bateau")
        self.setGeometry(100, 100, 1900, 1200)

        file_path = "../Schiffsreisen.xlsx"  # Remplacez par le chemin correct
        self.dataFrame = loadData_and_clean_data(file_path)
        if self.dataFrame is not None:
            print(self.dataFrame.head())  # Afficher un aperçu des données nettoyées
        else:
            print("Aucune donnée valide chargée.")
            
            
        # Définir les chemins des dossiers
        self.hafenstaedte_folder = "../images/Hafenstaedte"
        self.schiffstyp_folder = "../images/Schiffstypen"  # Types de navires
        self.cabintype_folder = "../images/Kabinentypen"  # Types de cabines

        # Sélections de l'utilisateur
        self.selected_schiffstyp = None
        self.selected_cities = set()

        # Initialiser l'interface
        self.init_ui()

    


    def init_ui(self):
        layout = QVBoxLayout()

        # Section des types de mer
        sea_selection_layout = QHBoxLayout()
        self.sea_combo = QComboBox()
        self.sea_combo.addItem("All Sea")
        self.sea_combo.addItems(self.dataFrame["Meerart"].unique())
        self.sea_combo.currentTextChanged.connect(self.filter_results)
        sea_selection_layout.addWidget(QLabel("Meer:"))
        sea_selection_layout.addWidget(self.sea_combo)
        layout.addLayout(sea_selection_layout)

        # Section du nombre de nuits
        nights_layout = QHBoxLayout()
        self.nights_spin = QSpinBox()
        #self.nights_save_button = QPushButton('save')
        self.nights_spin.setRange(2, 30)
        self.nights_spin.setValue(2)
        self.nights_spin.setSuffix(" nights")
        nights_layout.addWidget(QLabel("Anzahl von Übernachtung"))
        self.nights_spin.valueChanged.connect(self.filter_results)
        #self.nights_save_button.clicked.connect(self.create_city_selection)
        nights_layout.addWidget(self.nights_spin)
        #nights_layout.addWidget(self.nights_save_button)
        layout.addLayout(nights_layout)

        # Section des villes
        city_label = QLabel('Villes')
        layout.addWidget(city_label)
        city_selection_scroll = self.create_city_selection(self.nights_spin.value)
        layout.addWidget(city_selection_scroll)

        # Section des types de navires
        ship_selection_layout = QHBoxLayout()
        self.ship_combo = QComboBox()
        self.ship_combo.addItem("Sélectionnez un type de navire")
        self.load_ship_types()
        self.ship_combo.currentTextChanged.connect(self.display_selected_ship_image)

        self.ship_image_label = QLabel()
        self.ship_image_label.setAlignment(Qt.AlignCenter)
        self.ship_image_label.setFixedSize(300, 200)
        self.ship_image_label.setStyleSheet("border: 1px solid black;")

        ship_selection_layout.addWidget(QLabel("Type de navire"))
        ship_selection_layout.addWidget(self.ship_combo)
        ship_selection_layout.addWidget(self.ship_image_label)
        layout.addLayout(ship_selection_layout)

        # Section des types de cabines
        cabin_selection_layout = QHBoxLayout()
        self.cabin_combo = QComboBox()
        self.cabin_combo.addItem("Sélectionnez un type de cabine")
        self.load_cabin_types()
        self.cabin_combo.currentTextChanged.connect(self.display_selected_cabin_image)

        self.cabin_image_label = QLabel()
        self.cabin_image_label.setAlignment(Qt.AlignCenter)
        self.cabin_image_label.setFixedSize(300, 200)
        self.cabin_image_label.setStyleSheet("border: 1px solid black;")

        cabin_selection_layout.addWidget(QLabel("Type de cabine"))
        cabin_selection_layout.addWidget(self.cabin_combo)
        cabin_selection_layout.addWidget(self.cabin_image_label)
        layout.addLayout(cabin_selection_layout)

        # Boutons Réinitialiser et Rechercher
        buttons_layout = QHBoxLayout()
        reset_button = QPushButton("Réinitialiser")
        reset_button.clicked.connect(self.reset_form)
        search_button = QPushButton("Rechercher")
        search_button.clicked.connect(self.filter_results)
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(search_button)
        layout.addLayout(buttons_layout)

        results_label = QLabel("Résultats :")
        layout.addWidget(results_label)
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        # Tableau des résultats
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.dataFrame.columns))
        self.table.setHorizontalHeaderLabels(self.dataFrame.columns)
        layout.addWidget(self.table)

        # Configurer la fenêtre principale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_ship_types(self):
        """Charger les types de navires dans la barre déroulante."""
        if not os.path.exists(self.schiffstyp_folder):
            self.ship_combo.addItem("Aucun navire disponible")
            return

        for filename in os.listdir(self.schiffstyp_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                ship_name = filename.split(".")[0]  # Nom sans extension
                self.ship_combo.addItem(ship_name)

    def display_selected_ship_image(self, ship_name):
        """Afficher l'image du navire sélectionné."""
        if ship_name == "Sélectionnez un type de navire" or ship_name == "Aucun navire disponible":
            QMessageBox.warning(self, "Attention", "Aucun type de navire sélectionné.")
            return

        image_path = os.path.join(self.schiffstyp_folder, f"{ship_name}.jpg")
        if not os.path.exists(image_path):  # Si .jpg n'existe pas, chercher d'autres extensions
            for ext in [".png", ".jpeg"]:
                image_path = os.path.join(self.schiffstyp_folder, f"{ship_name}{ext}")
                if os.path.exists(image_path):
                    break
            else:
                image_path = os.path.join(self.schiffstyp_folder, "default.jpg")

                #QMessageBox.warning(self, "Erreur", f"Aucune image trouvée pour le navire : {ship_name}.")
                #return

        pixmap = QPixmap(image_path).scaled(300, 200, Qt.KeepAspectRatio)
        self.ship_image_label.setPixmap(pixmap)

    def load_cabin_types(self):
        """Charger les types de cabines dans la barre déroulante."""
        if not os.path.exists(self.cabintype_folder):
            self.cabin_combo.addItem("Aucune cabine disponible")
            return

        for filename in os.listdir(self.cabintype_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                cabin_name = filename.split(".")[0]  # Nom sans extension
                self.cabin_combo.addItem(cabin_name)

    def display_selected_cabin_image(self, cabin_name):
        """Afficher l'image de la cabine sélectionnée."""
        if cabin_name == "Sélectionnez un type de cabine" or cabin_name == "Aucune cabine disponible":
            QMessageBox.warning(self, "Attention", "Aucun type de cabine sélectionné.")
            return

        image_path = os.path.join(self.cabintype_folder, f"{cabin_name}.jpg")
        if not os.path.exists(image_path):  # Si .jpg n'existe pas, chercher d'autres extensions
            for ext in [".png", ".jpeg"]:
                image_path = os.path.join(self.cabintype_folder, f"{cabin_name}{ext}")
                if os.path.exists(image_path):
                    break
            else:
                image_path = os.path.join(self.schiffstyp_folder, "default.jpg")

            # QMessageBox.warning(self, "Erreur", f"Aucune image trouvée pour la cabine : {cabin_name}.")
                #return

        pixmap = QPixmap(image_path).scaled(300, 200, Qt.KeepAspectRatio)
        self.cabin_image_label.setPixmap(pixmap)

    def create_city_selection(self, selected_nights = None):
        """Créer une section de sélection des villes avec des boutons images."""
        scroll_area = QScrollArea()
        grid_layout = QGridLayout()
        row, col = 0, 0
        selected_nights = self.nights_spin.value() or None
        print(f"Selected nights: {selected_nights}")  # Debug
        #cities = self.dataFrame["Besuchte_Städte"].dropna().unique()
        #cities = set(city.strip() for cities in cities for city in cities.split(","))
       # self.display_unique_cities(filtered_df)
        unique_cities = self.update_city_choice(selected_nights)
        print(f"Unique cities: {unique_cities}")  # Debug

        if not unique_cities:
            print(f"Aucune ville trouvée pour {selected_nights} nuits.")
            no_city_label = QLabel("Aucune ville disponible pour le nombre de nuits sélectionné.")
            no_city_label.setAlignment(Qt.AlignCenter)
            scroll_area.setWidget(no_city_label)
            return scroll_area

        for city in sorted(unique_cities):
           # normalized_city = re.sub(r'\s+', ' ', city.strip())  # Enlever les espaces supplémentaires
            #normalized_city = normalized_city.lower().replace(" ","")  # Transformer en minuscule et enlever les espaces

            image_path = os.path.join(self.hafenstaedte_folder, f"{city}.jpg")


            if not os.path.exists(image_path):
                #print(f"Image not found for city '{city}' (normalized: '{normalized_city}')")
                image_path = os.path.join(self.hafenstaedte_folder, "default.jpg")

            # Créer un bouton image
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setStyleSheet("border: none;")
            btn.setIcon(QIcon(image_path))  # Utilisation de QIcon
            btn.setIconSize(QSize(300, 250))  # Taille de l'image

            # Ajouter un événement de clic pour la sélection
            btn.clicked.connect(lambda _, c=city, b=btn: self.toggle_city_selection(c, b))

            # Ajouter un label sous l'image pour le nom de la ville
            city_layout = QVBoxLayout()
            city_layout.addWidget(btn)
            city_label = QLabel(city)
            city_label.setAlignment(Qt.AlignCenter)
            city_layout.addWidget(city_label)

            # Créer un conteneur pour le bouton et le label
            city_widget = QWidget()
            city_widget.setLayout(city_layout)

            # Ajouter le conteneur au layout
            grid_layout.addWidget(city_widget, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        scroll_widget = QWidget()
        scroll_widget.setLayout(grid_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        return scroll_area



    def toggle_city_selection(self, city_name, btn):
        """Ajouter ou retirer une ville de la sélection et mettre à jour l'apparence."""
        if btn.isChecked():
            self.selected_cities.add(city_name)
            btn.setStyleSheet("border: 2px solid blue; background-color: lightblue;")
        else:
            self.selected_cities.remove(city_name)
            btn.setStyleSheet("border: 1px solid black; background-color: none;")
        self.filter_results()

    def reset_form(self):
        """Réinitialiser tous les choix du formulaire."""
        # Réinitialiser la sélection des mers
        self.sea_combo.setCurrentIndex(0)
        # Réinitialiser le nombre de nuits
        self.nights_spin.setValue(2)

        # Réinitialiser la sélection des villes
        self.selected_cities.clear()
        for btn in self.findChildren(QPushButton):
            if btn.isCheckable():
                btn.setChecked(False)
                btn.setStyleSheet("border: 1px solid black; background-color: none;")

        # Réinitialiser la sélection des types de navires
        self.ship_combo.setCurrentIndex(0)
        self.ship_image_label.clear()  # Effacer l'image du navire sélectionné

        # Réinitialiser la sélection des types de cabines
        self.cabin_combo.setCurrentIndex(0)
        self.cabin_image_label.clear()  # Effacer l'image de la cabine sélectionnée

        # Effacer le tableau des résultats
        self.table.clearContents()
        self.table.setRowCount(0)

    def filter_results(self):
        """Filtrer les résultats en fonction des critères sélectionnés."""
        selected_sea = self.sea_combo.currentText()
        selected_nights = self.nights_spin.value()
        selected_cities = list(self.selected_cities)
        min_nights = selected_nights - 2
        max_nights = selected_nights + 2

        # Appliquer les filtres sur le DataFrame
        filtered_df = self.dataFrame.copy()
        if selected_sea != "All Sea":
            filtered_df = filtered_df[filtered_df["Meerart"] == selected_sea]

        if selected_nights is not None and isinstance(selected_nights, (int, float)):
            filtered_df = filtered_df[(filtered_df["Übernachtungen"] >= min_nights) &
                                      (filtered_df["Übernachtungen"] <= max_nights)]
        else:
            print("Aucune sélection valide pour 'selected_nights'")

        if selected_cities:
            filtered_df = filtered_df[
                filtered_df["Besuchte_Städte"].apply(lambda x: any(city in x for city in selected_cities))
            ]
        if filtered_df.empty:
            print(f"Aucune ville trouvée pour {selected_nights} nuits.")
        else:
            # Afficher les villes trouvées
            print(f"Villes trouvées pour {selected_nights} nuits :")
            print(filtered_df["Besuchte_Städte"].unique())

        # Mettre à jour la liste des résultats
        self.results_list.clear()
        for _, row in filtered_df.iterrows():
            item = QListWidgetItem(
                f"Voyage: {row['ReiseName']} | Mer: {row['Meerart']} | Nuits: {row['Übernachtungen']}")
            self.results_list.addItem(item)

        # Mettre à jour le tableau des résultats
        self.table.setRowCount(len(filtered_df))
        for row_idx, row in enumerate(filtered_df.itertuples(index=False)):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        print(f"Type de selected_nights : {type(selected_nights)}, Valeur : {selected_nights}")

        self.update_table(filtered_df)

        #self.update_table(filtered_df)
        #filtered_cities = self.display_unique_cities(filtered_df)
        #print("Villes uniques :", filtered_cities)

        #self.table.clearContents()

        #self.create_city_selection(selected_nights)

        #print(self.update_city_choice(self.nights_spin.value()))

    def update_city_choice(self, nights=None):
        # nights = self.nights_spin.value()
        if nights:
            print(f"Filtering cities for nights = {nights}")
            filtered_cities = self.dataFrame[self.dataFrame["Übernachtungen"] == nights]["Besuchte_Städte"].dropna().unique()
            # cities = set(city.strip() for cities in filtered_cities for city in cities.split(","))
            # return cities
        else:
            filtered_cities = self.dataFrame["Besuchte_Städte"].dropna().unique()
            # cities = set(city.strip() for cities in cities for city in cities.split(","))
            # return cities
        cities = set(city.strip() for cities in filtered_cities for city in cities.split(","))
        return cities



    def update_table(self, dataFrame):
        """Mettre à jour le tableau avec les résultats filtrés."""
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setRowCount(len(dataFrame))
        self.table.setColumnCount(len(dataFrame.columns))
        self.table.setHorizontalHeaderLabels(dataFrame.columns)

        for i, row in dataFrame.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def show_error(self, message):
        """Afficher un message d'erreur."""
        QMessageBox.critical(self, "Erreur", message)

    def display_unique_cities(self, filtered_df):

        #   la function extrait et retourne une liste de villes unique a partir d'une dataframe filtree
        unique_cities_list = []

        # Parcourir les lignes du DataFrame
        for _, row in filtered_df.iterrows():
            cities = row['Besuchte_Städe'].split(",")  # Séparer les villes par la virgule
            for city in cities:
                if city.strip() not in unique_cities_list:  # Éviter les doublons et gérer les espaces
                    unique_cities_list.append(city.strip())

        # Mise à jour de l'affichage dans la QListWidget
        #self.results_list.clear()  # Supposons que results_list est un QListWidget
        if unique_cities_list:
            for city in unique_cities_list:
                self.results_list.addItem(QListWidgetItem(f"Ville unique : {city}"))
        else:
            self.results_list.addItem(QListWidgetItem("Aucune ville trouvée."))

        # Retourner la liste des villes uniques
        return unique_cities_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoyageApp()
    window.show()
    sys.exit(app.exec_())

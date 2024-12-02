import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMessageBox,
    QTableWidget, QTableWidgetItem, QScrollArea, QGridLayout, QPushButton, QComboBox, QSpinBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize


class VoyageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sélection de voyages en bateau")
        self.setGeometry(100, 100, 1200, 800)

        # Charger les données Excel
        self.data_file = "../Schiffsreisen_cleaned.xlsx"  # Remplacez par le chemin correct
        self.df = None  # Initialisation des données
        self.load_data()

        # Définir les chemins des dossiers
        self.schiffstyp_folder = "../images/Schiffstypen"  # Types de navires
        self.cabintype_folder = "../images/Kabinentypen"  # Types de cabines

        # Sélections de l'utilisateur
        self.selected_schiffstyp = None
        self.selected_cities = set()

        # Initialiser l'interface
        self.init_ui()

    def load_data(self):
        """Charger les données depuis l'Excel et les nettoyer."""
        try:
            self.df = pd.read_excel(self.data_file)
            self.df["Meerart"] = self.df["Meerart"].fillna("Inconnu").astype(str)
            self.df["Besuchte_Städte"] = self.df["Besuchte_Städte"].fillna("Inconnu").astype(str)
            self.df["Übernachtungen"] = self.df["Übernachtungen"].fillna(0).astype(int)
        except FileNotFoundError:
            self.show_error(f"Fichier introuvable : {self.data_file}")
        except Exception as e:
            self.show_error(f"Impossible de charger les données : {e}")

    def init_ui(self):
        layout = QVBoxLayout()

        # Section des types de mer
        sea_selection_layout = QHBoxLayout()
        self.sea_combo = QComboBox()
        self.sea_combo.addItem("Toutes")
        self.sea_combo.addItems(self.df["Meerart"].unique())
        self.sea_combo.currentTextChanged.connect(self.on_sea_combo_changed)
        sea_selection_layout.addWidget(QLabel("Mer:"))
        sea_selection_layout.addWidget(self.sea_combo)
        layout.addLayout(sea_selection_layout)

        # Section du nombre de nuits
        nights_layout = QHBoxLayout()
        self.nights_spin = QSpinBox()
        self.nights_spin.setRange(1, 30)
        self.nights_spin.valueChanged.connect(self.on_night_spin_changed)
        nights_layout.addWidget(QLabel("Nombre de nuits:"))
        nights_layout.addWidget(self.nights_spin)
        layout.addLayout(nights_layout)

        # Section des villes
        layout.addWidget(QLabel("Villes"))
        city_selection_scroll = self.create_city_selection()
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

        # Tableau des résultats
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)
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
                QMessageBox.warning(self, "Erreur", f"Aucune image trouvée pour le navire : {ship_name}.")
                return

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
                QMessageBox.warning(self, "Erreur", f"Aucune image trouvée pour la cabine : {cabin_name}.")
                return

        pixmap = QPixmap(image_path).scaled(300, 200, Qt.KeepAspectRatio)
        self.cabin_image_label.setPixmap(pixmap)

    def create_city_selection(self):
        """Créer une section de sélection des villes avec des boutons images."""
        scroll_area = QScrollArea()
        grid_layout = QGridLayout()

        row, col = 0, 0

        #self.df_filtred_by_night = self.filter_by_night()

        unique_cities = self.df["Besuchte_Städte"].dropna().unique()
        cities = set(city.strip() for cities in unique_cities for city in cities.split(","))

        for city in sorted(cities):
            # Créer un bouton image
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setStyleSheet("border: none;")
            btn.setIcon(QIcon(f"../images/Hafenstaedte/{city}.jpg"))  # Utilisation de QIcon
            btn.setIconSize(QSize(100, 100))  # Taille de l'image

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

    def reset_form(self):
        """Réinitialiser tous les choix du formulaire."""
        # Réinitialiser la sélection des mers
        self.sea_combo.setCurrentIndex(0)

        # Réinitialiser le nombre de nuits
        self.nights_spin.setValue(1)

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
        sea = self.sea_combo.currentText()
        nights = self.nights_spin.value()
        cities = self.selected_cities

        filtered_df = self.df.copy()

        if sea != "Toutes":
            filtered_df = filtered_df[filtered_df["Meerart"] == sea]

        filtered_df = filtered_df[(filtered_df["Übernachtungen"] >= (nights - 2)) &
                                  (filtered_df["Übernachtungen"] <= (nights + 2))]

        if cities:
            filtered_df = filtered_df[filtered_df["Besuchte_Städte"].apply(
                lambda x: all(city in (x or "") for city in cities))]

        self.update_table(filtered_df)

    def update_table(self, df):
        """Mettre à jour le tableau avec les résultats filtrés."""
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def show_error(self, message):
        """Afficher un message d'erreur."""
        QMessageBox.critical(self, "Erreur", message)


    def filter_by_sea(self, selected_sea, dataframe):
        """
        Filtre le DataFrame en fonction de la sélection du ComboBox.

        :param selected_sea: str, sélection actuelle du ComboBox.
                             Peut être "Toutes" ou une valeur spécifique.
        :param dataframe: pd.DataFrame, tableau de données à filtrer.
        :return: pd.DataFrame, tableau filtré.
        """
        if selected_sea == "Toutes":
            # Ne filtre pas, retourne tout le tableau
            return dataframe
        else:
            # Filtre le tableau en fonction de la colonne 'Meerart'
            return dataframe[dataframe["Meerart"] == selected_sea]

    def on_sea_combo_changed(self):
        selected_sea = self.sea_combo.currentText()
        filtered_df = self.filter_by_sea(selected_sea, self.df)
        # Vous pouvez utiliser filtered_df pour mettre à jour l'affichage
        print(filtered_df)  # Debug ou mettre à jour un tableau PyQt

    def filter_by_night(self, selected_night, dataframe):
        """
        Filtre le DataFrame en fonction du nombre de nuits ±2 nuits.

        :param selected_night: int, le nombre de nuits sélectionné par l'utilisateur.
        :param dataframe: pd.DataFrame, le DataFrame contenant les données des voyages.
        :return: pd.DataFrame, le DataFrame filtré.
        """
        # Définir la plage pour le filtrage
        min_nuits = max(1, selected_night - 2)  # Minimum de 1 pour éviter les valeurs négatives
        max_nuits = selected_night + 2

        # Filtrer le DataFrame en fonction de la plage
        dataframe_filtré = dataframe[
            (dataframe["Übernachtungen"] >= min_nuits) &
            (dataframe["Übernachtungen"] <= max_nuits)
            ]

        return dataframe_filtré

    def on_night_spin_changed(self):
        """
        Met à jour le DataFrame filtré lorsque la valeur du QSpinBox change.
        """
        selected_night = self.nights_spin.value()
        # Première étape : filtrer par la mer sélectionnée
        selected_sea = self.sea_combo.currentText()
        dataframe_filtré_par_mer = self.filter_by_sea(selected_sea, self.df)
        # Deuxième étape : filtrer par le nombre de nuits
        dataframe_final = self.filter_by_night(selected_night, dataframe_filtré_par_mer)
        # Mettre à jour l'affichage ou afficher les données filtrées
        print(dataframe_final)  # Debug ou mise à jour d'un tableau dans PyQt


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoyageApp()
    window.show()
    sys.exit(app.exec_())

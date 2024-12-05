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
            self.df = self.df[self.df["Meerart"].notna()]
            self.df["Meerart"] = self.df["Meerart"].astype(str)
            self.df = self.df[self.df["Besuchte_Städte"].notna()]
            self.df["Besuchte_Städte"] = self.df["Besuchte_Städte"].astype(str)
            self.df["Übernachtungen"] = self.df["Übernachtungen"].fillna(0).astype(int)
        except FileNotFoundError:
            self.show_error(f"Fichier introuvable : {self.data_file}")
        except Exception as e:
            self.show_error(f"Impossible de charger les données : {e}")

    def init_ui(self):
        layout = QVBoxLayout()

        # Section du type de mer
        sea_selection_layout = QHBoxLayout()
        self.sea_combo = QComboBox()
        self.sea_combo.addItem("Toutes")
        self.sea_combo.addItems(self.df["Meerart"].unique())
        self.sea_combo.currentTextChanged.connect(self.on_filters_changed)
        sea_selection_layout.addWidget(QLabel("Type de mer :"))
        sea_selection_layout.addWidget(self.sea_combo)
        layout.addLayout(sea_selection_layout)

        # Section pour le nombre de nuits
        nights_layout = QHBoxLayout()
        self.nights_spin = QSpinBox()
        self.nights_spin.setRange(0, 30)  # Inclure 0 comme état "non défini"
        self.nights_spin.setSpecialValueText("Non défini")  # Afficher "Non défini" lorsque la valeur est 0
        self.nights_spin.setValue(0)  # Définir la valeur initiale à "non défini"
        self.nights_spin.valueChanged.connect(self.on_filters_changed)
        nights_layout.addWidget(QLabel("Nombre de nuits :"))
        nights_layout.addWidget(self.nights_spin)
        layout.addLayout(nights_layout)

        # Section des villes
        layout.addWidget(QLabel("Villes :"))
        self.city_selection_widget = self.create_city_selection()
        self.city_scroll_area = QScrollArea()
        self.city_scroll_area.setWidget(self.city_selection_widget)
        self.city_scroll_area.setWidgetResizable(True)
        layout.addWidget(self.city_scroll_area)

        self.setLayout(layout)

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
                ship_name = filename.split(" ")[-1].split(".")[0]  # Exemple: "A" de "Schiffstyp A.jpg"

                #ship_name = filename.split(".")[0]  # Nom sans extension
                self.ship_combo.addItem(ship_name)

    def display_selected_ship_image(self, ship_name):
        """
        Afficher l'image du navire sélectionné, uniquement si le navire
        est disponible dans les résultats filtrés.
        """
        # Obtenir les résultats filtrés
        filtered_results = self.get_filtered_results()
        available_ships = filtered_results['Schiffstyp'].unique()

        # Vérifier si le navire sélectionné est dans les résultats filtrés
        if ship_name not in available_ships:
            return

        # Charger l'image correspondante
        image_path = os.path.join(self.schiffstyp_folder, f"Schiffstyp {ship_name}.jpg")
        if not os.path.exists(image_path):  # Si .jpg n'existe pas, chercher d'autres extensions
            for ext in [".png", ".jpeg"]:
                image_path = os.path.join(self.schiffstyp_folder, f"{ship_name}{ext}")
                if os.path.exists(image_path):
                    break

        # Afficher l'image
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

    def get_filtered_results(self):
        # Obtenir les valeurs des filtres
        selected_night = self.nights_spin.value()
        selected_sea = self.sea_combo.currentText()
        df_filtered = self.df

        # Filtrer par mer
        if selected_sea != "Toutes":
            df_filtered = self.filter_by_sea(selected_sea, df_filtered)

        # Filtrer par nuit si défini
        if selected_night != 0:
            df_filtered = self.filter_by_night(selected_night, df_filtered)
        #si au moins une ville dans la colone 'Besuchte Stadte
        if self.selected_cities:
            df_filtered = df_filtered[df_filtered["Besuchte_Städte"].apply(
                lambda cities: any(city in self.selected_cities for city in cities.split(",")))]

        return df_filtered

    def create_city_selection(self):
        """
        Crée la section de sélection des villes avec des boutons image.
        Les villes sont générées dynamiquement en fonction des résultats filtrés.
        """
        grid_layout = QGridLayout()
        row, col = 0, 0

        df_filtered = self.get_filtered_results()

        # Extraire les villes uniques
        unique_cities = df_filtered["Besuchte_Städte"].dropna().unique()
        cities = set(city.strip() for cities in unique_cities for city in cities.split(","))

        for city in sorted(cities):
            # Créer un bouton image
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setStyleSheet("border: none;")

            btn.setIcon(QIcon(f"../images/Hafenstaedte/{city}.jpg"))  # Chemin des images
            btn.setIconSize(QSize(120, 120))  # Taille de l'image

            # Ajouter un événement de clic
            btn.clicked.connect(lambda _, c=city, b=btn: self.toggle_city_selection(c, b))

            # Ajouter un label sous le bouton
            city_layout = QVBoxLayout()
            city_layout.addWidget(btn)
            city_label = QLabel(city)
            city_label.setAlignment(Qt.AlignCenter)
            city_layout.addWidget(city_label)

            # Conteneur pour chaque ville
            city_widget = QWidget()
            city_widget.setLayout(city_layout)

            # Ajouter à la grille
            grid_layout.addWidget(city_widget, row, col)
            col += 1
            if col > 3:  # 4 colonnes max
                col = 0
                row += 1

        # Retourner le conteneur
        scroll_widget = QWidget()
        scroll_widget.setLayout(grid_layout)
        return scroll_widget

    def on_filters_changed(self):
        """
        Méthode appelée lorsque les filtres (mer, nuits, villes) changent.
        Actualise l'affichage des villes et des types de bateaux.
        """
        try:
            print("Filtres modifiés, mise à jour des villes et des bateaux...")
           # self.update_city_buttons()

            # Actualiser les villes
            self.city_scroll_area.takeWidget()
            self.city_selection_widget = self.create_city_selection()
            self.city_scroll_area.setWidget(self.city_selection_widget)

            print("Villes mises à jour")

            # Actualiser les types de navires
            self.update_ship_types()

            print("Types de navires mis à jour")

        except Exception as e:
            print(f"Erreur lors de la mise à jour des filtres : {e}")

    def toggle_city_selection(self, city_name, btn):
        """Ajouter ou retirer une ville de la sélection et mettre à jour l'apparence."""
        if btn.isChecked():
            self.selected_cities.add(city_name)
            self.update_ship_types()
            btn.setStyleSheet("border: 2px solid blue; background-color: lightblue;")
        else:
            self.selected_cities.remove(city_name)
            self.update_ship_types()
            btn.setStyleSheet("border: 1px solid black; background-color: none;")

        print(self.selected_cities)

        return self.selected_cities


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
        dataframe_filtre = dataframe[
            (dataframe["Übernachtungen"] >= min_nuits) &
            (dataframe["Übernachtungen"] <= max_nuits)
            ]

        return dataframe_filtre

    def on_night_spin_changed(self):
        """
        Met à jour le DataFrame filtré lorsque la valeur du QSpinBox change.
        """
        selected_night = self.nights_spin.value()
        # Première étape : filtrer par la mer sélectionnée
        selected_sea = self.sea_combo.currentText()
        dataframe_filtre_par_mer = self.filter_by_sea(selected_sea, self.df)
        # Deuxième étape : filtrer par le nombre de nuits
        dataframe_final = self.filter_by_night(selected_night, dataframe_filtre_par_mer)
        # Mettre à jour l'affichage ou afficher les données filtrées
        print(dataframe_final)  # Debug ou mise à jour d'un tableau dans PyQt
        self.city_selection_widget = self.create_city_selection()
        #self.layout().addWidget(self.city_selection_widget)  # Actualiser dans le layout
        #return dataframe_final

    def update_ship_types(self):
        """Met à jour les types de bateaux dans le combo en fonction des filtres."""
        try:
            self.ship_combo.clear()
            self.ship_combo.addItem("Sélectionnez un type de navire")

            df_filtered = self.get_filtered_results()
            available_ships = df_filtered['Schiffstyp'].unique()

            # Vider la combo des types de navires et y ajouter uniquement ceux disponibles

            for ship in available_ships:
                self.ship_combo.addItem(ship)
            """
            selected_cities = self.selected_cities
            if not selected_cities:
                self.load_ship_types()  # Si aucune ville n'est sélectionnée, charger tous les navires
                return

            print("Mise à jour des types de navires...")
             # Récupérer les résultats filtrés
            filtered_df = self.get_filtered_results()
            print(f"Data filtrée : {filtered_df}")

            # Obtenir les types de navires uniques dans les résultats filtrés
            available_ships = set(filtered_df["Schiffstyp"].dropna().unique())
            print(f"Navires disponibles : {available_ships}")

            # Vider le combo et réinitialiser
            self.ship_combo.clear()
            self.ship_combo.addItem("Sélectionnez un type de navire")

            # Ajouter les navires filtrés (ou tous si aucun filtre n'est appliqué)
            if available_ships:
                self.ship_combo.addItems(sorted(available_ships))
            else:
                self.ship_combo.addItem("Aucun navire disponible")
            print("Types de navires ajoutés au combo.")
            """

        except Exception as e:
            print(f"Erreur dans la mise à jour des types de navires : {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoyageApp()
    window.show()
    sys.exit(app.exec_())

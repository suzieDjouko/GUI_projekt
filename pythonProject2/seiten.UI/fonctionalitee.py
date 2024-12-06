import sys
import os
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMessageBox,
    QTableWidget, QTableWidgetItem, QScrollArea, QGridLayout, QPushButton, QComboBox, QSpinBox, QSizePolicy, QLineEdit,
    QSpacerItem, QStackedWidget
)
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from styles import *
from database_action import get_user_balance


class VoyageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BlauWelle")
        self.setGeometry(100, 100, 1700, 1300)

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
        self.setStyleSheet(
            """
            QLabel{
                font-size:20px;
                }
            QLineEdit{
                font-size:24px;
                border: none;
                background-color:transparent;
            }
                }""")
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        spacer = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.headerLayout = QHBoxLayout()
        self.headerLayout.setContentsMargins(10, 10, 10, 10)

        # logo de l'application
        self.header_logo_label = QLabel()
        self.header_logo_label.setFixedSize(60, 60)
        self.header_logo = QPixmap("../icon/logo_schiff.png")
        self.header_logo_label.setStyleSheet(""" 
                   QLabel{ 
                       background-color:blue;
                       border:none;
                       border-radius:30px;
                       padding: 10px;
                       }
                   """)
        self.header_logo_label.setPixmap(self.header_logo)
        self.header_logo_label.setScaledContents(True)

        # USER
        self.header_user_layout = QHBoxLayout()
        self.header_user_layout.setContentsMargins(10, 10, 10, 10)
        self.header_user_layout.setSpacing(20)
        # Espacement flexible entre les widgets


        self.header_user_logo_btn = QPushButton()
        self.header_user_logo_btn.setIcon(QIcon("../icon/userlogo.svg"))
        self.header_user_logo_btn.setIconSize(QSize(50, 50))
        self.header_user_logo_btn.setFixedSize(60, 60)
        self.header_user_logo_btn.setStyleSheet(
            """
            QPushButton{
                border: none;
                border-radius: 30px;
                padding: 10px;

            }
            QPushButton:hover{
                background-color: green;             
            }
            """
        )
        # self.header_user_logo_btn.clicked.connect(self.handle_modify_profile)
        self.header_user_name_edit = QLineEdit()
        self.header_user_name_edit.setText("Username:")
        self.header_user_name_edit.setFixedHeight(40)
        #self.header_user_name_edit.setStyleSheet("QLineEdit {font-size: 24px; border: none; background: transparent;}")
        self.header_user_name_edit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.header_user_name_edit.setReadOnly(True)
        self.header_user_name_edit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.header_user_name_edit.setMinimumWidth(140)

        # add user Widdget
        self.header_user_layout.addWidget(self.header_user_logo_btn)
        self.header_user_layout.addWidget(self.header_user_name_edit)

        # KONTOSTAND
        self.header_kontostand_layout = QHBoxLayout()
        self.header_kontostand_layout.setSpacing(30)
        self.header_kontostand_layout.setContentsMargins(0, 0, 0, 0)
        self.header_kontostand_label = QLabel("Kontostand:")
        self.header_kontostand_label.setStyleSheet("QLabel {font-size: 24px;}")
        self.header_kontostand_label.setFixedHeight(40)
        self.header_kontostand_label.setMinimumWidth(130)

        self.kontostand_amont_edit = QLineEdit()
        self.kontostand_amont_edit.setStyleSheet("QLineEdit {font-size: 20px;}")
        self.kontostand_amont_edit.setText("0.00 €")
        self.kontostand_amont_edit.setFixedHeight(40)
        self.kontostand_amont_edit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.kontostand_amont_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.header_kontostand_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.kontostand_amont_edit.setMinimumWidth(120)

        self.kontostand_amont_logo_label = QLabel()
        self.kontostand_amont_logo_label.setFixedSize(60, 60)
        self.kontostand_amont_logo = QPixmap("../icon/reshot-icon-stack-of-coins.svg")
        self.kontostand_amont_logo_label.setPixmap(self.kontostand_amont_logo)
        self.kontostand_amont_logo_label.setScaledContents(True)
        # add Kontostand
        self.header_kontostand_layout.addWidget(self.header_kontostand_label, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.header_kontostand_layout.addWidget(self.kontostand_amont_edit)
        self.header_kontostand_layout.addWidget(self.kontostand_amont_logo_label)
        # LOGOUT
        self.header_logo_logout_button = QPushButton()
        self.header_logo_logout_button.setIcon(QIcon("../icon/logout.svg"))
        self.header_logo_logout_button.setIconSize(QSize(50, 50))
        self.header_logo_logout_button.setFixedSize(60, 60)
        self.header_logo_logout_button.setStyleSheet(
            """
            QPushButton{
                border: none;
                border-radius: 30px;
                padding: 10px;

            }
            QPushButton:hover{
                background-color: #D0292C;             
            }
            """
        )
        self.header_logo_logout_button.clicked.connect(self.close)

        self.headerLayout.setSpacing(30)
        self.headerLayout.addWidget(self.header_logo_label, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addLayout(self.header_user_layout)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addLayout(self.header_kontostand_layout)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addWidget(self.header_logo_logout_button)

        #self.setLayout(self.headerLayout)


        # MENU
        self.menuLayout = QHBoxLayout()
        self.menuLayout.setContentsMargins(0, 0, 0, 30)
        self.menuLayout.setSpacing(1)

        self.menu_selection_pushbutton = QPushButton("Selection")
        self.menu_result_pushbutton = QPushButton("Result")
        self.menu_cabins_pushbutton = QPushButton("Cabins")
        self.menu_payment_pushbutton = QPushButton("Payment")

        menu_buttons = [
            self.menu_selection_pushbutton,
            self.menu_result_pushbutton,
            self.menu_cabins_pushbutton,
            self.menu_payment_pushbutton,
        ]
        for button in menu_buttons:
            button.setStyleSheet(menu_style)
            self.menuLayout.addWidget(button)

        self.stacked_widget = QStackedWidget(self)

        # Créez les pages
        self.selection_page = QWidget()
        self.result_page = QWidget()
        self.cabins_page = QWidget()
        self.payment_page = QWidget()

        self.stacked_widget.addWidget(self.selection_page)
        self.stacked_widget.addWidget(self.result_page)
        self.stacked_widget.addWidget(self.cabins_page)
        self.stacked_widget.addWidget(self.payment_page)
        self.stacked_widget.setCurrentWidget(self.selection_page)
        #main_layout.addWidget(self.stacked_widget)
        self.stacked_widget.setCurrentWidget(self.selection_page)

        self.menu_selection_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.selection_page))
        self.menu_result_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.result_page))
        self.menu_cabins_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.cabins_page))
        self.menu_payment_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.payment_page))


        ##PAGE SELECTION

        selection_layout = QVBoxLayout()

        # Section du type de mer
        sea_selection_layout = QHBoxLayout()
        sea_selection_layout.setContentsMargins(0, 0, 0, 20)
        self.sea_combo = QComboBox()
        self.sea_combo.setStyleSheet(style_box)
        self.sea_combo.addItem("All")
        self.sea_combo.addItems(self.df["Meerart"].unique())
        self.sea_combo.currentTextChanged.connect(self.on_filters_changed)
        sea_selection_layout.addWidget(QLabel("Type of Sea :"))
        sea_selection_layout.addWidget(self.sea_combo)
        selection_layout.addLayout(sea_selection_layout)

        # Section pour le nombre de nuits
        nights_layout = QHBoxLayout()
        nights_layout.setContentsMargins(0, 0, 0, 30)

        self.nights_spin = QSpinBox()
        self.nights_spin.setStyleSheet(style_box)
        self.nights_spin.setRange(0, 30)  # Inclure 0 comme état "non défini"
        self.nights_spin.setSpecialValueText("undefine")  # Afficher "Non défini" lorsque la valeur est 0
        self.nights_spin.setValue(0)  # Définir la valeur initiale à "non défini"
        self.nights_spin.valueChanged.connect(self.on_filters_changed)
        nights_layout.addWidget(QLabel("Number of Nights :"))
        nights_layout.addWidget(self.nights_spin)
        #selection_layout.addLayout(self.nights_spin)
        selection_layout.addLayout(nights_layout)

        # Section des villes
        #selection_layout = QVBoxLayout()
        city_title = QLabel("Cities: ")
       # city_title.setObjectName("city_title")
        selection_layout.addWidget(city_title)
    
        self.city_selection_widget = self.create_city_selection()
        self.city_scroll_area = QScrollArea()
        self.city_scroll_area.setContentsMargins(0, 0, 0, 30)
        self.city_scroll_area.setWidget(self.city_selection_widget)
        self.city_scroll_area.setWidgetResizable(True)
        self.city_scroll_area.verticalScrollBar().setStyleSheet(city_section_style)
        selection_layout.addWidget(self.city_scroll_area)

        #self.selection_page.setLayout(selection_layout)

        # Section des types de navires
        ship_selection_layout = QHBoxLayout()
        self.ship_combo = QComboBox()
        self.ship_combo.setStyleSheet(style_box)
        self.ship_combo.addItem("Choose a Ship")
        self.load_ship_types()
        self.ship_combo.currentTextChanged.connect(self.display_selected_ship_image)


        self.ship_image_label = QLabel()
        self.ship_image_label.setFixedSize(300, 250)
        self.ship_image_label.setAlignment(Qt.AlignCenter)
        self.ship_image_label.setStyleSheet("border: 1px solid #60a698;")


        ship_selection_layout.addWidget(QLabel("Type of Ship: "))
        ship_selection_layout.addWidget(self.ship_combo)
        ship_selection_layout.addWidget(self.ship_image_label)
        selection_layout.addLayout(ship_selection_layout)


        # Boutons Réinitialiser et Rechercher
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 50, 0, 80)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_form)
        reset_button.setStyleSheet(reset_button_style)

        search_button = QPushButton("Search")
        search_button.setStyleSheet(search_button_style)

        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(search_button)

        selection_layout.addLayout(buttons_layout)


        ##PAGE RESULT

        self.result_layout = QVBoxLayout()





        # FOOTER
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 30, 40)

        self.footer_prev_button = QPushButton()
        self.footer_prev_button.setIcon(QIcon("../icon/reshot-icon-rewind.svg"))
        self.footer_prev_button.setIconSize(QSize(140, 40))
        self.footer_prev_button.setContentsMargins(0, 0, 0, 0)
        self.footer_prev_button.setStyleSheet(footer_prev_style)

        self.footer_next_button = QPushButton()
        self.footer_next_button.setIcon(QIcon('../icon/reshot-icon-fast-forward.svg'))
        self.footer_next_button.setIconSize(QSize(140, 40))
        self.footer_next_button.setStyleSheet(footer_next_style)

        #self.footer_prev_button.clicked.connect(self.on_previous_button_click)
        #self.footer_next_button.clicked.connect(self.on_next_button_click)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 30, 40)

        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.footer_prev_button)
        self.footer_layout.addSpacing(100)
        self.footer_layout.addWidget(self.footer_next_button)
        self.setLayout(self.footer_layout)


        main_layout = QVBoxLayout()
        main_layout.addLayout(self.headerLayout)
        main_layout.addLayout(self.menuLayout)
        self.selection_page.setLayout(selection_layout)
        self.result_page.setLayout(self.result_layout)

        main_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(self.footer_layout)

        # Configurer la fenêtre principale
        container = QWidget()
        container.setContentsMargins(20,20,20,20)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_result_table(self):
        # Créer un tableau pour afficher les résultats des voyages
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)  # Par exemple, 1 pour le numéro de voyage, 1 pour la mer, etc.
        self.result_table.setHorizontalHeaderLabels(
            ["Reisenummer", "Meerart", "Übernachtungen", "Innenkabine", "Aussenkabine", "Balkonkabine",
             "Luxuskabine Kategorie1", "Luxuskabine Kategorie2", "Luxuskabine Kategorie3"])

        # Ajouter les voyages filtrés dans le tableau
        filtered_results = self.get_filtered_results()

        # Parcours des voyages filtrés
        for index, row in filtered_results.iterrows():
            reisenummer = row["Reisenummer"]
            meerart = row["Meerart"]
            uebernachtungen = row["Übernachtungen"]
            cabin_prices = row[
                ["Innenkabine", "Aussenkabine", "Balkonkabine", "Luxuskabine Kategorie1", "Luxuskabine Kategorie2",
                 "Luxuskabine Kategorie3"]]

            # Ajouter une ligne dans le tableau
            row_position = self.result_table.rowCount()
            self.result_table.insertRow(row_position)

            # Ajouter les données du voyage dans chaque cellule de la ligne
            self.result_table.setItem(row_position, 0, QTableWidgetItem(str(reisenummer)))
            self.result_table.setItem(row_position, 1, QTableWidgetItem(meerart))
            self.result_table.setItem(row_position, 2, QTableWidgetItem(str(uebernachtungen)))

            # Ajouter les prix de chaque cabine et désactiver celles qui sont inaccessibles
            for i, price in enumerate(cabin_prices):
                kontostand = get_user_balance(self.header_user_name_edit)  # Fonction qui retourne le solde de l'utilisateur
                cell = QTableWidgetItem(str(price))
                if price > kontostand:
                    cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)  # Désactiver la cellule
                    cell.setBackground(
                        QColor(200, 200, 200))  # Couleur pour signaler que la cabine n'est pas sélectionnable
                self.result_table.setItem(row_position, i + 3, cell)

        # Ajouter le tableau à votre layout

        self.result_layout.addWidget(self.result_table)
        self.result_page.setLayout(self.result_layout)

    def update_result_page(self):
        # Effacer l'ancienne table
        self.result_table.setRowCount(0)
        # Ajouter de nouvelles lignes pour les résultats filtrés
        self.create_result_table()

    def load_ship_types(self):
        """Charger les types de navires dans la barre déroulante."""
        if not os.path.exists(self.schiffstyp_folder):
            self.ship_combo.addItem("No ship available")
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

        pixmap = QPixmap(image_path).scaled(300, 250, Qt.KeepAspectRatio)
        self.ship_image_label.resize(300, 250)

        self.ship_image_label.setPixmap(pixmap)


    def get_filtered_results(self):
        # Obtenir les valeurs des filtres
        selected_night = self.nights_spin.value()
        selected_sea = self.sea_combo.currentText()
        df_filtered = self.df.copy()

        # Filtrer par mer
        if selected_sea != "All"and "Meerart" in df_filtered.columns:
            df_filtered = self.filter_by_sea(selected_sea, df_filtered)

        # Filtrer par nuit si défini
        if selected_night != 0 and "Übernachtungen" in df_filtered.columns:
            df_filtered = self.filter_by_night(selected_night, df_filtered)
        #si au moins une ville dans la colone 'Besuchte Stadte
        if self.selected_cities and "Besuchte_Städte" in df_filtered.columns:
            def match_cities(cities):
                if not isinstance(cities, str):  # Sécurité contre les valeurs non textuelles
                    return False
                return any(city.strip() in self.selected_cities for city in cities.split(","))

            df_filtered = df_filtered[df_filtered["Besuchte_Städte"].apply(match_cities)]

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
            btn.setStyleSheet(city_section_style)

            btn.setIcon(QIcon(f"../images/Hafenstaedte/{city}.jpg"))  # Chemin des images

            btn.setIconSize(QSize(300, 250))  # Taille de l'image

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


            btn.setStyleSheet("border: 2px solid blue; background-color: lightblue;")
        else:
            self.selected_cities.remove(city_name)
            btn.setStyleSheet("border: 1px solid black; background-color: none;")

        self.update_ship_types()

        print(f"Villes sélectionnées : {self.selected_cities}")



    def reset_form(self):
        """Réinitialiser tous les choix du formulaire."""
        # Réinitialiser la sélection des mers
        self.sea_combo.setCurrentIndex(0)

        # Réinitialiser le nombre de nuits
        self.nights_spin.setSpecialValueText("undefine")
        self.nights_spin.setValue(0)

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
        #self.cabin_combo.setCurrentIndex(0)
        #self.cabin_image_label.clear()  # Effacer l'image de la cabine sélectionnée

        # Effacer le tableau des résultats
        #self.table.clearContents()
        #self.table.setRowCount(0)


    def show_error(self, message):
        """Afficher un message d'erreur."""
        QMessageBox.critical(self, "Erreur", message)


    def filter_by_sea(self, selected_sea, dataframe):

        #if selected_sea == "All":
            # Ne filtre pas, retourne tout le tableau

           # return dataframe
       # else:
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
        selected_sea = self.sea_combo.currentText()
        dataframe_filtre_par_mer = self.filter_by_sea(selected_sea, self.df)
        dataframe_final = self.filter_by_night(selected_night, dataframe_filtre_par_mer)
        print(dataframe_final)
        self.city_selection_widget = self.create_city_selection()

    def update_ship_types(self):
        """Met à jour les types de bateaux dans le combo en fonction des filtres."""
        if not self.selected_cities and self.sea_combo.currentText() == "All" and self.nights_spin.specialValueText() =="undefine" :
            filtered_results = self.df  # Pas de filtres appliqués
        else:
            filtered_results = self.get_filtered_results()

        self.ship_combo.clear()
        self.ship_combo.addItem("Choose a Ship")

            # Obtenir les types de navires uniques dans les résultats filtrés
        available_ships = filtered_results["Schiffstyp"].dropna().unique()

        # Vider et recharger les options dans le QComboBox

        if len(available_ships) == 0:
            self.ship_combo.addItem("No ship available")
        else:
            for ship_type in available_ships:
                self.ship_combo.addItem(ship_type)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoyageApp()
    window.show()
    sys.exit(app.exec_())

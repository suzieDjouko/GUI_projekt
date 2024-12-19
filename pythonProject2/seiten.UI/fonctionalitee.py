import sys
import os
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMessageBox,
     QScrollArea, QGridLayout, QComboBox, QSpinBox, QSizePolicy, QLineEdit,
    QSpacerItem, QStackedWidget, QFrame, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt,QSize
from styles import *
from database_action import *


class VoyageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BlauWelle")
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Redimensionner la fenêtre à 80% de la taille de l'écran
        self.resize(int(screen_width * 0.8), int(screen_height * 0.8))  # Convertir en entiers

        # Définir les dimensions minimales pour éviter que la fenêtre ne devienne trop petite
        self.setMinimumSize(800, 600)

        # Charger les données Excel
        self.data_file = "../Schiffsreisen_cleaned.xlsx"  # Remplacez par le chemin correct
        self.load_data()

        # Définir les chemins des dossiers
        self.schiffstyp_folder = "../images/Schiffstypen"  # Types de navires
        # Sélections de l'utilisateur
        self.ship_combo = QComboBox(self)
        self.selected_cities = set()

        # Initialiser l'interface
        self.init_ui()

    def load_data(self):
        """Charger les données depuis le fichier Excel, vérifier les colonnes et nettoyer les données."""
        try:
            # Charger les données
            self.df = pd.read_excel(self.data_file)

            # Vérifier la présence des colonnes nécessaires
            expected_columns = [
                "Meerart","Übernachtungen", "Besuchte_Städte", "Schiffstyp",
                "Innenkabine", "Aussenkabine", "Balkonkabine",
                "Luxuskabine1", "Luxuskabine2", "Luxuskabine3"
            ]
            missing_columns = [col for col in expected_columns if col not in self.df.columns]
            if missing_columns:
                self.show_error(f"Colonnes manquantes : {', '.join(missing_columns)}")
                return

            # Supprimer les lignes entièrement vides
            self.df = self.df.dropna(how='all')

            # Remplacer "nicht vorhanden" par NaN dans les colonnes de cabines
            cabine_columns = [
                "Innenkabine", "Aussenkabine", "Balkonkabine",
                "Luxuskabine1", "Luxuskabine2", "Luxuskabine3"
            ]
            for col in cabine_columns:
                if col in self.df.columns:
                    self.df[col] = self.df[col].replace("nicht vorhanden", 0)

                    # Conversion des colonnes en types appropriés
            type_mappings = {
                "Übernachtungen": int,
                "Meerart": str,
                "Besuchte_Städte": str,
                "Schiffstyp": str,
                "Innenkabine": int,
                "Aussenkabine": int,
                "Balkonkabine": int,
                "Luxuskabine1": int,
                "Luxuskabine2": int,
                "Luxuskabine3": int,
            }
            for col, dtype in type_mappings.items():
                if col in self.df.columns:
                    # Convertir les colonnes numériques en entier
                    if dtype == int:
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0).astype(int)
                    else:
                        self.df[col] = self.df[col].astype(dtype)

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
        self.cabin_page = QWidget()
        self.payment_page = QWidget()

        self.stacked_widget.addWidget(self.selection_page)
        self.stacked_widget.addWidget(self.result_page)
        self.stacked_widget.addWidget(self.cabin_page)
        self.stacked_widget.addWidget(self.payment_page)
        self.stacked_widget.setCurrentWidget(self.selection_page)
        #main_layout.addWidget(self.stacked_widget)
        self.stacked_widget.setCurrentWidget(self.selection_page)

        self.menu_selection_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.selection_page))
        self.menu_result_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.result_page))
        self.menu_cabins_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.cabin_page))
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
        self.city_scroll_area = QScrollArea()
        self.city_selection_widget = self.create_city_selection()
        self.city_scroll_area.setContentsMargins(0, 0, 0, 30)
        self.city_scroll_area.setWidget(self.city_selection_widget)
        self.city_scroll_area.setWidgetResizable(True)
        self.city_scroll_area.verticalScrollBar().setStyleSheet(city_section_style)
        selection_layout.addWidget(self.city_scroll_area)

        #self.selection_page.setLayout(selection_layout)

        # Section des types de navires
        ship_selection_layout = QHBoxLayout()
        ship_selection_layout.setContentsMargins(0, 0, 0, 20)
        #self.ship_combo = QComboBox()
        self.ship_combo.addItem("Choose a Ship")
        self.load_ship_types()
        self.ship_combo.setStyleSheet(style_box)
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
        search_button.clicked.connect(self.on_search_button_clicked)
        search_button.setStyleSheet(search_button_style)

        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(search_button)

        selection_layout.addLayout(buttons_layout)


        ##PAGE RESULT
        self.result_layout = QVBoxLayout()
        self.result_label = QLabel("List of Trips:")
        self.result_layout.addWidget(self.result_label)
        self.result_list = QListWidget()
        self.result_list.setStyleSheet(Qlist_style)
        self.result_layout.addWidget(self.result_list)
        self.return_button = QPushButton("Return")
        self.return_button.setStyleSheet(back_button_style)
        self.return_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.selection_page))
        self.result_layout.addWidget(self.return_button)

        self.result_page.setLayout(self.result_layout)

        #PAGE CABINES
        #self.cabintype_folder = "../images/Kabinentypen"

        self.cabin_layout = QVBoxLayout()

        self.cabin_summary_label = QLabel()
        self.cabin_summary_label.setAlignment(Qt.AlignTop)
        self.cabin_summary_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        #self.cabin_layout.addWidget(self.cabin_summary_label)
        back_button = QPushButton("Return")
        back_button.setStyleSheet(back_button_style)
        back_button.clicked.connect(self.on_back_to_results_clicked)  # Connecter au retour

        self.cabin_scroll_area = QScrollArea()
        self.cabin_scroll_area.setWidgetResizable(True)

        cabin_content_widget = QWidget()
        cabin_content_widget.setLayout(self.cabin_layout)

        self.cabin_scroll_area.setWidget(cabin_content_widget)

        cabin_page_layout = QVBoxLayout()
        cabin_page_layout.addWidget(self.cabin_summary_label)
        cabin_page_layout.addWidget(self.cabin_scroll_area)
        cabin_page_layout.addWidget(back_button)
        self.cabin_page.setLayout(cabin_page_layout)



        #PAGE PAYEMENT
        self.payment_layout = QVBoxLayout()

        # Payment Page Title
        self.payment_label = QLabel("Payment")
        self.payment_label.setAlignment(Qt.AlignCenter)
        self.payment_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.payment_layout.addWidget(self.payment_label)

        # Payment Details Section
        self.payment_details_layout = QVBoxLayout()

        # Add Cabin Details
        self.cabin_details_label = QLabel()
        self.cabin_details_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.payment_details_layout.addWidget(self.cabin_details_label)

        # Add Total Price Label
        self.total_price_label = QLabel("Total Price: €0")
        self.total_price_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green; margin-bottom: 20px;")
        self.payment_details_layout.addWidget(self.total_price_label)

        # Add Payment Details Layout to the Main Layout
        self.payment_layout.addLayout(self.payment_details_layout)

        # Payment Methods Section
        self.payment_methods_label = QLabel("Choose a Payment Method:")
        self.payment_methods_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.payment_layout.addWidget(self.payment_methods_label)

        # Payment Methods Dropdown
        self.payment_methods_combo = QComboBox()
        self.payment_methods_combo.addItems(["Credit Card", "PayPal", "Bank Transfer"])
        self.payment_methods_combo.setStyleSheet("font-size: 14px; padding: 5px; margin-bottom: 20px;")
        self.payment_layout.addWidget(self.payment_methods_combo)

        # Buttons Section
        self.payment_buttons_layout = QHBoxLayout()

        # Back Button
        self.payment_back_button = QPushButton("Return")
        self.payment_back_button.setStyleSheet(back_button_style)
        self.payment_back_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.cabin_page))  # Navigate back
        self.payment_buttons_layout.addWidget(self.payment_back_button)

        # Proceed to Payment Button
        self.proceed_button = QPushButton("Proceed to Payment")
        self.proceed_button.setStyleSheet(
            """
            background-color: green; 
            color: white; 
            font-size: 14px; 
            padding: 10px;
            border-radius: 8px;
            """
        )
        self.proceed_button.clicked.connect(self.process_payment)  # Implement payment processing
        self.payment_buttons_layout.addWidget(self.proceed_button)

        # Add Buttons Layout to Main Payment Layout
        self.payment_layout.addLayout(self.payment_buttons_layout)

        # Set Layout for the Payment Page
        self.payment_page.setLayout(self.payment_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.headerLayout)
        main_layout.addLayout(self.menuLayout)
        self.selection_page.setLayout(selection_layout)


        self.payment_page.setLayout(self.payment_layout)

        main_layout.addWidget(self.stacked_widget)


        # Configurer la fenêtre principale
        container = QWidget()
        container.setContentsMargins(20, 20, 20, 20)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def get_filtered_results(self):

        # Obtenir les valeurs des filtres
        df_filtered = self.df.copy()

        # Filtrer par mer
        selected_sea = self.sea_combo.currentText()

        if selected_sea != "All":
            df_filtered = self.filter_by_sea(selected_sea, df_filtered)

        # Filtrer par nuit si défini
        selected_night = self.nights_spin.value()
        if selected_night != 0:
            df_filtered = self.filter_by_night(selected_night, df_filtered)
        #si au moins une ville dans la colone 'Besuchte Stadte

        #fiter bei Ship
        selected_ship = self.ship_combo.currentText()
        if selected_ship and selected_ship != "Choose a Ship":
            df_filtered = self.filter_by_ship(selected_ship, df_filtered)

        if self.selected_cities:
            def match_cities(cities):
                if not isinstance(cities, str):  # Sécurité contre les valeurs non textuelles
                    return False
                return any(city.strip() in self.selected_cities for city in cities.split(","))

            df_filtered = df_filtered[df_filtered["Besuchte_Städte"].apply(match_cities)]

        print(f"Filtrage par Meerart : {selected_sea}")
        print(f"Filtrage par Übernachtungen : {selected_night}")
        print(f"Villes sélectionnées : {self.selected_cities}")

        return df_filtered

    def process_payment(self):
        try:
            selected_method = self.payment_methods_combo.currentText()
            total_price_text = self.total_price_label.text().strip()
            print(f"Total Price Label Text: {total_price_text}")

            if "Total Price: €" in total_price_text:
                total_price = int(total_price_text.replace("Total Price: €", "").strip())
            else:
                QMessageBox.warning(self, "Error", "Unable to retrieve the total price.")
                return

            print(f"Parsed Total Price: {total_price} €")

            username = self.header_user_name_edit.text()
            user_balance = get_user_balance(username)
            print(f"User balance: {user_balance} €")

            if user_balance is None:
                QMessageBox.warning(self, "Error", "User not found.")
                return

            if total_price > user_balance:
                QMessageBox.warning(self, "Error", "Insufficient balance.")
                return

            # Deduct from balance and update the database
            new_balance = user_balance - total_price
            update_user_balance(username, new_balance)
            self.kontostand_amont_edit.setText(f"{new_balance} €")

            QMessageBox.information(
                self, "Payment Successful",
                f"Your payment of {total_price} € using {selected_method} was successful."
            )
        except Exception as e:
            print(f"Error in process_payment: {e}")

    def add_result_item_with_cabins(self, row_data):
        """
        Add a trip to the QListWidget with details on one line and a "Choose" button aligned to the right.
        """
        try:
            # Get the user's balance (if needed for future enhancements)
            user_balance = get_user_balance(self.header_user_name_edit.text())
            print(f"User balance: {user_balance} €")  # Debugging

            # Create a QWidget to represent the trip
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(5, 5, 5, 5)

            # Format trip details as a single string
            visited_cities = row_data.get("Besuchte_Städte", "Unknown")
            trip_details_text = (
                f"Trip {row_data['Reisenummer']}: {row_data['Meerart']}, "
                f"{row_data['Übernachtungen']} nights,  cities: {visited_cities}"
            )
            trip_details_label = QLabel(trip_details_text)
            trip_details_label.setStyleSheet("font-size: 18px;")
            trip_details_label.setWordWrap(False)  # Keep it on one line
            item_layout.addWidget(trip_details_label)

            # Add spacer to push the button to the right
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            item_layout.addItem(spacer)

            # Add the "Choose" button
            choose_button = QPushButton("Choose")
            choose_button.setFixedSize(150, 40)
            choose_button.setStyleSheet(choose_button_style)
            choose_button.clicked.connect(lambda: self.on_choose_button_clicked(row_data))
            item_layout.addWidget(choose_button)

            # Add the widget to the QListWidget
            list_item = QListWidgetItem(self.result_list)
            list_item.setSizeHint(item_widget.sizeHint())  # Adjust the size to fit content
            self.result_list.addItem(list_item)
            self.result_list.setItemWidget(list_item, item_widget)

            print(f"Added: {trip_details_text}")
        except Exception as e:
            print(f"Error adding item: {e}")

    def display_result_table(self, filtered_data):
        """Display filtered trips in the QListWidget with details on one line."""
        self.result_list.clear()  # Reset the list

        if filtered_data.empty:
            self.result_label.setText("No results found.")
            return

        # Add each trip to the list
        for _, row_data in filtered_data.iterrows():
            self.add_result_item_with_cabins(row_data)

        self.result_label.setText("Results found:")

    def on_cabin_selected(self, cabin_type, cabin_price):
        """Gère la sélection d'une cabine par l'utilisateur."""
        QMessageBox.information(
            self,
            "Cabine Sélectionnée",
            f"Vous avez sélectionné la cabine {cabin_type} pour {cabin_price} €."
        )
        # Naviguer vers la page de paiement ou effectuer d'autres actions
        self.stacked_widget.setCurrentWidget(self.payment_page)
        self.update_payment_page(cabin_type, cabin_price)

    def reset_cabin_page(self):
        """Réinitialiser la page des cabines."""
        self.clear_layout(self.cabin_layout)
        self.cabin_summary_label.clear()

    def on_back_to_results_clicked(self):
        self.stacked_widget.setCurrentWidget(self.result_page)  # Naviguer vers la page des résultats

    def clear_layout(self, layout):
        """Supprime tous les widgets d'un layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_search_button_clicked(self):
        filtered_results = self.get_filtered_results()
        self.display_result_table(filtered_results)
        self.stacked_widget.setCurrentWidget(self.result_page)

    def on_choose_button_clicked(self, row_data):
        """Gère la sélection d'un voyage par l'utilisateur."""
        # Afficher un message de confirmation
        # Afficher les images des cabines pour ce voyage
        self.clear_layout(self.cabin_layout)
        summary = (
            f"<b>Reise Nummer :</b> {row_data['Reisenummer']}<br>"
            f"<b>Meerart :</b> {row_data['Meerart']}<br>"
            f"<b>Nombre de nuits :</b> {row_data['Übernachtungen']}<br>"
            f"<b>Schiffstyp :</b> {row_data['Schiffstyp']}"
        )
        self.cabin_summary_label.setText(summary)

        self.stacked_widget.setCurrentWidget(self.cabin_page)

        self.display_cabin_images(row_data)

    def display_cabin_images(self, row_data):
        self.clear_layout(self.cabin_layout)

        cabin_details = {
            "Innenkabine": "Comfortable and budget-friendly, ideal for travelers seeking functionality.",
            "Aussenkabine": "Bright and serene with a porthole view of the sea.",
            "Balkonkabine": "Enjoy fresh air and an open view from your private balcony.",
            "Luxuskabine1": "Luxurious and spacious, including premium services.",
            "Luxuskabine2": "Elegant with a private lounge and minibar, perfect for exceptional trips.",
            "Luxuskabine3": "Ultimate luxury with a large space, jacuzzi, and exclusive concierge service."
        }

        user_balance = get_user_balance(self.header_user_name_edit.text())  # Get user balance dynamically

        for cabin_type, description in cabin_details.items():
            cabin_price = row_data.get(cabin_type, "not available")  # Retrieve cabin price or "not available"
            image_path = self.get_cabin_image_path(cabin_type)  # Retrieve the image path for the cabin

            # Display cabin image and information
            cabin_layout = QHBoxLayout()

            # Cabin image
            image_label = QLabel()
            if image_path:
                image_label.setPixmap(QPixmap(image_path).scaled(380, 250, Qt.KeepAspectRatio))  # Appropriate size
            else:
                image_label.setText("Image not available")
            cabin_layout.addWidget(image_label)

            # Cabin information
            info_layout = QVBoxLayout()
            name_label = QLabel(f"<b>{cabin_type}</b>")
            name_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 5px;")
            info_layout.addWidget(name_label)

            # Cabin description
            characteristics_label = QLabel(description)
            characteristics_label.setStyleSheet("font-size: 18px; margin-top: 5px; margin-bottom: 10px;")
            info_layout.addWidget(characteristics_label)

            # Display price
            if  cabin_price == 0:
                # Price not available
                price_label = QLabel("Price: Not Available")
                price_label.setStyleSheet("font-size: 20px; color: gray;")
                info_layout.addWidget(price_label)
            else:
                # Price available
                price_label = QLabel(f"{cabin_price} €")
                if cabin_price > user_balance:
                    # Insufficient balance
                    price_label.setStyleSheet("font-size: 20px; color: red;")
                    balance_label = QLabel("Insufficient balance")
                    balance_label.setStyleSheet("font-size: 14px; color: red;")
                    info_layout.addWidget(price_label)
                    info_layout.addWidget(balance_label)
                else:
                    # Sufficient balance
                    price_label.setStyleSheet("font-size: 16px; color: green;")
                    info_layout.addWidget(price_label)

            # Add "Pay" button
            choose_button = QPushButton("Pay")
            choose_button.setFixedSize(120, 50)
            if cabin_price == 0 or cabin_price > user_balance:
                choose_button.setEnabled(False)
                choose_button.setStyleSheet(
                    "background-color: lightgray; color: gray; border-radius: 8px; padding: 10px; font-size:16px"
                )
                if cabin_price == 0:
                    choose_button.setToolTip("Price not available")
                else:
                    choose_button.setToolTip("Insufficient balance")
            else:
                choose_button.setStyleSheet(
                    "background-color: #007bff; color: white; border-radius: 8px; padding: 10px; font-size:16px"
                )
                choose_button.clicked.connect(lambda _, ct=cabin_type, cp=cabin_price: self.on_cabin_selected(ct, cp))
            info_layout.addWidget(choose_button, alignment=Qt.AlignRight)

            cabin_layout.addLayout(info_layout)

            # Add the cabin layout to the main cabin layout
            cabin_widget = QWidget()
            cabin_widget.setLayout(cabin_layout)
            self.cabin_layout.addWidget(cabin_widget)

            # Add a horizontal separator
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.cabin_layout.addWidget(separator)

    def get_cabin_image_path(self, cabin_type):
        cabin_images= {
            "Innenkabine":"../images/Kabinentypen/Innenkabine.JPG",
            "Aussenkabine": "../images/Kabinentypen/Aussenkabine.JPG",
            "Balkonkabine": "../images/Kabinentypen/Balkonkabine.JPG",
            "Luxuskabine1": "../images/Kabinentypen/Luxuskabine Kategorie 1.jpg",
            "Luxuskabine2": "../images/Kabinentypen/Luxuskabine Kategorie 2.jpg",
            "Luxuskabine3": "../images/Kabinentypen/Luxuskabine Kategorie 3.jpg",
        }
        image_path = cabin_images.get(cabin_type)
        if image_path and os.path.exists(image_path):
            return image_path
        else:
            return None

    #def on_cabin_selected(self, cabin_type, cabin_price):

        # Switch to the payment page
        #self.stacked_widget.setCurrentWidget(self.payment_page)

        # Update payment page details (optional, based on your payment page design)
        #self.update_payment_page(cabin_type, cabin_price)

    def update_payment_page(self, cabin_type, cabin_price):
        """
        Update payment page details with selected cabin and price.
        """
        # Update cabin details label
        self.cabin_details_label.setText(
            f"<b>Selected Cabin:</b> {cabin_type}<br>"
            f"<b>Price:</b> {cabin_price} €"
        )

        # Update total price label
        self.total_price_label.setText(f"Total Price: {cabin_price} €")

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

        extensions = [".jpeg", ".JPG"]
        image_path = None

        for ext in extensions:
            path = os.path.join(self.schiffstyp_folder, f"Schiffstyp {ship_name}{ext}")
            if os.path.exists(path):
                image_path = path
                break  # Trouvé, on sort de la boucle
        # Si aucune image trouvée, retourner sans rien faire
        if not image_path:
            return
        # Charger et afficher l'image
        pixmap = QPixmap(image_path).scaled(300, 250, Qt.KeepAspectRatio)
        self.ship_image_label.setPixmap(pixmap)

    def create_city_selection(self):
        """
        Crée la section de sélection des villes avec des boutons image.
        Les villes sont générées dynamiquement en fonction des résultats filtrés.
        """
        grid_layout = QGridLayout()
        row, col = 0, 0

        df_filtered = self.get_filtered_results()
        print(df_filtered)

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
            btn.setStyleSheet(city_section_style)

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

            # Actualiser les villes
            self.city_scroll_area.takeWidget()
            self.city_selection_widget = self.create_city_selection()
            self.city_scroll_area.setWidget(self.city_selection_widget)

            print("Villes mises à jour")
            filtered_results = self.get_filtered_results()
            self.display_result_table(filtered_results)

            # Actualiser les types de navires
            self.update_ship_types()


        except Exception as e:
            print(f"Erreur lors de la mise à jour des filtres : {e}")

    def toggle_city_selection(self, city_name, btn):
        """Ajouter ou retirer une ville de la sélection et mettre à jour l'apparence."""
        if btn.isChecked():
            self.selected_cities.add(city_name)
        else:
            self.selected_cities.remove(city_name)
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
        self.result_list.clear()
        self.ship_image_label.clear()  # Effacer l'image du navire sélectionné




    def show_error(self, message):
        QMessageBox.critical(self, "Erreur", message)


    def filter_by_sea(self, selected_sea, dataframe):
        if selected_sea == "All":
            return dataframe
        return dataframe[dataframe["Meerart"] == selected_sea]

    def filter_by_ship(self, selected_ship, dataframe):
        return dataframe if not selected_ship or selected_ship == "Choose a Ship" else dataframe[
            dataframe["Schiffstyp"].str.contains(selected_ship, na=False, case=False)]

    def filter_by_night(self, selected_night, dataframe):
        min_nuits = max(1, selected_night - 2)  # Minimum de 1 pour éviter les valeurs négatives
        max_nuits = selected_night + 2

        # Filtrer le DataFrame en fonction de la plage
        dataframe_filtre = dataframe[
            (dataframe["Übernachtungen"] >= min_nuits) &
            (dataframe["Übernachtungen"] <= max_nuits)
            ]
        print(dataframe_filtre)
        return dataframe_filtre

    def update_ship_types(self):
        """Met à jour les types de bateaux dans le combo en fonction des filtres."""
        filtered_results = self.get_filtered_results()  # Toujours récupérer les résultats filtrés
        available_ships = filtered_results["Schiffstyp"].dropna().unique()

        self.ship_combo.clear()
        self.ship_combo.addItem("Choose a Ship")

        if not available_ships.size:  # Vérifie si la liste est vide
            self.ship_combo.addItem("No ship available")
        else:
            for ship_type in available_ships:
                self.ship_combo.addItem(ship_type)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoyageApp()
    window.show()
    sys.exit(app.exec_())

import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout,
    QScrollArea, QComboBox, QSpinBox, QSizePolicy, QLineEdit,
    QSpacerItem, QStackedWidget, QFrame, QListWidget, QListWidgetItem, QLabel, QWidget, QVBoxLayout, QGridLayout,
    QPushButton
)



from styles import *
from database_action import *
from functionen import *
from checking_funktion import *

from user_info import UserInfoWindow
from reisezeit import ReisezeitPage





class TravelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BlauWelle")
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Die Größe des Fensters auf 80% der Bildschirmgröße ändern
        self.setMinimumSize(int(screen_width * 0.4), int(screen_height * 0.4))

        self.resize(int(screen_width * 0.8), int(screen_height * 0.8))


        # Excel-Daten laden
        self.data_file = "../Schiffsreisen_cleaned.xlsx"  # Remplacez par le chemin correct
        self.df = load_data(self.data_file, self)

        # Ordnerpfade festlegen
        self.schiffstyp_folder = "../images/Schiffstypen"  # Types de navires
        # Sélections de l'utilisateur
        self.ship_combo = QComboBox(self)
        self.selected_cities = set()

        # Schnittstelle initialisieren
        self.init_ui()


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

        # logo App
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

        # Flexible Abstände zwischen Widgets
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
        self.header_user_logo_btn.clicked.connect(lambda: [
            self.on_user_logo_clicked(),
            self.stacked_widget.setCurrentWidget(self.user_profil)
        ])
        self.header_user_name_edit = QLineEdit()
        self.header_user_name_edit.setText("Username:")
        self.header_user_name_edit.setFixedHeight(40)
        #self.header_user_name_edit.setStyleSheet("QLineEdit {font-size: 24px; border: none; background: transparent;}")
        self.header_user_name_edit.setFocusPolicy(Qt.NoFocus)
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
        self.header_kontostand_label.setMinimumWidth(110)

        self.kontostand_amont_edit = QLineEdit()
        self.kontostand_amont_edit.setStyleSheet("QLineEdit {font-size: 20px;}")
        self.kontostand_amont_edit.setText("0.00 €")
        self.kontostand_amont_edit.setFixedHeight(40)
        self.kontostand_amont_edit.setFocusPolicy(Qt.NoFocus)
        self.kontostand_amont_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.header_kontostand_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.kontostand_amont_edit.setMinimumWidth(120)

        self.kontostand_amont_logo_label = QLabel()
        self.kontostand_amont_logo_label.setFixedSize(60, 60)
        self.kontostand_amont_logo = QPixmap("../icon/reshot-icon-stack-of-coins.svg")
        self.kontostand_amont_logo_label.setPixmap(self.kontostand_amont_logo)
        self.kontostand_amont_logo_label.setScaledContents(True)
        # add Kontostand
        self.header_kontostand_layout.addWidget(self.header_kontostand_label, alignment=Qt.AlignmentFlag.AlignVCenter)
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
        self.headerLayout.addWidget(self.header_logo_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addLayout(self.header_user_layout)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addLayout(self.header_kontostand_layout)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addWidget(self.header_logo_logout_button)

        # MENU

        # Erstellen Sie die Seiten

        self.stacked_widget = QStackedWidget(self)

        self.selection_page = QWidget()
        self.result_page = QWidget()
        self.cabin_page = QWidget()
        self.user_profil = UserInfoWindow()
        self.user_profil.return_callback = lambda: self.stacked_widget.setCurrentWidget(self.selection_page)


        self.stacked_widget.addWidget(self.selection_page)
        self.stacked_widget.addWidget(self.result_page)
        self.stacked_widget.addWidget(self.cabin_page)

        self.stacked_widget.addWidget(self.user_profil)


        self.stacked_widget.setCurrentWidget(self.selection_page)

        self.menuLayout = QHBoxLayout()
        self.menuLayout.setContentsMargins(0, 0, 0, 30)
        self.menuLayout.setSpacing(1)

        self.menu_selection_pushbutton = QPushButton("Selection")
        self.menu_result_pushbutton = QPushButton("Result")
        self.menu_cabins_pushbutton = QPushButton("Cabins")
        self.menu_reisezeit_pushbutton = QPushButton("Reisezeit")
        self.menu_payment_pushbutton = QPushButton("Payment")

        menu_buttons = [
            self.menu_selection_pushbutton,
            self.menu_result_pushbutton,
            self.menu_cabins_pushbutton,
            self.menu_reisezeit_pushbutton,
            self.menu_payment_pushbutton,
        ]
        for button in menu_buttons:
            button.setStyleSheet(menu_style)
            self.menuLayout.addWidget(button)


        self.menu_selection_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.selection_page))
        self.menu_result_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.result_page))
        self.menu_cabins_pushbutton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.cabin_page))

        ##AUSWAHLSEITE

        selection_layout = QVBoxLayout()


        # Sektion Seetyps
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

        # Sektion Anzahl der Nächte
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

        # Sektion Städte
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

        # Sektion Schiffstypen
        ship_selection_layout = QHBoxLayout()
        ship_selection_layout.setContentsMargins(0, 0, 0, 20)
        #self.ship_combo = QComboBox()
        self.ship_combo.addItem("Choose a Ship")
        self.load_ship_types()
        self.ship_combo.setStyleSheet(style_box)
        self.ship_combo.currentTextChanged.connect(self.display_selected_ship_image)


        self.ship_image_label = QLabel()
        self.ship_image_label.setFixedSize(250, 200)
        self.ship_image_label.setAlignment(Qt.AlignCenter)
        self.ship_image_label.setStyleSheet("border: 1px solid #60a698;")


        ship_selection_layout.addWidget(QLabel("Type of Ship: "))
        ship_selection_layout.addWidget(self.ship_combo)
        ship_selection_layout.addWidget(self.ship_image_label)
        selection_layout.addLayout(ship_selection_layout)

        # Schaltflächen Zurücksetzen und Suchen
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


        ##SEITE ERGEBNIS
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

        #SEITE KABINEN
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

        # SEITE DATUMSAUSWAHL


        #PAYEMENT
        self.payment_layout = QVBoxLayout()

        self.total_price_label = QLabel("Total Price: €0")

        self.payment_layout.addWidget(self.total_price_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.headerLayout)
        main_layout.addLayout(self.menuLayout)
        self.selection_page.setLayout(selection_layout)


        main_layout.addWidget(self.stacked_widget)
        # Configurer la fenêtre principale
        container = QWidget()
        container.setContentsMargins(20, 20, 20, 20)
        container.setLayout(main_layout)
        self.setCentralWidget(container)


    def get_filtered_results(self):

            # Filterwerte erhalten
            df_filtered = self.df.copy()

            # Nach Meer filtern
            selected_sea = self.sea_combo.currentText()

            if selected_sea != "All":
                df_filtered = self.filter_by_sea(selected_sea, df_filtered)

            # Nach Nacht filtern, falls festgelegt
            selected_night = self.nights_spin.value()
            if selected_night != 0:
                df_filtered = self.filter_by_night(selected_night, df_filtered)
            #wenn mindestens eine Stadt in der Spalte „Besuchte Städte“ enthalten ist

            #fiter bei ship
            self.selected_ship = self.ship_combo.currentText()
            if self.selected_ship and self.selected_ship != "Choose a Ship":
                df_filtered = self.filter_by_ship(self.selected_ship, df_filtered)

            if self.selected_cities:
                def match_cities(cities):
                    if not isinstance(cities, str):  # Sicherheit vor nicht-textuellen Werten
                        return False
                    return any(city.strip() in self.selected_cities for city in cities.split(","))

                df_filtered = df_filtered[df_filtered["Besuchte_Städte"].apply(match_cities)]

            print(f"Filtrage par Meerart : {selected_sea}")
            print(f"Filtrage par Übernachtungen : {selected_night}")
            print(f"Villes sélectionnées : {self.selected_cities}")

            return df_filtered
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
            visited_cities = row_data.get("Besuchte_Städte")
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

    def on_pay_clicked(self, cabin_type, cabin_price, row_data):
        try:
            self.selected_cabin_type = cabin_type
            self.selected_cabin_price = cabin_price
            self.trip_data = row_data
            self.user_balance = get_user_balance(self.header_user_name_edit.text())

            # Créer une nouvelle instance de ReisezeitPage avec les données à jour
            reisezeit_page = ReisezeitPage(
                trip_data=self.trip_data,
                cabin_type=self.selected_cabin_type,
                cabin_price=self.selected_cabin_price,
                user_balance=self.user_balance,
                user_name=self.header_user_name_edit,
                stacked_widget=self.stacked_widget,
                konto_edit=self.kontostand_amont_edit,
                payment_page=None,
                cabin_page=self.cabin_page,
            )
            reisezeit_page.update_reisezeit_page()

            self.stacked_widget.addWidget(reisezeit_page)
            self.menu_reisezeit_pushbutton.clicked.connect(
                lambda: self.stacked_widget.setCurrentWidget(reisezeit_page))

            self.stacked_widget.setCurrentWidget(reisezeit_page)

        except Exception as e:
            print(f"Error in on_pay_clicked: {e}")


    def on_back_to_results_clicked(self):
        self.stacked_widget.setCurrentWidget(self.result_page)

    def on_search_button_clicked(self):
        filtered_results = self.get_filtered_results()
        self.display_result_table(filtered_results)
        self.stacked_widget.setCurrentWidget(self.result_page)

    def on_choose_button_clicked(self, row_data):
        """Verwaltet die Auswahl einer Reise durch den Nutzer."""
        # Zeige eine Bestätigungsnachricht
        # Zeige Bilder der Kabinen für diese Reise

        self.selected_cabin_type = None

        trip_details = (
            f"<b>Trip number:</b> {row_data['Reisenummer']}<br>"
            f"<b>Sea:</b> {row_data['Meerart']}<br>"
            f"<b>Number of nights:</b> {row_data['Übernachtungen']}<br>"
            f"<b>Cities:</b> {row_data['Besuchte_Städte']}<br>"
            f"<b>Ship type:</b> {row_data['Schiffstyp']}"
        )
        self.cabin_summary_label.setText(trip_details)

        self.selected_trip_data = row_data


        self.display_selected_ship_image(row_data['Schiffstyp'])
        self.display_cabin_images(row_data)
        self.stacked_widget.setCurrentWidget(self.cabin_page)


    def display_cabin_images(self, row_data):
        clear_layout(self.cabin_layout)

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
            cabin_price = row_data.get(cabin_type, "not available")  # Kabinenpreis abrufen oder „nicht verfügbar“
            image_path = get_cabin_image_path(cabin_type)  # Abrufen des Bildpfads für die Kabine

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
            if cabin_price == 0:
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
            pay_button = QPushButton("Pay")
            pay_button.setFixedSize(120, 50)
            if cabin_price == 0 or cabin_price > user_balance:
                pay_button.setEnabled(False)
                pay_button.setStyleSheet(
                    "background-color: lightgray; color: gray; border-radius: 8px; padding: 10px; font-size:16px"
                )
                if cabin_price == 0:
                    pay_button.setToolTip("Price not available")
                else:
                    pay_button.setToolTip("Insufficient balance")
            else:
                pay_button.setStyleSheet(
                    "background-color: #007bff; color: white; border-radius: 8px; padding: 10px; font-size:16px"
                )
                pay_button.clicked.connect(
                    lambda _, ct=cabin_type, cp=cabin_price: self.on_pay_clicked(ct, cp, row_data)
                )
            info_layout.addWidget(pay_button, alignment=Qt.AlignRight)

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



    def load_ship_types(self):
        """Laden Sie die Schiffstypen in die Dropdownleiste."""
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
                break

        if not image_path:
            return
        # Bild laden und anzeigen
        pixmap = QPixmap(image_path).scaled(300, 250, Qt.KeepAspectRatio)
        self.ship_image_label.setPixmap(pixmap)

    def create_city_selection(self):
        """
        Erstellt den Abschnitt zur Auswahl von Städten mit Bildschaltflächen.
        Die Städte werden dynamisch anhand der gefilterten Ergebnisse generiert.
        """
        grid_layout = QGridLayout()
        row, col = 0, 0

        df_filtered = self.get_filtered_results()
        print(df_filtered)

        # Einzigartige Städte extrahieren
        unique_cities = df_filtered["Besuchte_Städte"].dropna().unique()
        cities = set(city.strip() for cities in unique_cities for city in cities.split(","))

        for city in sorted(cities):
            # Erstellen einer Bildschaltfläche
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setStyleSheet(city_section_style)

            btn.setIcon(QIcon(f"../images/Hafenstaedte/{city}.jpg"))  # Chemin des images

            btn.setIconSize(QSize(280, 200))  # Taille de l'image
            btn.setStyleSheet(city_section_style)

            btn.clicked.connect(lambda _, c=city, b=btn: self.toggle_city_selection(c, b))

            # Ein Label unter der Schaltfläche hinzufügen
            city_layout = QVBoxLayout()
            city_layout.addWidget(btn)
            city_label = QLabel(city)
            city_label.setAlignment(Qt.AlignCenter)
            city_layout.addWidget(city_label)

            # Container für jede Stadt
            city_widget = QWidget()
            city_widget.setLayout(city_layout)

            # Zum Raster hinzufügen
            grid_layout.addWidget(city_widget, row, col)
            col += 1
            if col > 3:  # 4 colonnes max
                col = 0
                row += 1

        # Container zuruckgeben
        scroll_widget = QWidget()
        scroll_widget.setLayout(grid_layout)
        return scroll_widget

    def on_filters_changed(self):
        """
        Methode, die aufgerufen wird, wenn sich die Filter (Meer, Nächte, Städte) ändern.
        Aktualisiert die Anzeige von Städten und Schiffstypen.
        """
        try:
            print("Geänderte Filter, aktualisierte Städte und Schiffe...")

            # Städte aktualisieren
            self.city_scroll_area.takeWidget()
            self.city_selection_widget = self.create_city_selection()
            self.city_scroll_area.setWidget(self.city_selection_widget)

            print("Aktualisierte Städte")
            filtered_results = self.get_filtered_results()
            self.display_result_table(filtered_results)

            # Schiffstypen aktualisieren
            self.update_ship_types()

        except Exception as e:
            print(f"Fehler beim Aktualisieren von Filtern : {e}")

    def toggle_city_selection(self, city_name, btn):
        """Eine Stadt zur Auswahl hinzufügen oder entfernen und das Erscheinungsbild aktualisieren."""
        if btn.isChecked():
            self.selected_cities.add(city_name)
        else:
            self.selected_cities.remove(city_name)
        self.update_ship_types()

        print(f"Ausgewählte Städte : {self.selected_cities}")

    def reset_form(self):
        """Alle Auswahlmöglichkeiten des Formulars zurücksetzen."""
        # Die Auswahl der Meere zurücksetzen
        self.sea_combo.setCurrentIndex(0)

        # Anzahl der Nächte zurücksetzen
        self.nights_spin.setSpecialValueText("undefine")
        self.nights_spin.setValue(0)

        # Die Auswahl der Städte zurücksetzen
        self.selected_cities.clear()
        for btn in self.findChildren(QPushButton):
            if btn.isCheckable():
                btn.setChecked(False)
                btn.setStyleSheet("border: 1px solid black; background-color: none;")

        # Auswahl der Schiffstypen zurücksetzen
        self.ship_combo.setCurrentIndex(0)
        self.ship_image_label.clear()

        self.result_list.clear()
        clear_layout(self.cabin_layout)
        self.cabin_summary_label.setText("")
        self.total_price_label = QLabel("Total Price: €0")


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
        min_nuits = max(1, selected_night - 2)  # Minimum von 1, um negative Werte zu vermeiden
        max_nuits = selected_night + 2

        # DataFrame nach Bereich filtern
        dataframe_filtre = dataframe[
            (dataframe["Übernachtungen"] >= min_nuits) &
            (dataframe["Übernachtungen"] <= max_nuits)
            ]
        print(dataframe_filtre)
        return dataframe_filtre

    def update_ship_types(self):
        """Aktualisiert die Bootstypen in der Combo entsprechend den Filtern."""
        filtered_results = self.get_filtered_results()
        available_ships = filtered_results["Schiffstyp"].dropna().unique()

        self.ship_combo.clear()
        self.ship_combo.addItem("Choose a Ship")

        if not available_ships.size:  # Prüft, ob die Liste leer ist
            self.ship_combo.addItem("No ship available")
        else:
            for ship_type in available_ships:
                self.ship_combo.addItem(ship_type)

    def on_user_logo_clicked(self):

        try:
            self.update_user_profil_page()  # Aktualisiert die Benutzerseite
            self.stacked_widget.setCurrentWidget(self.user_profil)  # Zeigt die Benutzerseite an
        except Exception :
            return None

    def update_user_profil_page(self):
        """
        Aktualisiert die Benutzerinformationen auf der Seite user_profil
        """
        user_data = get_user_info(self.header_user_name_edit)
        if user_data:
            self.user_profil.update_user_info(user_data)
        else:
            return None


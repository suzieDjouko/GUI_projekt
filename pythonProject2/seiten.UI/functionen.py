import os
import pandas as pd
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox, QGridLayout, QPushButton, QVBoxLayout, QLabel, QWidget


def load_data(file_path, parent_widget):
    """Daten aus der Excel-Datei laden."""
    try:
        df = pd.read_excel(file_path)

        # Überprüfen Sie, ob die notwendigen Spalten vorhanden sind
        expected_columns = [
            "Meerart", "Übernachtungen", "Besuchte_Städte", "Schiffstyp",
            "Innenkabine", "Aussenkabine", "Balkonkabine",
            "Luxuskabine1", "Luxuskabine2", "Luxuskabine3"
        ]
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            parent_widget.show_error(f"Fehlende Spalten : {', '.join(missing_columns)}")
            return None

        # Bereinigung der Daten
        df = df.dropna(how='all')
        for col in ["Innenkabine", "Aussenkabine", "Balkonkabine", "Luxuskabine1", "Luxuskabine2", "Luxuskabine3"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].replace("nicht vorhanden", 0), errors='coerce').fillna(0).astype(int)
        return df
    except FileNotFoundError:
        parent_widget.show_error(f"Datei nicht gefunden : {file_path}")
    except Exception as e:
        parent_widget.show_error(f"Daten können nicht geladen werden : {e}")
    return None

def filter_by_sea(selected_sea, dataframe):
    return dataframe if selected_sea == "All" else dataframe[dataframe["Meerart"] == selected_sea]

def filter_by_night( selected_night, dataframe):
        min_nuits = max(1, selected_night - 2)  # Minimum von 1, um negative Werte zu vermeiden
        max_nuits = selected_night + 2
        return dataframe[
            (dataframe["Übernachtungen"] >= min_nuits) &
            (dataframe["Übernachtungen"] <= max_nuits)
            ]
def filter_by_ship(selected_ship, dataframe):
    return dataframe if not selected_ship or selected_ship == "Choose a Ship" else dataframe[
        dataframe["Schiffstyp"].str.contains(selected_ship, na=False, case=False)
    ]

def get_filtered_results(selected_sea, selected_night, selected_ship, selected_cities, dataframe):
    """Alle Filter auf den Datenrahmen anwenden."""
    filtered_df = filter_by_sea(selected_sea, dataframe)
    filtered_df = filter_by_night(selected_night, filtered_df)
    filtered_df = filter_by_ship(selected_ship, filtered_df)

    if selected_cities:
        def match_cities(cities):
            if not isinstance(cities, str):
                return False
            return any(city.strip() in selected_cities for city in cities.split(","))
        filtered_df = filtered_df[filtered_df["Besuchte_Städte"].apply(match_cities)]
    return filtered_df

def get_cabin_image_path(cabin_type):
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


def update_payment_page(cabin_type, cabin_price, cabin_details_label, total_price_label):
    """
    Aktualisieren Sie die Details der Zahlungsseite mit der ausgewählten Kabine und dem Preis.
    """
    cabin_details_label.setText(
        f"<b>Selected Cabin:</b> {cabin_type}<br>"
        f"<b>Price:</b> {cabin_price} €"
    )
    total_price_label.setText(f"Total Price: {cabin_price} €")


def load_ship_types(folder_path, ship_combo):
    """Schiffstypen in das Kombinationsfeld laden."""
    if not os.path.exists(folder_path):
        ship_combo.addItem("No ship available")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            ship_name = filename.split(" ")[-1].split(".")[0]  # Example: "A" from "Schiffstyp A.jpg"
            ship_combo.addItem(ship_name)


def display_selected_ship_image(ship_name, folder_path, ship_image_label):
    """Anzeige des Bildes des ausgewählten Schiffes."""
    extensions = [".jpeg", ".JPG"]
    image_path = None

    for ext in extensions:
        path = os.path.join(folder_path, f"Schiffstyp {ship_name}{ext}")
        if os.path.exists(path):
            image_path = path
            break

    if not image_path:
        return

    pixmap = QPixmap(image_path).scaled(300, 250, aspectRatioMode=1)  # Qt.KeepAspectRatio = 1
    ship_image_label.setPixmap(pixmap)


def create_city_selection(filtered_df, city_section_style, toggle_city_selection_callback):
    """
    Erstellen Sie den Stadtauswahlbereich dynamisch auf der Grundlage der gefilterten Ergebnisse.
    """
    grid_layout = QGridLayout()
    row, col = 0, 0

    # Extract unique cities
    unique_cities = filtered_df["Besuchte_Städte"].dropna().unique()
    cities = set(city.strip() for cities in unique_cities for city in cities.split(","))

    for city in sorted(cities):
        # Create image button
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setStyleSheet(city_section_style)
        btn.setIcon(QIcon(f"../images/Hafenstaedte/{city}.jpg"))
        btn.setIconSize(QSize(300, 250))

        # Add click event
        btn.clicked.connect(lambda _, c=city, b=btn: toggle_city_selection_callback(c, b))

        # Add a label under the button
        city_layout = QVBoxLayout()
        city_layout.addWidget(btn)
        city_label = QLabel(city)
        city_label.setAlignment(Qt.AlignCenter)
        city_layout.addWidget(city_label)

        # Add to grid
        city_widget = QWidget()
        city_widget.setLayout(city_layout)
        grid_layout.addWidget(city_widget, row, col)

        col += 1
        if col > 3:  # 4 columns max
            col = 0
            row += 1

    # Return the layout as a QWidget
    scroll_widget = QWidget()
    scroll_widget.setLayout(grid_layout)
    return scroll_widget


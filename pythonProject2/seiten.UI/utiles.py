
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import os
from city_selection import toggle_city_selection


def display_cities_in_grid(city_image_mapping, layout, max_columns=4):
    """
    Affiche les villes et leurs images dans une grille.

    Args:
        city_image_mapping (dict): Dictionnaire contenant les villes comme clés et leurs chemins d'image comme valeurs.
        layout (QGridLayout): Layout de destination pour afficher les villes.
        max_columns (int): Nombre maximum de colonnes dans la grille.
    """
    row, col = 0, 0
    button_size = QSize(380, 290)
    #image_size = QSize(350,230)# Taille fixe pour les boutons

    for city_name, image_path in city_image_mapping.items():
        if not os.path.exists(image_path):
            image_path = "../images/Hafenstaedte/default.jpg"  # Image par défaut

        pixmap = QPixmap(image_path).scaled(button_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        city_button = QPushButton()
        city_button.setCheckable(True)
        icon = QIcon(pixmap)
        city_button.setIcon(icon)
        city_button.setIconSize(button_size)  # Fixer la taille de l'icône
        city_button.setFixedSize(button_size)  # Fixer la taille du bouton indépendamment de l'image
        #city_button.setIconSize(pixmap.size())  # Redimensionner l'icône pour qu'elle corresponde à l'image
        #city_button.setFixedSize(button_size)  # Fixer la taille du bouton indépendamment de l'image

        city_button.clicked.connect(lambda checked,  btn=city_button , city= city_name: toggle_city_selection(city, btn))



        city_button.setStyleSheet("border: 0px solid black; margin: 0px; padding: 0px;")

        city_name_label = QLabel(city_name)
        city_name_label.setAlignment(Qt.AlignCenter)
        city_name_label.setStyleSheet("font-weight: bold; margin-top: 5px;")

        # Ajouter les éléments dans un layout vertical
        city_layout = QVBoxLayout()
        city_layout.addWidget(city_button)
        city_layout.addWidget(city_name_label)


        layout.addLayout(city_layout, row, col)
        col += 1
        if col >= max_columns:
            col = 0
            row += 1






def clear_layout(layout):
    """Supprime tous les widgets d'un layout."""
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()  # Supprime le widget
        elif item.layout():
            clear_layout(item.layout())  # Nettoie les layouts imbriqués


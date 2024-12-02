"""
def update_city_selection(self):
    try:
        selected_sea = self.sea_combo.currentText()
        selected_night = self.nights_spin.value()

        print(f"Selected Sea: {selected_sea}, Selected Nights: {selected_night}")

        # Mettre à jour la liste des villes selon les critères
        unique_cities = filter_cities_by_criteria(selected_night, selected_sea)
        unique_cities = list(set(unique_cities))
        print(f"Unique cities: {unique_cities}")

        # Récupérer les images correspondantes aux villes filtrées
        images_paths = getImagesForFilteredCities(selected_night, selected_sea, self.dataFrame,
                                                  self.hafenstaedte_folder)
        images_paths = list(set(images_paths))
        print(f"Image paths: {images_paths}")
        city_image_mapping = {}

        for city in unique_cities:
            for image_path in images_paths:
                # Vérifiez si le nom de la ville est dans le nom du fichier image
                if city.lower() in image_path.lower():
                    city_image_mapping[city] = image_path
                    break  # Associez l'image à la ville et passez à la ville suivante

        # Afficher la correspondance des villes et images
        print("City and Image Mapping:")
        for city, image_path in city_image_mapping.items():
            print(f"{city}: {image_path}")

        clear_layout(self.city_selection_layout)

        max_columns = 4
        row = 0
        col = 0

        for city_name in unique_cities:
            # Vérifier si l'image pour la ville est dans le mapping
            if city_name in city_image_mapping:
                image_path = city_image_mapping[city_name]
            else:
                image_path = "../images/Hafenstaedte\\default.jpg"  # Image par défaut si la ville n'a pas d'image

            if not os.path.exists(image_path):  # Vérifiez si le fichier existe
                print(f"Image file does not exist: {image_path}")
                image_path = "../images/Hafenstaedte\\default.jpg"  # Utilisez une image par défaut si le fichier n'existe pas

            city_image_label = QLabel()
            pixmap = QPixmap(image_path)
            city_image_label.setPixmap(pixmap)
            city_image_label.setAlignment(Qt.AlignCenter)
            city_image_label.setFixedSize(350, 230)
            city_image_label.setStyleSheet("border: 1px solid black; margin: 10px;")
            # Placer l'image dans la grille à la position (row, col)

            city_name_label = QLabel(city_name)
            city_name_label.setAlignment(Qt.AlignCenter)
            city_name_label.setStyleSheet("font-weight: bold; margin-top: 5px;")

            city_layout = QVBoxLayout()
            city_layout.addWidget(city_image_label)
            city_layout.addWidget(city_name_label)

            # self.city_selection_layout.addWidget(city_image_label, row, col)
            self.city_selection_layout.addLayout(city_layout, row, col)

            col += 1
            if col >= max_columns:  # Si la colonne atteint le maximum, on passe à la ligne suivante
                col = 0
                row += 1

        self.city_selection_scroll.setWidget(self.city_selection_widget)
        self.city_selection_scroll.setWidgetResizable(True)

    except Exception as e:
        print(f"Error in update_city_selection: {e}")


   def populate_cities(self, hafenstaedte_folder):

        if not os.path.exists(hafenstaedte_folder):
            print(f"Le dossier {hafenstaedte_folder} n'existe pas.")
            return

        city_files = [f for f in os.listdir(hafenstaedte_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if not city_files:
            print(f"Aucune image trouvée dans {hafenstaedte_folder}.")
            return

        max_columns = 4  # Nombre d'images par ligne
        row, col = 0, 0

        for city_file in city_files:
            image_path = os.path.join(hafenstaedte_folder, city_file)

            # Créer un QLabel pour l'image
            city_image_label = QLabel()
            pixmap = QPixmap(image_path).scaled(
                350, 230, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            city_image_label.setPixmap(pixmap)
            city_image_label.setAlignment(Qt.AlignCenter)
            city_image_label.setFixedSize(350,230)
            city_image_label.setStyleSheet("border: 1px solid black; margin: 10px;")

            # Créer un QLabel pour le nom de la ville
            city_name = os.path.splitext(city_file)[0]  # Nom du fichier sans extension
            city_name_label = QLabel(city_name)
            city_name_label.setAlignment(Qt.AlignCenter)
            city_name_label.setStyleSheet("font-weight: bold; margin-top: 5px;")

            # Ajouter l'image et le label dans un layout vertical
            city_layout = QVBoxLayout()
            city_layout.addWidget(city_image_label)
            city_layout.addWidget(city_name_label)

            # Ajouter ce layout dans la grille
            self.city_selection_layout.addLayout(city_layout, row, col)

            # Gérer les colonnes et les lignes
            col += 1
            if col >= max_columns:
                col = 0
                row += 1




 def update_city_selection(self):
    try:
        selected_sea = self.sea_combo.currentText()
        selected_night = self.nights_spin.value()

        print(f"Selected Sea: {selected_sea}, Selected Nights: {selected_night}")

        # Mettre à jour la liste des villes selon les critères
        unique_cities = filter_cities_by_criteria(selected_night, selected_sea)
        print(f"Unique cities: {unique_cities}")

        # Récupérer les images correspondantes aux villes filtrées
        images_paths = getImagesForFilteredCities(selected_night, selected_sea, self.dataFrame,
                                                  self.hafenstaedte_folder)
        print(f"Image paths: {images_paths}")

        # Vider la disposition existante
        for i in reversed(range(self.city_selection_layout.count())):
            widget = self.city_selection_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        max_columns = 4  # Nombre d'images par ligne (colonnes)

        row = 0
        col = 0

        # Ajouter les nouvelles images à la vue
        for image_path in images_paths:
            if not os.path.exists(image_path):  # Vérifiez si le fichier existe
                print(f"Image file does not exist: {image_path}")
                image_path = "default.jpg"  # Utilisez une image par défaut si le fichier n'existe pas

            city_image_label = QLabel()
            pixmap = QPixmap(image_path)
            city_image_label.setPixmap(pixmap)
            city_image_label.setAlignment(Qt.AlignCenter)
            city_image_label.setFixedSize(300, 230)
            city_image_label.setStyleSheet("border: 1px solid black; margin: 10px;")
            # Placer l'image dans la grille à la position (row, col)
            self.city_selection_layout.addWidget(city_image_label, row, col)

            col += 1
            if col >= max_columns:  # Si la colonne atteint le maximum, on passe à la ligne suivante
                col = 0
                row += 1

        self.city_selection_scroll.setWidget(self.city_selection_widget)
        self.city_selection_scroll.setWidgetResizable(True)
    except Exception as e:
        print(f"Error in update_city_selection: {e}")

    ""

        def display_city_images(self,city_list, folder_path, layout):
        city_images = getImageByCityName(city_list, folder_path)  # Remplace cette ligne si nécessaire

        for city_name, image_path in zip(city_list,city_images):
            # Créer un QLabel pour afficher l'image
            city_image_label = QLabel()
            city_image_label.setFixedSize(350, 230)
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(350,230,Qt.KeepAspectRatio , Qt.SmoothTransformation) # Adapter la taille de l'image
            city_image_label.setPixmap(pixmap)

            # Ajouter une description de la ville sous l'image
            city_name_label = QLabel(city_name)

            # Créer un layout vertical pour chaque ville (image + nom)
            city_layout = QVBoxLayout()
            city_layout.addWidget(city_image_label)
            city_layout.addWidget(city_name_label)

            # Ajouter le layout de la ville au layout principal
            layout.addLayout(city_layout)


    """


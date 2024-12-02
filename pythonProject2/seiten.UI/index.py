import os

import pandas as pd
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from city_selection import get_selected_cities

hafenstaedte_folder = "../images/Hafenstaedte"

schiffstyp_folder = "../images/Schiffstypen"  # Types de navires
cabintype_folder = "../images/Kabinentypen"  # Types de cabines
base_dir = os.path.dirname(os.path.abspath(__file__))
# Répertoire actuel
hafenstaedte_folder2 = os.path.join(base_dir, "images", "Hafenstaedte")
schiffstyp_folder2 = os.path.join(base_dir, "images", "Schiffstypen")
cabintype_folder2 = os.path.join(base_dir, "images", "Kabinentypen")

#loadImage charge les noms  de fichiers images depuis un dossier specifique
#et retourne une liste de noms  des fichiers sans leurs extensions
file_path = "../Schiffsreisen.xlsx"  # Chemin vers le fichier Excel



def loadImages(folder_path):
    if not os.path.exists(folder_path):
        return []
    return [
        #filename.split(".")[0].replace(" ", "")

        filename.replace(" ", "_").strip()
        for filename in os.listdir(folder_path)
        #filename for filename in os.listdir(folder_path)
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".JPG"))
    ]

def find_city_image(city_names , folder_path):
    city_image_name = city_names.lower().replace(" ", "_")  # Normalisation du nom de la ville
    available_images = os.listdir(folder_path)  # Liste des fichiers dans le dossier
    for image in available_images:
        # Extraire le nom du fichier sans extension pour comparer
        image_name_no_ext = os.path.splitext(image)[0].lower().replace(" ", "_")
        if city_image_name == image_name_no_ext:
            return os.path.join(folder_path, image)  # Retourner le chemin complet de l'image
    return None



def match_city_images(city_list, folder_path):
    #retourne un Dictionnaire avec les villes en clé et le chemin de l'image trouvée ou None.
    results = {}
    for city in city_list:
        image_path = find_city_image(city, folder_path)  # Trouver l'image pour chaque ville
        results[city] = image_path
        if image_path:
            print(f"Image trouvée pour {city}: {image_path}")
        else:
            print(f"Aucune image trouvée pour {city}.")
    return results




def getImageByCityName(city_names, folder_path):
    available_images = loadImages(folder_path)
    #city_names = loadImgagesnamawithowExtension(folder_path)
    images_paths = [] #pour stocker les chemeins des images
    #print('available_images')
    #print(available_images)
    for city_name in available_images:
        # Remplace les espaces par des underscores pour correspondre aux fichiers
        city_image_name = city_name.replace(" ", "_")  # Nom de ville transformé
        #print("city_image_name")
        #print(city_image_name)

        # Vérifie les différentes extensions (.jpg, .JPG, etc.)
        found_image = None
        for image in available_images:
            #print(f"Comparing {city_image_name.lower()} with {image.lower().replace(' ', '_')}")
            if city_image_name.lower() == image.lower().replace(" ", "_"):
                found_image = os.path.join(folder_path, image)
                print(found_image)
                #print(f"Match found: {city_image_name} -> {image}")

                break
        # Si l'image est trouvée, on l'ajoute à la liste, sinon on ajoute l'image par défaut
        if found_image and os.path.exists(found_image):
            images_paths.append(found_image)
        else:
            images_paths.append(os.path.join(folder_path, "default.jpg"))

    return images_paths

result = loadImages(hafenstaedte_folder)
print(result)
images_paths = getImageByCityName(result, hafenstaedte_folder)
print(images_paths)


def load_data(file_path):
    try:
        dataFrame = pd.read_excel(file_path, header=3)
        print("Data loaded")
        return dataFrame

    except Exception as e:
        print(f"Error reading : {e}")
        return None

def load_data2(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"File does not exist at path: {file_path}")
            return None
        dataFrame = pd.read_excel(file_path, header=3)
        print("Data loaded successfully.")
        return dataFrame
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error loading file: {e}")
    return None


def clean_data(dataFrame):
    if dataFrame is not None:
        dataFrame = dataFrame.dropna(how='all', axis=1) #supprimes les colonnes entierement vides

        dataFrame = dataFrame.dropna(how='all', axis=0)   #supprimes les lignes entierement vides
        return dataFrame
    else:
        print("No data")
        return None


def loadData_and_clean_data(file_path): #charge et netoi les donne depuis le fichier Excel
    data = load_data2(file_path)
    data = clean_data(data)


    if data is not None:
        try:
            # Convertir les types de colonnes
            data["Reisenummer"] = data["Reisenummer"].astype(int)
            data["Meerart"] = data["Meerart"].astype(str)
            data["besuchte Städte"] = data["besuchte Städte"].astype(str)
            data["Übernachtungen"] = data["Übernachtungen"].astype(int)

            print("Data cleaned and ready to use.")
            return data
        except KeyError as e:
            print(f"Missing expected column: {e}")
            return None
        except Exception as e:
            print(f"Error during cleaning: {e}")
            return None
    else:
        print("No data to clean.")
        return None

# Remplacez par le chemin correct

dataFrame = loadData_and_clean_data(file_path)
if dataFrame is not None:
    print(dataFrame.head())  # Afficher un aperçu des données nettoyées
else:
    print("Aucune donnée valide chargée.")

def getSea(dataFrame):
    if 'Meerart' in dataFrame.columns:
        sea_data = dataFrame['Meerart'].unique()  # Récupère les valeurs uniques de la colonne 'Meerart  depuis le fichier Excel'
        print(f"Available seas: {sea_data}")
        return sea_data
    else:
        print("Column 'Meerart' not found in DataFrame")
        return []

seas = getSea(dataFrame)


def filterBySea(dataFrame , selected_sea):
    filtered_data = dataFrame[dataFrame['Meerart'] == selected_sea]
    return filtered_data


selected_sea = 'Nordsee'  # Exemple : l'utilisateur a sélectionné 'Nordsee'
filtered_results = filterBySea(dataFrame, selected_sea)
print(filtered_results)

def filterBySeaAndByNight(dataFrame, selected_sea , uebernachtung):
    sea_filtered = dataFrame[dataFrame['Meerart'] == selected_sea]
    interval = [uebernachtung - 2, uebernachtung - 1, uebernachtung, uebernachtung + 1, uebernachtung + 2]
    final_filtered_data = sea_filtered[sea_filtered['Übernachtungen'].isin(interval)]
    return final_filtered_data

selected_sea1 = 'Nordsee'  # Exemple : l'utilisateur a sélectionné 'Nordsee'
uebernachtung1 = 5
result4 = filterBySeaAndByNight(dataFrame, selected_sea1, uebernachtung1)
print(result4)

def filter_cities_by_criteria(selected_night , selected_sea, selected_city):
    filtered_data = dataFrame  # Valeur par défaut si aucun critère n'est appliqué

    if selected_city :
        filtered_data = get_selected_cities()
    if selected_sea =='All Sea'and selected_night == '2':
        print('Fetching all images since selected sea is All sea and nights = 2.')
        filtered_data = dataFrame
    if selected_sea and selected_night:  # Si la mer et les nuits sont sélectionnées
        filtered_data = filterBySeaAndByNight(dataFrame, selected_sea, selected_night)
    elif selected_sea:  # Si seule la mer est sélectionnée
        filtered_data = filterBySea(dataFrame, selected_sea)
    elif selected_night:  # Si seulement les nuits sont sélectionnées
        filtered_data = getVacanciesByNigthRange(dataFrame,selected_night)
    #else:  # Si aucun filtre n'est appliqué
        #filtered_data = dataFrame  # Aucune condition, on retourne toutes les données

    city_column = filtered_data['besuchte Städte'].dropna().str.strip()
    all_cities = city_column.str.split(',').sum()
    all_cities = [city.strip() for city in all_cities if city.strip()]
    return all_cities

def update_table(table_widget , filtered_data):
    table_widget.setRowCount(0)
    table_widget.setRowCount(len(filtered_data))  # Définit le nombre de lignes
    #table_widget.setColumnCount(len(filtered_data.columns))
    table_widget.setHorizontalHeaderLabels(filtered_data.columns)

    for i, row in filtered_data.iterrows():
        table_widget.insertRow(i)
        for j, value in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(value)))

    print(f"Table mise à jour avec {len(filtered_data)} lignes.")

def reset_table(table):
    update_table(table, dataFrame)


selected_sea = 'Nordsee'  # La mer sélectionnée
selected_nights = 14 # Le nombre de nuits sélectionné
selected_cities = {'Edinburgh', 'Aberdeen', 'Torshavn', 'Reykjavik'}
unique_cities = filter_cities_by_criteria(selected_nights, selected_sea,selected_cities)
print("unique_cities")
print(unique_cities)
imgage_sources = getImageByCityName(unique_cities , hafenstaedte_folder)
print('imgage_sources')
print(imgage_sources)


# Maintenant, unique_cities contient les villes disponibles pour la mer 'Nordsee' et 5 nuits
print(unique_cities)


#filterbynight
def getVacanciesByNigthRange(dataFrame ,uebernachtung):
    #interval = [uebernachtung - 2, uebernachtung - 1, uebernachtung, uebernachtung + 1, uebernachtung + 2]
    #interval = [n for n in interval if n >= 1]


    if 'Übernachtungen' not in dataFrame.columns:
        raise ValueError("La colonne 'Übernachtungen' est manquante dans le DataFrame.")

    #unique_nights = dataFrame['Übernachtungen'].unique()
    interval = range(max(1, uebernachtung - 2), uebernachtung + 3)  # Inclut (n-2, n-1, n, n+1, n+2)


    filtered_data = dataFrame[dataFrame['Übernachtungen'].isin(interval)]
    return filtered_data

result3 = getVacanciesByNigthRange(dataFrame,5)
print(result3)


def findVacaniesByNigth(self, nigth):
    print("Get vacancies by nigth value")

def show_warning_message(title, message):
    warning_box = QMessageBox()
    warning_box.setWindowTitle(title)
    warning_box.setText(message)
    warning_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #ffe6e6;
                        border: 1px solid #ff4d4d;
                    }
                    QLabel {
                        font-size: 14px;
                        color: #cc0000;
                        font-weight: bold;
                    }
                    QPushButton {
                        background-color: #ff4d4d;
                        color: white;
                        padding: 8px;
                        border-radius: 5px;
                        width: 50px;
                    }
                    QPushButton:hover {
                        background-color: #cc0000;
                    }
                """)
    warning_box.exec_()


def load_ship_types(file_path):
    """Charge les types de navires à partir du répertoire donné et retourne une liste des noms des navires."""
    ship_types = []

    if not os.path.exists(file_path):
        print(f"Le répertoire {file_path} n'existe pas.")
        return ship_types

    for filename in os.listdir(file_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            ship_name = filename.split(".")[0]  # Nom sans extension
            ship_types.append(ship_name)

    return ship_types


def display_selected_ship_image(ship_name, imge_label):
        """Afficher l'image du navire sélectionné."""
        if ship_name == "Sélectionnez un type de navire" or ship_name == "Aucun navire disponible":
           # QMessageBox.warning("Attention", "Aucun type de navire sélectionné.")
            return
        image_path = os.path.join(schiffstyp_folder, f"{ship_name}.jpg")
        if not os.path.exists(image_path):  # Si .jpg n'existe pas, chercher d'autres extensions
            for ext in [".png", ".jpeg"]:
                image_path = os.path.join(schiffstyp_folder, f"{ship_name}{ext}")
                if os.path.exists(image_path):
                    break
            else:
                image_path = os.path.join(schiffstyp_folder, "default.jpg")

        if not os.path.exists(image_path):
            image_path = os.path.join(schiffstyp_folder, "default.jpg")

                    #QMessageBox.warning(self, "Erreur", f"Aucune image trouvée pour le navire : {ship_name}.")
                #return
        pixmap = QPixmap(image_path).scaled(300, 200, Qt.KeepAspectRatio)
        imge_label.setPixmap(pixmap)


def getImagesForFilteredCities(selected_night,selected_sea, dataFrame,folder_path):


    unique_cities = filter_cities_by_criteria(selected_night, selected_sea,get_selected_cities())
    image_paths = []
    for city in unique_cities:
        city_image_path = find_city_image(city, folder_path)
        if city_image_path:
            image_paths.append(city_image_path)
        else:
            # Ajouter une image par défaut si aucune image spécifique n'est trouvée
            image_paths.append(os.path.join(folder_path, "default.jpg"))

    return image_paths


selected_sea = 'Ostsee'  # Exemple : Mer sélectionnée
selected_nights = 14  # Exemple : Nombre de nuits sélectionné

# Obtenir les chemins d'images pour les villes filtrées
filtered_image_paths = getImagesForFilteredCities(selected_nights, selected_sea, dataFrame, hafenstaedte_folder)

# Afficher les chemins des images trouvées
print("Chemins des images filtrées :")
for path in filtered_image_paths:
    print(path)

def getVacancyBySelectedCity(selected_cities):
   # selected_cities = get_selected_cities()
    if selected_cities:
        filtered_dataframe = dataFrame[dataFrame['besuchte Städte'].isin(selected_cities)]
        return filtered_dataframe
    else:
        return dataFrame


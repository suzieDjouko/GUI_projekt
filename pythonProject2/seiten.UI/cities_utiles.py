import os
from utiles import display_cities_in_grid , clear_layout
from index import filter_cities_by_criteria ,getImagesForFilteredCities
from  city_selection import toggle_city_selection , get_selected_cities

def populate_cities(hafenstaedte_folder, layout):
    """
    Charge et affiche les images des villes depuis un dossier donné.

    Args:
        hafenstaedte_folder (str): Chemin du dossier contenant les images des villes.
        layout (QGridLayout): Layout de destination pour afficher les villes.
    """
    if not os.path.exists(hafenstaedte_folder):
        print(f"Le dossier {hafenstaedte_folder} n'existe pas.")
        return

    city_files = [f for f in os.listdir(hafenstaedte_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    city_image_mapping = {
        os.path.splitext(f)[0]: os.path.join(hafenstaedte_folder, f)
        for f in city_files
    }
    display_cities_in_grid(city_image_mapping, layout)

def update_city_selection(dataframe, hafenstaedte_folder, sea, nights, layout):
    """
    Met à jour la sélection des villes en fonction des critères.

    Args:
        dataframe (DataFrame): Données des voyages.
        hafenstaedte_folder (str): Dossier contenant les images des villes.
        sea (str): Mer sélectionnée.
        nights (int): Nombre de nuits sélectionné.
        layout (QGridLayout): Layout de destination pour afficher les villes.
    """
    try:
        selected_cities = get_selected_cities()
        unique_cities = filter_cities_by_criteria(nights, sea,selected_cities)
        unique_cities = list(set(unique_cities))
        print(f"Filtered cities: {unique_cities}")

        images_paths = getImagesForFilteredCities(nights, sea, dataframe, hafenstaedte_folder)
        images_paths = list(set(images_paths))

        city_image_mapping = {}
        for city in unique_cities:
            for image_path in images_paths:
                if city.lower() in image_path.lower():
                    city_image_mapping[city] = image_path
                    break
        clear_layout(layout)
        display_cities_in_grid(city_image_mapping, layout)
    except Exception as e:
        print(f"Error in update_city_selection: {e}")


selected_cities = set()

def toggle_city_selection(city_name, btn):
    global selected_cities
    """Ajouter ou retirer une ville de la sélection et mettre à jour l'apparence."""
    if btn.isChecked():
        selected_cities.add(city_name)
        btn.setStyleSheet("border: 2px solid blue; background-color: lightblue;")
        print(f"{city_name} sélectionnée")
        print(selected_cities)
    else:
        selected_cities.remove(city_name)
        btn.setStyleSheet("border: 1px solid black; background-color: none;")
        print(f"{city_name} retirée")
        print(selected_cities)
    return list(selected_cities)

def get_selected_cities():
    return list(selected_cities)




import os
import pandas as pd


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






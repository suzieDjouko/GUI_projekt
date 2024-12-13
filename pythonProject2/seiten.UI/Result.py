import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView, QMessageBox, QPushButton, QApplication
from PyQt5.QtCore import QStringListModel
from fonctionalitee import Reise  # Assurez-vous que VoyageApp est bien défini dans ce fichier


class TravelSelectionWidget(QWidget):
    def __init__(self, user_balance, trips_data):
        """
        Constructeur de la classe TravelSelectionWidget.
        :param user_balance: Le solde du compte utilisateur.
        :param trips_data: Les données des voyages filtrés sous forme de DataFrame.
        """
        super().__init__()

        # Initialisation des attributs avec les données passées par le constructeur
        self.user_balance = user_balance
        self.trips_data = trips_data  # trips_data doit être un DataFrame filtré avec get_filtered_results()

        self.initUI()

    def initUI(self):
        """
        Initialisation de l'interface utilisateur avec la liste des voyages.
        """
        layout = QVBoxLayout()

        # Initialisation de la vue et du modèle de la liste
        self.list_view = QListView(self)
        self.model = QStringListModel(self)
        self.updateTripList()

        # Connexion du bouton de confirmation à la méthode de sélection
        self.confirm_button = QPushButton("Select Trip", self)
        self.confirm_button.clicked.connect(self.select_trip)

        # Ajout des éléments au layout
        layout.addWidget(self.list_view)
        layout.addWidget(self.confirm_button)

        # Application du layout à la fenêtre principale
        self.setLayout(layout)

    def updateTripList(self):
        """
        Mise à jour de la liste des voyages à afficher, en fonction du solde utilisateur.
        """
        try:
            # Convertir le solde de l'utilisateur en un nombre flottant à partir du texte du QLineEdit
            user_balance = float(self.user_balance.text())  # Convertir le texte du QLineEdit en un nombre flottant
        except ValueError:
            # Si la conversion échoue, afficher un message d'erreur et arrêter la méthode
            #QMessageBox.warning(self, "Erreur", "Le solde de l'utilisateur est invalide.")
            return

        trip_strings = []
        for _, trip in self.trips_data.iterrows():  # Nous itérons sur les lignes du DataFrame
            trip_str = f"Voyage {trip['Reisenummer']} - {trip['Meerart']} - {trip['Übernachtungen']} nuits"

            # Vérification des cabines abordables en fonction du solde utilisateur
            affordable = False
            cabin_names = ['Innenkabine', 'Aussenkabine', 'Balkonkabine', 'Luxuskabine Kategorie1',
                           'Luxuskabine Kategorie2', 'Luxuskabine Kategorie3']

            for cabin_name in cabin_names:
                try:
                    cabin_price = float(trip[cabin_name])  # Convertir le prix de la cabine en un nombre flottant
                    if cabin_price <= user_balance:
                        affordable = True
                        break  # Si une cabine est abordable, on arrête la vérification pour ce voyage
                except ValueError:
                    # Si le prix de la cabine est invalide (non numérique), ignorer cette cabine
                    continue
            if affordable:
                trip_strings.append(trip_str)
            else:
                trip_strings.append(trip_str + " (Indisponible - Solde insuffisant)")

        # Mise à jour du modèle avec les voyages filtrés
        self.model.setStringList(trip_strings)

    def select_trip(self):
        """
        Traitement de la sélection d'un voyage par l'utilisateur.
        """
        selected_index = self.list_view.currentIndex()

        if selected_index.isValid():
            # Récupération du voyage sélectionné (ligne du DataFrame)
            selected_trip = self.trips_data.iloc[selected_index.row()]

            # Recherche des cabines abordables pour ce voyage
            affordable_cabins = []
            cabin_names = ['Innenkabine', 'Aussenkabine', 'Balkonkabine', 'Luxuskabine Kategorie1',
                           'Luxuskabine Kategorie2', 'Luxuskabine Kategorie3']

            for cabin_name in cabin_names:
                cabin_price = selected_trip[cabin_name]  # Prix de la cabine
                if cabin_price <= self.user_balance:
                    affordable_cabins.append(cabin_name)  # Ajout du nom de la cabine si elle est abordable

            if affordable_cabins:
                # Affichage du voyage sélectionné et des cabines disponibles
                print(f"Voyage sélectionné: {selected_trip['Reisenummer']}")
                print(f"Cabines disponibles: {affordable_cabins}")
            else:
                # Message d'erreur si aucune cabine n'est abordable
                return

if __name__ == "__main__":
    # Démarrage de l'application PyQt
    app = QApplication(sys.argv)

    # Exemple d'utilisation avec un solde d'utilisateur et des données de voyage
    voyage_app = Reise()
    user_balance = voyage_app.kontostand_amont_edit  # Solde utilisateur
    trips_data = voyage_app.get_filtered_results()  # Données des voyages filtrées

    window = TravelSelectionWidget(user_balance, trips_data)
    window.show()

    sys.exit(app.exec_())

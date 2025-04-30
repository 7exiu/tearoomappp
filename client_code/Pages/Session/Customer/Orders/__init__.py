from ._anvil_designer import OrdersTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Orders(OrdersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
# Dans ta Formulaire où se trouve le bouton "Télécharger reçu"

# ... (ton code existant) ...

    def telecharger_recu_button_click(self, **event_args):
        """Gère le clic du bouton pour télécharger le reçu."""

        commande_id = self.item['id'] # Supposons que chaque commande a un ID

        commande_details = anvil.server.call('get_commande_details', commande_id)

        # 3. Vérifier si les détails de la commande ont été récupérés
        if commande_details:
            # 4. Préparer les données de la commande pour la génération du reçu
            commande_data = {
                'id': commande_details['id'],
                'nom_client': commande_details['nom_client'],
                'prenom_client': commande_details['prenom_client'],
                'email_client': commande_details['email_client'],
                'produits': commande_details['produits'], # Assure-toi que ça contient nom et prix
                'total': commande_details['total']
                # Ajoute ici toutes les autres informations nécessaires pour ton reçu
            }

            # 5. Appeler la fonction serveur pour générer le reçu
            recu_pdf = anvil.server.call('generer_recu', commande_data)

            # 6. Proposer le téléchargement du PDF
            if recu_pdf:
                anvil.downloader.download(recu_pdf)
            else:
                alert("Une erreur est survenue lors de la génération du reçu.")
        else:
            alert("Impossible de récupérer les détails de cette commande.")

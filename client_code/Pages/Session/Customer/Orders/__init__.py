from ._anvil_designer import OrdersTemplate
from anvil import *
import anvil.server



class Orders(OrdersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
# Dans ta Formulaire où se trouve le bouton "Télécharger reçu"

# ... (ton code existant) ...


class Orders(OrdersTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.load_orders()

    def load_orders(self):
        try:
            user_info = anvil.server.call('get_user_info')
            orders = anvil.server.call('get_user_orders', user_info['user_id'])
            self.repeating_panel_1.items = orders
        except Exception as e:
            Notification(f"Erreur lors du chargement des commandes : {e}", style="warning").show()

    def view_details_click(self, **event_args):
        try:
            order_id = event_args['sender'].item['id']
            user_info = anvil.server.call('get_user_info')
            order = anvil.server.call('get_order_details', order_id, user_info['user_id'])
            if order:
                alert(str(order), large=True)
            else:
                Notification("Impossible de charger les détails de la commande", style="danger").show()
        except Exception as e:
            Notification(f"Erreur lors du chargement des détails : {e}", style="danger").show()

    def menu_button_click(self, **event_args):
        """Gère le clic sur le bouton Retour au Menu."""
        get_open_form().load_page('menu')


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

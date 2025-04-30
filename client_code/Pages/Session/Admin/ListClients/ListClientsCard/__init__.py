from ._anvil_designer import ListClientsCardTemplate
from anvil import *
import anvil.server

class ListClientsCard(ListClientsCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.display_client()

  def display_client(self):
    client = self.item
    print("👤 Affichage du client :", client)

    # Affichage des informations du client
    self.label_name.text = f"{client['firstname']} {client['lastname']}"
    self.label_email.text = client['email']
    self.label_role.text = "Admin" if client['is_admin'] else "Client"
    
    # Affichage de la photo de profil si disponible
    if client['photo']:
      self.profile_photo.source = client['photo']
    else:
      self.profile_photo.source = "https://ui-avatars.com/api/?name=" + client['firstname'] + "+" + client['lastname']

  def desactiver_click(self, **event_args):
    """Cette méthode sera appelée quand le bouton de désactivation sera cliqué"""
    try:
      # Appel au serveur pour désactiver le compte
      result = anvil.server.call('deactivate_user', self.item['email'])
      if result:
        Notification("Compte désactivé avec succès", style="success").show()
        # Rafraîchir l'affichage
        self.parent.parent.load_clients()
      else:
        Notification("Erreur lors de la désactivation du compte", style="danger").show()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()
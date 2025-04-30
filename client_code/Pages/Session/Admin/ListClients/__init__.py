from ._anvil_designer import ListClientsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ListClientsCard import ListClientsCard

class ListClients(ListClientsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    print("📄 Page ListClients chargée")

    self.load_clients()

  def load_clients(self):
    try:
      print("🔄 Appel serveur pour récupérer les utilisateurs...")
      clients = anvil.server.call('get_all_users')  # Utilisation de la fonction existante
      print(f"✅ {len(clients)} clients reçus")

      self.repeating_panel_1.item_template = ListClientsCard
      self.repeating_panel_1.items = clients

    except Exception as e:
      print(f"❌ Erreur lors de la récupération des clients : {e}")
      Notification(f"Erreur lors du chargement des clients : {e}", style="danger").show()

from anvil import *
import anvil.server

class ListClientsCard():
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_clients()

  def load_clients(self):
    try:
      print("🔄 Chargement des clients...")
      self.clients = anvil.server.call('get_all_users')
      print(f"✅ {len(self.clients)} clients trouvés")
      self.clients_repeating_panel.items = self.clients
    except Exception as e:
      print(f"❌ Erreur lors du chargement des clients : {e}")
      Notification(f"Erreur lors du chargement : {e}", style="danger").show()
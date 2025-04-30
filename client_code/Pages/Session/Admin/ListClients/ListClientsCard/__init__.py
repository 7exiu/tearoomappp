from ._anvil_designer import ListClientsCardTemplate
from anvil import *

class ListClientsCard(ListClientsCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.display_client()

  def display_client(self):
    client = self.item
    print("👤 Affichage du client :", client)

    self.label_name.text = f"{client['firstname']} {client['lastname']}"
    self.label_email.text = client['email']
    self.label_role.text = "Admin" if client.get('is_admin') else "Client"
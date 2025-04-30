from ._anvil_designer import OrderDetailsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state

class OrderDetails(OrderDetailsTemplate):
  def __init__(self, order=None, **properties):
    self.init_components(**properties)
    if order:
      self.load_order_details(order)

  def load_order_details(self, order):
    """Charge les détails de la commande."""
    # Mettre à jour l'interface avec les détails de la commande
    self.order_id_label.text = f"Commande #{order['id']}"
    self.order_date_label.text = f"Date: {order['time'].strftime('%d/%m/%Y %H:%M')}"
    self.order_status_label.text = f"Statut: {'Réservé' if order['is_available'] else 'Disponible'}"
    self.order_name_label.text = order['name']
    self.order_price_label.text = f"{order['price']:.2f} €"
    if 'description' in order:
      self.order_description_label.text = order['description']
    else:
      self.order_description_label.text = "Aucune description disponible"

  def receipt_button_click(self, **event_args):
    """Gère le clic sur le bouton Télécharger le reçu."""
    order_id = self.order_id_label.text.split('#')[1]
    receipt = anvil.server.call('generate_receipt', order_id)
    if receipt:
      anvil.media.download(receipt)
    else:
      Notification("Impossible de générer le reçu", style="danger").show()

  def close_button_click(self, **event_args):
    """Ferme la fenêtre de détails."""
    self.raise_event('x-close-alert') 
from ._anvil_designer import OrdersTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state
from .OrderDetails import OrderDetails

class Orders(OrdersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_orders()

    # Any code you write here will run before the form opens.

  def load_orders(self):
    """Charge les commandes de l'utilisateur."""
    user_id = state.user['id']
    orders = anvil.server.call('get_user_orders', user_id)
    
    # Formater les commandes pour l'affichage
    formatted_orders = []
    for order in orders:
      formatted_orders.append({
        'id': order['id'],
        'time': order['time'].strftime('%d/%m/%Y %H:%M'),
        'status': 'Réservé' if order['is_available'] else 'Disponible',
        'name': order['name'],
        'price': f"{order['price']:.2f}"
      })
    
    # Mettre à jour le repeating panel
    self.repeating_panel_1.items = formatted_orders

  def view_details_click(self, **event_args):
    """Gère le clic sur le bouton Voir les détails."""
    order_id = event_args['sender'].item['id']
    order = anvil.server.call('get_order_details', order_id)
    if order:
      alert(OrderDetails(order=order), large=True)
    else:
      Notification("Impossible de charger les détails de la commande", style="danger").show()

  def menu_button_click(self, **event_args):
    """Gère le clic sur le bouton Retour au Menu."""
    get_open_form().load_page('menu')

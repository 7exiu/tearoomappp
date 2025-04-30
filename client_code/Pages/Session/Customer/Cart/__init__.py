from ._anvil_designer import CartTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
# CartForm.py
from anvil import *
from .... import state
from .SouCart import SouCart

class Cart(CartTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.cart_repeating_panel.item_template = SouCart
        self.load_cart()


    def button_pop_click(self, **event_args):
      alert("Votre commande a était prise en compte")
      anvil.server.call('delete_card')



    def load_cart(self):
        try:
            user_info = anvil.server.call('get_user_info')
            cart = anvil.server.call('get_cart', user_info['user_id'])
            if cart:
                self.cart_repeating_panel.items = cart['content']
                self.update_total()
            else:
                self.cart_repeating_panel.items = []
                self.total_label.text = "Total: 0 €"
        except Exception as e:
            Notification(f"Erreur lors du chargement du panier : {e}", style="warning").show()

    def update_total(self):
        total = 0
        for item in self.cart_repeating_panel.items:
            total += item['price'] * item['quantity']
        self.total_label.text = f"Total: {total} €"

    def dashboard_button_click(self, **event_args):
        get_open_form().load_page('dashboard')

    def outlined_button_1_click(self, **event_args):
        try:
            user_info = anvil.server.call('get_user_info')
            order = anvil.server.call('create_order', user_info['user_id'], self.cart_repeating_panel.items)
            if order:
                Notification("Commande validée avec succès !", style="success").show()
                self.load_cart()
            else:
                Notification("Erreur lors de la validation de la commande", style="danger").show()
        except Exception as e:
            Notification(f"Erreur lors de la validation de la commande : {e}", style="danger").show()


    def calculer_total(self):
      total = sum(item['price'] for item in state.cart_items)
      print("Total du panier :", total)
      return total
  


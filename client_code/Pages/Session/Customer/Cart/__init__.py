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
      self.load_cart()
      self.update_dashboard_button()

    def load_cart(self):
      # Récupérer le panier de l'utilisateur
      user_id = anvil.server.call('get_user_info')['user_id']
      cart = anvil.server.call('get_cart', user_id)
      
      if cart:
        self.cart_repeating_panel.items = cart['content']
        self.update_total()
      else:
        self.cart_repeating_panel.items = []
        self.total_label.text = "Total: 0 €"

    def update_total(self):
      total = 0
      for item in self.cart_repeating_panel.items:
        total += item['price'] * item['quantity']
      self.total_label.text = f"Total: {total} €"

    def update_dashboard_button(self):
      # Vérifier si une session est active
      user_info = anvil.server.call('get_user_info')
      self.dashboard_button.enabled = bool(user_info)

    def dashboard_button_click(self, **event_args):
      get_open_form().load_page('dashboard')

    def outlined_button_1_click(self, **event_args):
      # Logique de commande existante
      pass

    def calculer_total(self):
      total = sum(item['price'] for item in state.cart_items)
      print("Total du panier :", total)
      return total
  


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
      self.cart = anvil.server.call('get_card')
      self.cart_repeating_panel.items = self.cart
      print(self.cart)
      total = sum(item['price'] for item in self.cart)
      self.total_label.text = f"Total : {total} €"
      self.code_label.text = "Code a 16 chiffres"
      self.date_label.text = "Date expiration"
      self.crypto_label.text = "cryptogramme"
      self.outlined_button_1.set_event_handler('click', self.button_pop_click)

    def button_pop_click(self, **event_args):
      alert("Votre commande a était prise en compte")

    def calculer_total(self):
      total = sum(item['price'] for item in state.cart_items)
      print("Total du panier :", total)
      return total
  


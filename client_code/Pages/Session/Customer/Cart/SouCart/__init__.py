from ._anvil_designer import SouCartTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import state

class SouCart(SouCartTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    print("la ca marche")
    self.form_show()

    
  def form_show(self, **event_args):
        cart = self.item

        print(">>> item reçu dans cartCard :", self.item)

        self.cart_name.text = cart["name"]
        img = cart["image"]
        if isinstance(img, Media) or isinstance(img, str):
            self.cart_image.source = img
        else:
          self.cart_image.source = "https://placehold.co/200x150?text=Image+manquante"

        self.cart_price.text = f"{cart['price']}"
        print("Prix affiché :", self.cart_price.text)
    
        




from ._anvil_designer import TeaCardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import state

class TeaCard(TeaCardTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.add_to_cart_button.set_event_handler('click', self.add_to_cart_button_click)

    def form_show(self, **event_args):
        tea = self.item
        self.cart_name.text = tea["name"]
        img = tea["image"]
        if isinstance(img, Media) or isinstance(img, str):
            self.cart_image.source = img
        else:
            self.cart_image.source = "https://placehold.co/200x150?text=Image+manquante"
        self.cart_price.text = f"{tea['price']} €"
        self.cart_description.text = tea["description"]

    def add_to_cart_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        tea = self.item
        row_id = tea.get_id()
        anvil.server.call('addcard', row_id)



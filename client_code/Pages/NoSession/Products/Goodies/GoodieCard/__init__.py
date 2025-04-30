from ._anvil_designer import GoodieCardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import state

class GoodieCard(GoodieCardTemplate):
    def __init__(self, **properties):
      self.init_components(**properties)
      self.add_to_cart_button.set_event_handler('click', self.add_to_cart_button_click)


    def form_show(self, **event_args):
      goodie = self.item
      img = self.item.get("image")
      if isinstance(img, Media) or isinstance(img, str):
        self.goodie_image.source = img
      else:
        self.goodie_image.source = "https://placehold.co/200x150?text=Image+manquante"
      self.goodie_name.text = goodie["name"]
      self.goodie_price.text = goodie["price"]
      self.goodie_description.text = goodie["description"]
      
    def button_add_click(self, **event_args):
      #state.add_to_cart(self.item)
      pass

    def add_to_cart_button_click(self, **event_args):
      goodie = self.item
      row_id = goodie.get_id()
      print(row_id)
      cleaned_str = row_id.strip("[]")
      numbers = cleaned_str.split(',')
      result = numbers[1] if len(numbers) > 1 else None
      print(result, "dkfhqslkjgfhqszkhgfghqsKHASHGKHYH")
      anvil.server.call('addgoodie' , row_id)


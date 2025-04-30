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

        print(">>> item reçu dans TeaCard :", self.item)

        self.tea_name.text = tea["name"]
        img = tea["image"]
        if isinstance(img, Media) or isinstance(img, str):
            self.tea_image.source = img
        else:
          self.tea_image.source = "https://placehold.co/200x150?text=Image+manquante"

        #self.tea_price.text = f"{tea['price']} €"
        print("Prix affiché :", self.tea_price.text)
    
        self.tea_description.text = tea["description"]


    def button_add_click(self, **event_args):
      pass

  
    def add_to_cart_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      
      tea = self.item
      row_id = tea.get_id()
      print(row_id)
      cleaned_str = row_id.strip("[]")
      numbers = cleaned_str.split(',')
      result = numbers[1] if len(numbers) > 1 else None
      print(result, "dkfhqslkjgfhqszkhgfghqsKHASHGKHYH")
      anvil.server.call('addcard' , row_id)
      pass



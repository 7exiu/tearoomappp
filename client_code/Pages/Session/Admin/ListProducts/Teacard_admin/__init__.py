from ._anvil_designer import Teacard_adminTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Teacard_admin(Teacard_adminTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
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

    # Any code you write here will run before the form opens.

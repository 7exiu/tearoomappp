from ._anvil_designer import TableCardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TableCard(TableCardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    tearoom_table = self.item 
    self.table_card_is_available.text = "Available" if tearoom_table["is_available"]  else 'Not available'
    self.table_card_capacity.text = str(tearoom_table["chairs_count"]) + " people"
    
  
  def table_card_booking_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

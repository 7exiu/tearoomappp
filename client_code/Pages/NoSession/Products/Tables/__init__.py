from ._anvil_designer import TablesTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .TableCard import TableCard


class Tables(TablesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      tables = anvil.server.call('get_tables')
      print(tables)
      self.tables_repeating_panel.item_template = TableCard
      self.tables_repeating_panel.items = tables
    except:
      pass
      

    # Any code you write here will run before the form opens.

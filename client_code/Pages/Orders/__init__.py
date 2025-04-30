from ._anvil_designer import OrdersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Orders(OrdersTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.load_orders()
        
    def load_orders(self):
        """Charge les commandes de l'utilisateur"""
        user = anvil.users.get_user()
        if not user:
            self.orders_panel.items = []
            return
            
        orders = anvil.server.call('get_user_orders')
        self.orders_panel.items = orders 
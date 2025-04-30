from ._anvil_designer import CartTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .CartItemPanel import CartItemPanel

class Cart(CartTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.repeating_panel_1.item_template = CartItemPanel
        self.load_cart()
        
    def load_cart(self):
        """Charge le panier de l'utilisateur"""
        user = anvil.users.get_user()
        if not user:
            self.repeating_panel_1.items = []
            self.total_label.text = "Total : 0.00 €"
            return
            
        cart_items = anvil.server.call('panier')
        if not cart_items:
            self.repeating_panel_1.items = []
            self.total_label.text = "Total : 0.00 €"
            return
            
        self.repeating_panel_1.items = cart_items
        total = sum(item['price'] for item in cart_items)
        self.update_total(total)
        
    def update_total(self, amount):
        """Met à jour le total du panier"""
        self.total_label.text = f"Total : {amount:.2f} €"
        
    def remove_item_click(self, item, **event_args):
        """Supprime un article du panier"""
        user = anvil.users.get_user()
        if user:
            anvil.server.call('remove_from_cart', user['id'], item['id'])
            self.load_cart()
            
    def update_quantity(self, item, quantity, **event_args):
        """Met à jour la quantité d'un article"""
        user = anvil.users.get_user()
        if user and quantity > 0:
            anvil.server.call('update_quantity', user['id'], item['id'], quantity)
            self.load_cart()
            
    def clear_cart_click(self, **event_args):
        """Vide le panier"""
        user = anvil.users.get_user()
        if user:
            anvil.server.call('delete_card')
            self.load_cart()
            
    def checkout_click(self, **event_args):
        """Passe à la caisse"""
        user = anvil.users.get_user()
        if not user:
            alert("Veuillez vous connecter pour passer commande")
            return
            
        cart_items = anvil.server.call('panier')
        if not cart_items:
            alert("Votre panier est vide")
            return
            
        # Rediriger vers la page de paiement
        open_form('Checkout') 
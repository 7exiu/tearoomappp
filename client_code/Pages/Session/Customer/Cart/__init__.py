from ._anvil_designer import CartTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from .... import state
from .SouCart import SouCart

class Cart(CartTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Configuration du repeating panel
        self.cart_repeating_panel.item_template = SouCart
        
        # Récupération des articles
        self.cart = anvil.server.call('get_card')
        self.cart_repeating_panel.items = self.cart
        print("🛒 Articles dans le panier :", self.cart)

        # Calcul du total
        total = sum(item['price'] for item in self.cart)
        self.total_label.text = f"Total : {total} €"

        # Champs placeholder
        self.code_label.text = "Code à 16 chiffres"
        self.date_label.text = "Date expiration"
        self.crypto_label.text = "Cryptogramme"

        # Connexion du bouton à son événement
        self.outlined_button_1.set_event_handler('click', self.outlined_button_1_click)

    def calculer_total(self):
        total = sum(item['price'] for item in self.cart)
        print("Total du panier :", total)
        return total

    def outlined_button_1_click(self, **event_args):
        try:
            anvil.server.call('delete_card')
            Notification("✅ Votre commande a été prise en compte.").show()
            self.cart_repeating_panel.items = []  # Réinitialiser le panier côté client
            self.total_label.text = "Total : 0 €"
        except Exception as e:
            print(f"❌ Erreur lors de la commande : {e}")
            Notification(f"Erreur lors de la commande : {e}").show()

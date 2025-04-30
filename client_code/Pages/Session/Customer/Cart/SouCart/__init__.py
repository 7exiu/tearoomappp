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

    def form_show(self, **event_args):
        # Appel serveur : récupère uniquement les articles du panier (déjà filtrés dans la fonction `panier`)
        user_cart_items = anvil.server.call("panier")
        

        print(">>> Items filtrés pour l'utilisateur:", user_cart_items)

        if user_cart_items:
            cart = user_cart_items[0]  # Affiche le premier item du panier
            self.cart_name.text = cart["name"]
            img = cart["image"]
            if isinstance(img, Media) or isinstance(img, str):
                self.cart_image.source = img
            else:
                self.cart_image.source = "https://placehold.co/200x150?text=Image+manquante"
            self.cart_price.text = f"{cart['price']}"
            print("Prix affiché :", self.cart_price.text)
        else:
            # Aucun article dans le panier
            self.cart_name.text = "Aucun article en attente dans votre panier"
            self.cart_image.source = None
            self.cart_price.text = ""

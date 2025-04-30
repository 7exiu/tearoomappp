from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CartTemplate(Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Création des composants
        self.cart_panel = Panel()
        self.cart_panel.role = "cart-panel"
        
        # Titre du panier
        self.title_label = Label(text="Votre Panier")
        self.title_label.role = "cart-title"
        self.cart_panel.add_component(self.title_label)
        
        # Panel pour les articles
        self.cart_items_panel = RepeatingPanel()
        self.cart_items_panel.role = "cart-items"
        self.cart_items_panel.item_template = CartItemTemplate()
        self.cart_panel.add_component(self.cart_items_panel)
        
        # Panel pour le total
        self.total_panel = Panel()
        self.total_panel.role = "cart-total"
        
        self.total_label = Label(text="Total : 0.00 €")
        self.total_label.role = "total-label"
        self.total_panel.add_component(self.total_label)
        
        # Boutons d'action
        self.buttons_panel = FlowPanel()
        self.buttons_panel.role = "cart-buttons"
        
        self.clear_button = Button(text="Vider le panier")
        self.clear_button.role = "clear-button"
        self.clear_button.set_event_handler('click', self.clear_cart_click)
        
        self.checkout_button = Button(text="Passer la commande")
        self.checkout_button.role = "checkout-button"
        self.checkout_button.set_event_handler('click', self.checkout_click)
        
        self.buttons_panel.add_component(self.clear_button)
        self.buttons_panel.add_component(self.checkout_button)
        
        self.total_panel.add_component(self.buttons_panel)
        self.cart_panel.add_component(self.total_panel)
        
        self.add_component(self.cart_panel)

class CartItemTemplate(Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        self.item_panel = Panel()
        self.item_panel.role = "cart-item"
        
        # Image du produit
        self.item_image = Image()
        self.item_image.width = 80
        self.item_panel.add_component(self.item_image)
        
        # Détails de l'article
        self.details_panel = Panel()
        self.details_panel.role = "item-details"
        
        self.item_name_label = Label()
        self.item_name_label.role = "item-name"
        self.details_panel.add_component(self.item_name_label)
        
        self.item_price_label = Label()
        self.item_price_label.role = "item-price"
        self.details_panel.add_component(self.item_price_label)
        
        self.item_panel.add_component(self.details_panel)
        self.add_component(self.item_panel)
        
    def form_show(self, **event_args):
        """Affiche les détails de l'article"""
        self.item_image.source = self.item['image']
        self.item_name_label.text = self.item['name']
        self.item_price_label.text = f"{self.item['price']:.2f} €"

    def clear_cart_click(self, **event_args):
        """Gère le clic sur le bouton vider le panier"""
        pass
        
    def checkout_click(self, **event_args):
        """Gère le clic sur le bouton passer la commande"""
        pass

    def form_show(self, **event_args):
        self.cart_items_panel.items = []
        self.total_label.text = "Total : 0.00 €"
        
    def cart_item_show(self, **event_args):
        """Affiche un article du panier"""
        self.item_name_label.text = self.item['name']
        self.item_price_label.text = f"{self.item['price']:.2f} €"
        self.quantity_input.text = str(self.item['quantity'])
        
    def quantity_input_change(self, **event_args):
        """Gère le changement de quantité"""
        try:
            quantity = int(self.quantity_input.text)
            if quantity > 0:
                self.parent.update_quantity(self.item, quantity)
        except ValueError:
            pass
            
    def remove_button_click(self, **event_args):
        """Supprime l'article du panier"""
        self.parent.remove_item_click(self.item) 
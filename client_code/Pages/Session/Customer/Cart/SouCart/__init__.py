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
    self.form_show()

  def update_quantity(self, new_quantity):
    if new_quantity >= 1:
      self.item['quantity'] = new_quantity
      self.quantity_label.text = str(new_quantity)
      self.parent.parent.update_total()

  def decrease_button_click(self, **event_args):
    current_quantity = int(self.quantity_label.text)
    self.update_quantity(current_quantity - 1)

  def increase_button_click(self, **event_args):
    current_quantity = int(self.quantity_label.text)
    self.update_quantity(current_quantity + 1)

  def delete_button_click(self, **event_args):
    # Supprimer l'article du panier
    cart_items = self.parent.parent.cart_repeating_panel.items
    cart_items.remove(self.item)
    self.parent.parent.cart_repeating_panel.items = cart_items
    self.parent.parent.update_total()

  def form_show(self, **event_args):
    try:
      # Récupérer toutes les cartes depuis la table temp
      cards = anvil.server.call('get_card')

      if not cards:
        print("❌ Aucune carte trouvée dans la table temp.")
        self.cart_name.text = "Aucune carte"
        return

      # Ici on prend simplement la première (ou tu peux faire une logique + avancée)
      cart = cards[0]
      print(">>> Carte chargée depuis la DB temp :", cart)

      # Nom
      self.cart_name.text = cart.get("name", "Nom inconnu")

      # Image
      img = cart.get("image")
      self.cart_image.source = img if isinstance(img, (Media, str)) else "https://placehold.co/200x150?text=Image+manquante"

      # Prix
      self.cart_price.text = f"{cart.get('price', 0)} €"

      # Date (optionnelle selon ta table)
      if "time" in cart and cart["time"]:
        self.cart_date.text = cart["time"].strftime("%d/%m/%Y %H:%M")
      else:
        self.cart_date.text = "Date non disponible"

    except Exception as e:
      print(f"❌ Erreur lors du chargement de la carte : {e}")

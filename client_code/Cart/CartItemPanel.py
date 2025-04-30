from ._anvil_designer import CartItemPanelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CartItemPanel(CartItemPanelTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.refresh_data()

  def refresh_data(self):
    # Afficher les données de l'article
    if self.item:
      self.image_produit.source = self.item['image']
      self.nom_produit.text = self.item['name']
      self.prix_produit.text = f"{self.item['price']:.2f} €"
      self.description_produit.text = self.item['description'] 
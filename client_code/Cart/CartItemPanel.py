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
    # Configuration du gestionnaire d'événements pour le bouton de suppression
    self.delete_button.set_event_handler('click', self.delete_click)
    self.refresh_data()

  def refresh_data(self):
    """Affiche les données de l'article"""
    if self.item:
      self.image_produit.source = self.item['image']
      self.nom_produit.text = self.item['name']
      self.prix_produit.text = f"{self.item['price']:.2f} €"
      self.description_produit.text = self.item['description']
      
  def delete_click(self, **event_args):
    """Gère le clic sur le bouton de suppression"""
    if self.item:
      # Marquer l'article comme supprimé en utilisant la fonction existante
      self.item['etat'] = True
      # Rafraîchir le panier
      self.parent.parent.load_cart() 
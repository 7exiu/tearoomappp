from anvil import *

class CartItemPanelTemplate(Container):
  def __init__(self, **properties):
    # Initialisation du conteneur
    self.init_components(**properties)
    
    # Création du panel principal
    self.item_container = Container()
    self.item_container.role = "cart-item"
    
    # Image du produit
    self.image_produit = Image(width=100)
    self.item_container.add_component(self.image_produit)
    
    # Panel pour les informations textuelles
    self.info_panel = FlowPanel()
    self.info_panel.role = "item-details"
    
    # Nom du produit
    self.nom_produit = Label()
    self.nom_produit.role = "item-name"
    self.info_panel.add_component(self.nom_produit)
    
    # Prix du produit
    self.prix_produit = Label()
    self.prix_produit.role = "item-price"
    self.info_panel.add_component(self.prix_produit)
    
    # Description du produit
    self.description_produit = Label()
    self.description_produit.role = "item-description"
    self.info_panel.add_component(self.description_produit)
    
    # Ajout du panel d'informations au conteneur principal
    self.item_container.add_component(self.info_panel)
    
    # Ajout du conteneur principal à this
    self.add_component(self.item_container) 
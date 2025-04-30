from anvil import *

class CartItemPanelTemplate(Container):
  def __init__(self, **properties):
    # Initialisation du conteneur
    self.init_components(**properties)
    
    # Création du panel principal
    self.item_container = GridPanel(spacing="10")
    self.item_container.role = "cart-item"
    
    # Image du produit
    self.image_produit = Image(width=100, height=100, display_mode="shrink_to_fit")
    self.item_container.add_component(self.image_produit, row="0", col="0", width_xs=120)
    
    # Panel pour les informations
    self.info_panel = GridPanel(spacing="5")
    
    # Nom du produit
    self.nom_produit = Label(font_size=16, font_weight="bold")
    self.nom_produit.role = "item-name"
    self.info_panel.add_component(self.nom_produit, row="0", col_xs=12)
    
    # Prix du produit
    self.prix_produit = Label(font_size=14)
    self.prix_produit.role = "item-price"
    self.info_panel.add_component(self.prix_produit, row="1", col_xs=12)
    
    # Description du produit
    self.description_produit = Label(font_size=12)
    self.description_produit.role = "item-description"
    self.info_panel.add_component(self.description_produit, row="2", col_xs=12)
    
    # Ajout du panel d'informations
    self.item_container.add_component(self.info_panel, row="0", col="1")
    
    # Bouton de suppression
    self.delete_button = Button(text="Retirer", icon="fa:trash", background="#dc3545", foreground="white")
    self.delete_button.role = "remove-button"
    self.item_container.add_component(self.delete_button, row="0", col="2", width_xs=100)
    
    # Ajout du conteneur principal
    self.add_component(self.item_container) 
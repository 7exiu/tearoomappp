from ._anvil_designer import AddProductTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

class AddProduct(AddProductTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def add_pd_click(self, **event_args):
    """Méthode appelée lorsque le bouton 'Ajouter Produit' est cliqué"""
    try:
      print("🛠 Tentative d'ajout de produit...")

      name = self.add_pb_name.text
      description = self.add_description.text
      price_text = self.add_price.text
      image = self.file_loader_1.file
      category = self.category_dropdown.selected_value

      # Vérification des champs
      if not name or not description or not price_text or not category:
        alert("Tous les champs obligatoires doivent être remplis.")
        print("❌ Champs manquants")
        return

      # Conversion du prix
      try:
        price = float(price_text)
      except ValueError:
        alert("Le prix doit être un nombre.")
        print("❌ Erreur de type sur le prix")
        return

      # Conversion de la catégorie
      category = 'tea' if category == 'Thé' else 'goodie'

      # Appel au serveur
      result = anvil.server.call('add_product_to_catalog', name, description, price, image, category)
      
      print(f"✅ Produit ajouté avec succès : {result}")
      Notification(result).show()

      # Réinitialisation du formulaire
      self.add_pb_name.text = ""
      self.add_description.text = ""
      self.add_price.text = ""
      self.file_loader_1.clear()
      self.category_dropdown.selected_value = None

    except Exception as e:
      print(f"❌ Erreur inattendue : {e}")
      alert(f"Erreur lors de l'ajout : {str(e)}")
    
  def add_pb_name_pressed_enter(self, **event_args):
    pass

  def add_price_pressed_enter(self, **event_args):
    pass

  def add_description_pressed_enter(self, **event_args):
    pass


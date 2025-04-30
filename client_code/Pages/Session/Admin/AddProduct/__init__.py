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

      # Vérification des champs
      if not name or not description or not price_text:
        Notification("Tous les champs obligatoires doivent être remplis.", style="danger").show()
        print("❌ Champs manquants")
        return

      # Conversion du prix et du stock
      try:
        price = float(price_text)
      except ValueError:
        Notification("Le prix doit être un nombre.", style="danger").show()
        print("❌ Erreur de type sur le prix")
        return

      # Appel au serveur
      result = anvil.server.call('add_product', name, description, price, image)
      
      print(f"✅ Produit ajouté avec succès : {result}")
      Notification(result, style="success").show()

      # Réinitialisation du formulaire
      self.add_pb_name.text = ""
      self.add_description.text = ""
      self.add_price.text = ""
      self.file_loader_1.clear()  


    except Exception as e:
      print(f"❌ Erreur inattendue : {e}")
      Notification(f"Erreur lors de l'ajout : {e}", style="danger").show()
    
def add_pb_name_pressed_enter(self, **event_args):
    pass

def add_price_pressed_enter(self, **event_args):
    pass

def add_description_pressed_enter(self, **event_args):
    pass


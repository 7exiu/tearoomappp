from ._anvil_designer import AddProductTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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
      stock_text = self.stock_textbox.text
      photo = self.photo_loader.file
      category = self.category_textbox.text

      # Vérification des champs
      if not name or not description or not price_text or not stock_text:
        Notification("Tous les champs obligatoires doivent être remplis.", style="danger").show()
        print("❌ Champs manquants")
        return

      # Conversion du prix et du stock
      try:
        price = float(price_text)
        stock = int(stock_text)
      except ValueError:
        Notification("Le prix doit être un nombre et le stock un entier.", style="danger").show()
        print("❌ Erreur de type sur le prix ou stock")
        return

      # Appel au serveur
      result = anvil.server.call('add_product', name, description, price, stock, photo)
      
      print(f"✅ Produit ajouté avec succès : {result}")
      Notification(result, style="success").show()

      # Optionnel : réinitialiser le formulaire
      self.add_pb_name.text = ""
      self.add_description.text = ""
      self.add_price.text = ""
      self.stock_textbox.text = ""
      self.file_loader_1.file = None
      

    except Exception as e:
      print(f"❌ Erreur inattendue : {e}")
      Notification(f"Erreur lors de l'ajout : {e}", style="danger").show()

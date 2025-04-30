from ._anvil_designer import ListProductsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from .Teacard_admin import Teacard_admin
from .Goodiescard_admin import Goodiescard_admin
from .TableCard_admin import TableCard_admin  # Ajout de l'import manquant

class ListProducts(ListProductsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Chargement des thés
    self.teas_repeating_panel.item_template = Teacard_admin
    try:
      self.teas = anvil.server.call('get_teas')
      self.teas_repeating_panel.items = self.teas
      print(f"✅ Thés récupérés : {self.teas}")
    except Exception as e:
      print(f"❌ Erreur lors du chargement des thés : {e}")
      Notification(f"Erreur chargement thés : {e}", style="danger").show()

    # Chargement des goodies
    self.goodies_repeating_panel.item_template = Goodiescard_admin
    if not anvil.server.is_app_online():
      print("⚠️ Application hors ligne : chargement de goodies par défaut.")
      self.goodies_repeating_panel.items = [
        {"name": "Pancake", "price": 2.50, "image": "https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", "description": "Pancakes of Mami Jaja"},
        {"name": "Crêpe", "price": 4.80, "image":"https://images.pexels.com/photos/2613471/pexels-photo-2613471.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", "description": "French Crêpes By Laurent Pi"}
      ]
    else:
      try:
        goodies = anvil.server.call('get_goodies')
        self.goodies_repeating_panel.items = goodies
        print(f"✅ Goodies récupérés : {goodies}")
      except Exception as e:
        print(f"❌ Erreur lors du chargement des goodies : {e}")
        Notification(f"Erreur chargement goodies : {e}", style="danger").show()

    # Chargement des tables
    self.tables_repeating_panel.item_template = TableCard_admin
    try:
      tables_data = anvil.server.call('get_tables')
      self.tables_repeating_panel.items = tables_data
      print(f"✅ Tables récupérées : {tables_data}")
    except Exception as e:
      print(f"❌ Erreur lors du chargement des tables : {e}")
      Notification(f"Erreur chargement tables : {e}", style="danger").show()

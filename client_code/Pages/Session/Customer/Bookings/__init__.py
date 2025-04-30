from ._anvil_designer import BookingsTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables
from ....NoSession.Products.Tables import Tables
from ....NoSession.Products.Goodies.GoodieCard import GoodieCard
from ....NoSession.Products.Teas.TeaCard import TeaCard
from ....NoSession.Products.Tables.TableCard import TableCard


class Bookings(BookingsTemplate):
    def __init__(self, **properties):
        # Initialisation des propriétés et des composants
        self.init_components(**properties)
        self.load_tables_page()
        self.display_goodies()
        self.display_teas()

    def load_tables_page(self):
      try:
            # Appel serveur pour récupérer les goodies
            tables = anvil.server.call('get_tables')
            print(f"Tables chargés : {tables}")
            
            # Réinitialiser les composants existants avant d'ajouter les nouveaux
            self.tables_panel.clear()
            
            # Ajouter chaque image de goodie au flow panel des goodies
            for tables in tables:
                # Créez une carte GoodieCard pour chaque goodie et ajoutez-la à column_panel_1
                tablecard = TableCard(item=tables)
                self.tables_panel.add_component(tablecard)
      except Exception as e:
            alert(f"Erreur lors du chargement des images des goodies : {e}")

    def display_goodies(self):
      try:
        goodies = anvil.server.call('get_goodies')
        for goodie in goodies:
          self.goodie_panel.add_component(Image(source=goodie['image']))
      except Exception as e:
        alert(f"Erreur lors du chargement des images : {e}")

    
    def display_teas(self):
     try:
      teas = anvil.server.call('get_teas')
      for tea in teas:
        self.teas_panel.add_component(Image(source=tea['image']))
     except Exception as e:
      alert(f"Erreur lors du chargement des images : {e}")

    def form_show(self, **event_args):
        """Cette méthode est appelée quand le formulaire est affiché"""
        pass  # Vous pouvez éventuellement personnaliser davantage ici si nécessaire

    def cart_link_click(self, **event_args):
        """Clique sur le lien 'Panier'"""
        get_open_form().load_page("cart")

    def orders_link_click(self, **event_args):
        """Clique sur le lien 'Commandes'"""
        get_open_form().load_page("orders")

    def profile_link_click(self, **event_args):
        """Clique sur le lien 'Profil'"""
        get_open_form().load_page("profile")

    def teas_list_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass

    def goodies_list_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass



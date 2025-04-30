from ._anvil_designer import BookingsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....NoSession.Products.Tables.TableCard import TableCard
from ....NoSession.Products.Goodies.GoodieCard import GoodieCard
from ....NoSession.Products.Teas.TeaCard import TeaCard

from anvil.tables import app_tables
from ....NoSession.Products.Tables import Tables
from ....NoSession.Products.Goodies.GoodieCard import GoodieCard
from ....NoSession.Products.Teas.TeaCard import TeaCard
from ....NoSession.Products.Tables.TableCard import TableCard



class Bookings(BookingsTemplate):
    def __init__(self, **properties):
        # Initialisation des propriétés et des composants
        self.init_components(**properties)
        self.display_tables()
        self.display_goodies()
        self.display_teas()

    def display_tables(self):
        try:
            tables = anvil.server.call('get_tables')
            self.tables_panel.clear()
            for table in tables:
                self.tables_panel.add_component(Image(source=table['image']))
        except Exception as e:
            Notification(f"Erreur lors du chargement des tables : {e}", style="warning").show()

    def display_goodies(self):
        try:
            goodies = anvil.server.call('get_goodies')
            self.goodie_panel.clear()
            for goodie in goodies:
                self.goodie_panel.add_component(Image(source=goodie['image']))
        except Exception as e:
            Notification(f"Erreur lors du chargement des goodies : {e}", style="warning").show()

    def display_teas(self):
        try:
            teas = anvil.server.call('get_teas')
            self.teas_panel.clear()
            for tea in teas:
                self.teas_panel.add_component(Image(source=tea['image']))
        except Exception as e:
            Notification(f"Erreur lors du chargement des thés : {e}", style="warning").show()

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
        get_open_form().load_page("teas")

    def goodies_list_button_click(self, **event_args):
        get_open_form().load_page("goodies")
      


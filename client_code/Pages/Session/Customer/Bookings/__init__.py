from ._anvil_designer import BookingsTemplate
from anvil import *
import anvil.server
from .TableCard import TableCard
from .GoodieCard import GoodieCard
from .TeaCard import TeaCard


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

        self.setup_ui()
        self.load_tables()
        self.load_goodies()
        self.load_teas()

    def load_tables(self):
        try:
            tables = anvil.server.call('get_tables')
            self.tables_panel.clear()
            for table in tables:
                self.tables_panel.add_component(TableCard(item=table))
        except Exception as e:
            Notification(f"Erreur lors du chargement des tables : {e}", style="warning").show()

    def load_goodies(self):
        try:
            goodies = anvil.server.call('get_goodies')
            self.goodie_panel.clear()
            for goodie in goodies:
                self.goodie_panel.add_component(GoodieCard(item=goodie))
        except Exception as e:
            Notification(f"Erreur lors du chargement des goodies : {e}", style="warning").show()

    def load_teas(self):
        try:
            teas = anvil.server.call('get_teas')
            self.teas_panel.clear()
            for tea in teas:
                self.teas_panel.add_component(TeaCard(item=tea))
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
      


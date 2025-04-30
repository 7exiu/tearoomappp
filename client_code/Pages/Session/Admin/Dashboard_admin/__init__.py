from ._anvil_designer import Dashboard_adminTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from ..AddProduct import AddProduct
from ..ListClients import ListClients
from ..ListProducts import ListProducts
from ... import Customer
from ...Customer.Profile import Profile


class Dashboard_admin(Dashboard_adminTemplate):
    def __init__(self, **properties):
        print("🛠 Initialisation du Dashboard Administrateur...")
        self.init_components(**properties)
        self.current_page = None

        try:
            print("📡 Connexion au serveur pour récupérer les informations utilisateur...")
            self.user_info = anvil.server.call("get_user_info")
            print(f"✅ Infos utilisateur récupérées : {self.user_info}")

            if not self.user_info.get("user_email"):
                raise ValueError("Aucun email utilisateur récupéré.")

            print("🔎 Recherche de l'utilisateur dans la base de données...")
            self.user = anvil.server.call("get_user_by_email", self.user_info["user_email"])

            if not self.user:
                raise ValueError("Utilisateur introuvable dans la base de données.")

            print(f"🎯 Utilisateur trouvé : {self.user}")

            # Charger automatiquement la page Profile
            self.load_profile()

        except Exception as e:
            print(f"❌ Erreur dans Dashboard : {e}")
            Notification(f"Erreur lors du chargement du Dashboard : {e}", style="danger").show()

    def load_profile(self):
        """Charge la page Profile dans le dashboard."""
        self.current_page = Profile(self.user)
        self.dashboard_panel.clear()
        self.dashboard_panel.add_component(self.current_page)
        self.update_navigation_style('profile_link')

    def load_add_product(self):
        """Charge la page Ajouter un Produit dans le dashboard."""
        self.current_page = AddProduct()
        self.dashboard_panel.clear()
        self.dashboard_panel.add_component(self.current_page)
        self.update_navigation_style('cart_link_copy')

    def load_list_clients(self):
        """Charge la page Liste des Clients dans le dashboard."""
        self.current_page = ListClients()
        self.dashboard_panel.clear()
        self.dashboard_panel.add_component(self.current_page)
        self.update_navigation_style('orders_link_copy')

    def load_list_products(self):
        """Charge la page Liste des Produits dans le dashboard."""
        self.current_page = ListProducts()
        self.dashboard_panel.clear()
        self.dashboard_panel.add_component(self.current_page)
        self.update_navigation_style('link_1')

    def update_navigation_style(self, active_link_name):
        """Met à jour le style des liens de navigation."""
        for link in [self.profile_link, self.cart_link_copy, self.orders_link_copy, self.link_1]:
            if getattr(link, 'name', None) == active_link_name:
                link.role = 'selected'
                link.background = '#c19e6b'
            else:
                link.role = None
                link.background = '#d4b483'

    def profile_link_click(self, **event_args):
        """Gère le clic sur le lien Profile."""
        self.load_profile()

    def cart_link_click(self, **event_args):
        """Gère le clic sur le lien Ajouter un Produit."""
        self.load_add_product()

    def orders_link_click(self, **event_args):
        """Gère le clic sur le lien Liste des Clients."""
        self.load_list_clients()

    def link_1_click(self, **event_args):
        """Gère le clic sur le lien Liste des Produits."""
        self.load_list_products()

    def menu_button_click(self, **event_args):
        """Gère le clic sur le bouton Retour au Menu."""
        get_open_form().load_page('menu')

  

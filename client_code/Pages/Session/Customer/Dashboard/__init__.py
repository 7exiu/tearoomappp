from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state
from ..Profile import Profile
from ..Cart import Cart
from ..Orders import Orders
from ..Bookings import Bookings

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.current_page = None
    self.user_info = anvil.server.call('get_user_info')
    self.user = anvil.server.call('get_user_by_email', self.user_info['user_email'])
    
    # Vérifier si l'utilisateur est admin
    if self.user and self.user['is_admin']:
      self.admin_button.visible = True
    
    # Charger automatiquement la page Profile
    self.load_profile()

  def load_profile(self):
    """Charge la page Profile dans le dashboard."""
    self.current_page = Profile(user=self.user)
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('profile_link')

  def load_cart(self):
    """Charge la page Cart dans le dashboard."""
    self.current_page = Cart()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('cart_link_copy')

  def load_orders(self):
    """Charge la page Orders dans le dashboard."""
    self.current_page = Orders()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('orders_link_copy')

  def load_bookings(self):
    """Charge la page Bookings dans le dashboard."""
    self.current_page = Bookings()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('link_1')

  def update_navigation_style(self, active_link_name):
    """Met à jour le style des liens de navigation."""
    for link in [self.profile_link, self.cart_link_copy, self.orders_link_copy, self.link_1]:
      if link.name == active_link_name:
        link.role = 'selected'
        link.background = '#c19e6b'  # Couleur plus foncée pour le lien actif
      else:
        link.role = None
        link.background = '#d4b483'  # Couleur normale pour les liens inactifs

  def profile_link_click(self, **event_args):
    """Gère le clic sur le lien Profile."""
    self.load_profile()

  def cart_link_click(self, **event_args):
    """Gère le clic sur le lien Cart."""
    self.load_cart()

  def orders_link_click(self, **event_args):
    """Gère le clic sur le lien Orders."""
    self.load_orders()

  def link_1_click(self, **event_args):
    """Gère le clic sur le lien Bookings."""
    self.load_bookings()

  def menu_button_click(self, **event_args):
    """Gère le clic sur le bouton Retour au Menu."""
    get_open_form().load_page('menu')

  def link_2_click(self, **event_args):
    """Gère le clic sur le lien Menu."""
    get_open_form().load_page('menu')

  def admin_button_click(self, **event_args):
    """Gère le clic sur le bouton Administration."""
    get_open_form().load_page('dashboard_admin')

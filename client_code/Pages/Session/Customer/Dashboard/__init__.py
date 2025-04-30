from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
from ..Profile import Profile
from ..Cart import Cart
from ..Orders import Orders
from ..Bookings import Bookings
from ...Admin.Dashboard_admin import Dashboard_admin

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    print("🛠 Initialisation du Dashboard...")
    self.init_components(**properties)

    try:
      print("📡 Connexion au serveur pour récupérer les informations utilisateur...")
      self.user_info = anvil.server.call('get_user_info')
      print(f"✅ Infos utilisateur récupérées : {self.user_info}")

      if not self.user_info.get("user_email"):
        raise ValueError("Aucun email utilisateur récupéré.")

      print("🔎 Recherche de l'utilisateur dans la base de données...")
      self.user = anvil.server.call('get_user_by_email', self.user_info["user_email"])

      if not self.user:
        raise ValueError("Utilisateur introuvable dans la base de données.")

      print(f"🎯 Utilisateur trouvé : {self.user['email']}")

      # Contrôle de l'affichage du bouton Admin (link_3)
      if self.user['is_admin'] is True:
        self.link_3.visible = True
        print("👑 Utilisateur est Admin. Bouton Admin visible.")
      else:
        self.link_3.visible = False
        print("👤 Utilisateur classique. Bouton Admin caché.")

      # Nettoyer l'ancien contenu du dashboard_panel
      print("🧹 Nettoyage du dashboard_panel...")
      self.dashboard_panel.clear()

      # Charger le formulaire Profile en passant l'utilisateur
      print("➕ Ajout du formulaire Profile au dashboard_panel...")
      profile_form = Profile(self.user)
      self.dashboard_panel.add_component(profile_form)

      print("✅ Formulaire Profile affiché avec succès dans le Dashboard.")

    except Exception as e:
      print(f"❌ Erreur dans Dashboard : {e}")
      Notification(f"Erreur lors du chargement du Dashboard : {e}", style="danger").show()
      get_open_form().load_page("main")  # Retour à la page principale si erreur

  def link_1_click(self, **event_args):
    """Lien vers les Bookings"""
    bookings = Bookings()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(bookings)

  def cart_link_click(self, **event_args):
    """Lien vers le Cart"""
    self.dashboard_panel.clear()
    cart_form = Cart()
    self.dashboard_panel.add_component(cart_form)

  def orders_link_click(self, **event_args):
    """Lien vers les Orders"""
    self.dashboard_panel.clear()
    orders_form = Orders()
    self.dashboard_panel.add_component(orders_form)

  def profile_link_click(self, **event_args):
    """Lien vers le Profile"""
    self.dashboard_panel.clear()
    profile_form = Profile(self.user)
    self.dashboard_panel.add_component(profile_form)

  def link_2_click(self, **event_args):
    """Lien de déconnexion"""
    get_open_form().load_page("landing")

  def link_3_click(self, **event_args):
    """Lien vers Dashboard Admin (réservé aux admins)"""
    if self.user['is_admin'] is True:
      print("🔐 Accès au Dashboard Admin autorisé.")
      self.dashboard_panel.clear()
      admin_form = Dashboard_admin()
      self.dashboard_panel.add_component(admin_form)
    else:
      print("🚫 Accès interdit : utilisateur non admin.")
      Notification("Accès réservé aux administrateurs.", style="danger").show()

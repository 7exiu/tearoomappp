from ._anvil_designer import LogInFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state

class LogInForm(LogInFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.update_button_visibility()
    # Ajoute le handler sur le bouton de connexion
    self.form_buttons.submit_button.add_event_handler('click', self.on_submit_click)

  def update_button_visibility(self):
    """Met à jour la visibilité des boutons en fonction de l'état de connexion."""
    user_info = anvil.server.call('get_user_info')
    if user_info:
      # Utilisateur connecté
      self.form_buttons.login_button.visible = False
      self.form_buttons.dashboard_button.visible = True
    else:
      # Utilisateur non connecté
      self.form_buttons.login_button.visible = True
      self.form_buttons.dashboard_button.visible = False

  def on_submit_click(self, **event_args):
    email = self.credentials_fields.email_field.text
    password = self.credentials_fields.password_field.text
    if not email or not password:
      Notification("Tous les champs doivent être remplis", style="danger").show()
      return
    # Appel serveur pour authentification
    server_response = anvil.server.call('login_user', email, password)
    if "Invalid" in server_response:
      Notification("Email ou mot de passe incorrect", style="danger").show()
      return
    Notification(server_response, style="success").show()
    self.update_button_visibility()
    get_open_form().load_page('dashboard')

  def dashboard_button_click(self, **event_args):
    """Redirige vers le dashboard."""
    get_open_form().load_page('dashboard')

  def form_hide(self, **event_args):
    pass

  def on_state_change(self):
    pass

  def sign_up_link_click(self, **event_args):
    get_open_form().load_page("signup")

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
    """Gère la soumission du formulaire de connexion."""
    # Vérifier si les champs sont vides
    if not self.credentials_fields.email_input.text or not self.credentials_fields.password_input.text:
      Notification("Veuillez remplir tous les champs", style="danger").show()
      return

    try:
      # Appeler la fonction serveur pour la connexion
      result = anvil.server.call('login_user', 
                                self.credentials_fields.email_input.text,
                                self.credentials_fields.password_input.text)
      
      if result == "Invalid Data":
        Notification("Email ou mot de passe incorrect", style="danger").show()
      else:
        Notification("Connexion réussie", style="success").show()
        self.update_button_visibility()
        get_open_form().load_page('dashboard')
    except Exception as e:
      Notification(f"Erreur lors de la connexion : {str(e)}", style="danger").show()

  def dashboard_button_click(self, **event_args):
    """Redirige vers le dashboard."""
    get_open_form().load_page('dashboard')

  def form_hide(self, **event_args):
    pass

  def on_state_change(self):
    pass

  def sign_up_link_click(self, **event_args):
    get_open_form().load_page("signup")

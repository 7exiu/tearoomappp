from ._anvil_designer import LogInFormTemplate
from anvil import *
import anvil.server

class LogInForm(LogInFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Ajoute le handler sur le bouton de connexion
    self.form_buttons.submit_button.add_event_handler('click', self.on_submit_click)
    # Configuration du bouton de connexion
    self.form_buttons.submit_button.text = "Se connecter"
    self.form_buttons.submit_button.role = "filled-button"

  def on_submit_click(self, **event_args):
    """Gestion de la connexion"""
    try:
        email = self.credentials_fields.email_field.text
        password = self.credentials_fields.password_field.text
        
        # Validation des champs
        if not email or not password:
            Notification("Tous les champs doivent être remplis", style="danger").show()
            return
            
        # Appel serveur pour authentification
        server_response = anvil.server.call('login_user', email, password)
        
        if "Invalid" in server_response:
            Notification("Email ou mot de passe incorrect", style="danger").show()
            # Effacer le mot de passe en cas d'erreur
            self.credentials_fields.password_field.text = ""
            return
            
        # Connexion réussie
        Notification(server_response, style="success").show()
        get_open_form().load_page('dashboard')
        
    except Exception as e:
        Notification(f"Erreur lors de la connexion : {str(e)}", style="danger").show()

  def dashboard_button_click(self, **event_args):
    get_open_form().load_page('dashboard')

  def form_hide(self, **event_args):
    pass

  def on_state_change(self):
    pass

  def sign_up_link_click(self, **event_args):
    """Redirection vers la page d'inscription"""
    get_open_form().load_page("signup")

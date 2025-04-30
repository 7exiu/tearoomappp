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
    #state.register(self.on_state_change)
    #self.on_state_change()
    self.form_buttons.submit_button.add_event_handler('click', self.on_submit_click)
    
  def on_submit_click(self, **event_args):
    print("✅---------------------------------------")
    email = self.credentials_fields.email_field.text
    password = self.credentials_fields.password_field.text
    if not email or not password:
      Notification("All Fields must be filled", style="danger").show()
      return
    server_response = anvil.server.call('login_user', email, password) 
    Notification(server_response, style="success").show()
    get_open_form().load_page('dashboard')



  def form_hide(self, **event_args):
    #state.unregister(self.on_state_change)  
    pass
  def on_state_change(self):
    #print(f"Utilisateur actuel : {state.get('user')}")
    pass

  def sign_up_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().load_page("signup")
    pass

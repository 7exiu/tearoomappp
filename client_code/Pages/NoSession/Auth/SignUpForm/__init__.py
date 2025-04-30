from ._anvil_designer import SignUpFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import math
import string
import time



class SignUpForm(SignUpFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.sign_up_form_buttons.submit_button.add_event_handler('click', self.on_submit_click)
    self.file_loader_1.file_types = ['.jpg', '.png']
    self.credentials_fields.password_field.add_event_handler('change', self.on_password_change)
      
  def on_password_change(self, **event_args):
    password = self.credentials_fields.password_field.text
    if password:
      entropie, taille_alphabet, redon = anvil.server.call('calculer_entropie', password)
      securite = anvil.server.call('evaluer_securite', entropie)
      
      # Mise à jour de l'indicateur visuel
      if securite == "Invalide":
        self.password_strength.text = "Le mot de passe doit contenir au moins 12 caractères, incluant majuscules, minuscules, chiffres et caractères spéciaux"
        self.password_strength.foreground = "#BA1A1A"  # Rouge pour erreur
      else:
        self.password_strength.text = f"Force du mot de passe : {securite}"
        if securite in ["Très faible", "Faible"]:
          self.password_strength.foreground = "#BA1A1A"  # Rouge
        elif securite == "Moyenne":
          self.password_strength.foreground = "#695E2F"  # Orange
        else:
          self.password_strength.foreground = "#006C48"  # Vert
    else:
      self.password_strength.text = ""
      
  def on_submit_click(self, **event_args):
    photo = self.file_loader_1.file
    firstname = self.name_fields.firstname_field.text 
    lastname = self.name_fields.lastname_field.text
    email = self.credentials_fields.email_field.text
    password = self.credentials_fields.password_field.text
    confirmed_password = self.confirmed_password_field.text

    if not firstname or not lastname or not email or not password or not confirmed_password:
        Notification("Tous les champs doivent être remplis", style="danger").show()
        return

    if password != confirmed_password:
        Notification("Les mots de passe ne correspondent pas", style="danger").show()
        return  

    entropie, taille_alphabet, redon = anvil.server.call('calculer_entropie', password)
    securite = anvil.server.call('evaluer_securite', entropie)
    
    if securite == "Invalide":
      Notification("Le mot de passe doit contenir au moins 12 caractères, incluant majuscules, minuscules, chiffres et caractères spéciaux", style="danger").show()
      return
    if securite in ["Très faible", "Faible", "Moyenne"]:
      Notification(f"Le mot de passe est trop faible : {securite}", style="danger").show()
      return

    try:
        photo = anvil.server.call("add_metadata", photo, email)
        response = anvil.server.call('add_user', firstname, lastname, email, password, photo)
        Notification(response, style="success").show()

        self.name_fields.firstname_field.text = ""
        self.name_fields.lastname_field.text = ""
        self.credentials_fields.email_field.text = ""
        self.credentials_fields.password_field.text = ""
        self.confirmed_password_field.text = ""
        self.password_strength.text = ""

        get_open_form().load_page("login")

    except Exception as e:
        Notification(f"Erreur lors de la communication avec le serveur : {e}", style="danger").show()

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass

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
    # Configuration des composants
    self.setup_components()
    # Initialisation des gestionnaires d'événements
    self.setup_event_handlers()

  def setup_components(self):
    """Configure les composants du formulaire"""
    # Configuration du chargeur de photo
    self.photo_loader.file_types = ['.jpg', '.png']
    
    # Configuration des boutons
    self.sign_up_form_buttons.submit_button.text = "S'inscrire"
    self.sign_up_form_buttons.submit_button.role = "filled-button"
    self.sign_up_form_buttons.reset_button.text = "Annuler"
    
    # Initialisation du label de force du mot de passe
    self.password_strength.text = ""
    self.password_strength.foreground = "#000000"

  def setup_event_handlers(self):
    """Configure les gestionnaires d'événements"""
    self.credentials_fields.password_field.add_event_handler('change', self.on_password_change)
    self.sign_up_form_buttons.submit_button.add_event_handler('click', self.submit_click)
    self.sign_up_form_buttons.reset_button.add_event_handler('click', self.cancel_click)

  def on_password_change(self, **event_args):
    """Gère le changement de mot de passe et met à jour l'indicateur de force"""
    password = self.credentials_fields.password_field.text
    if password:
      entropie, taille_alphabet, redon = anvil.server.call('calculer_entropie', password)
      securite = anvil.server.call('evaluer_securite', entropie)
      
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
      
  def submit_click(self, **event_args):
    """Gère la soumission du formulaire d'inscription"""
    try:
        # Récupération des valeurs des champs
        photo = self.photo_loader.file
        firstname = self.name_fields.firstname_field.text 
        lastname = self.name_fields.lastname_field.text
        email = self.credentials_fields.email_field.text
        password = self.credentials_fields.password_field.text
        confirmed_password = self.confirmed_password_field.text

        # Validation des champs requis
        if not firstname or not lastname or not email or not password or not confirmed_password:
            Notification("Tous les champs doivent être remplis", style="danger").show()
            return

        # Validation de la correspondance des mots de passe
        if password != confirmed_password:
            Notification("Les mots de passe ne correspondent pas", style="danger").show()
            return  

        # Validation de la force du mot de passe
        entropie, taille_alphabet, redon = anvil.server.call('calculer_entropie', password)
        securite = anvil.server.call('evaluer_securite', entropie)
        
        if securite == "Invalide":
            Notification("Le mot de passe doit contenir au moins 12 caractères, incluant majuscules, minuscules, chiffres et caractères spéciaux", style="danger").show()
            return
        if securite in ["Très faible", "Faible", "Moyenne"]:
            Notification(f"Le mot de passe est trop faible : {securite}", style="danger").show()
            return

        # Ajout des métadonnées à la photo si elle existe
        if photo:
            photo = anvil.server.call("add_metadata", photo, email)

        # Création de l'utilisateur
        response = anvil.server.call('add_user', firstname, lastname, email, password, photo)
        
        if response == "success":
            Notification("Inscription réussie ! Vous pouvez maintenant vous connecter.", style="success").show()
            # Redirection vers la page de connexion
            get_open_form().load_page("login")
        else:
            Notification(f"{response}", style="success").show()

    except Exception as e:
        Notification(f"Erreur lors de l'inscription : {str(e)}", style="danger").show()

  def cancel_click(self, **event_args):
    """Redirige vers la page de connexion lors de l'annulation"""
    get_open_form().load_page("login")

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass

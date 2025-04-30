from ._anvil_designer import ProfileTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables

class Profile(ProfileTemplate):
    def __init__(self, user, **properties):
        self.init_components(**properties)
<<<<<<< HEAD

        self.user = user  # Reçoit l'objet Row depuis Dashboard

        try:
            self.setup_ui()
            print("✅ UI Profile chargée avec succès.")
        except Exception as e:
            print(f"❌ Erreur dans Profile __init__ : {e}")
            Notification(f"Erreur lors de l'initialisation du Profil : {e}", style="danger").show()
=======
        self.user = user  # Reçoit l'objet Row depuis Dashboard
        self.setup_ui()
>>>>>>> 98edb84 (ton message de commit ici444454)

    def setup_ui(self):
        """Affiche les infos utilisateur dans les labels"""
        try:
<<<<<<< HEAD
            print(">>> Chargement des infos utilisateur dans Profile...")
            
            # Affichage prénom et nom
            self.profile_name.text = f"{self.user['firstname']} {self.user['lastname']}"
            self.profile_email.text = self.user['email']
            self.profile_photo.source = self.user['photo']

            # Vérification et masquage du mot de passe
            password = len(self.user['password'])  # Utilisation de get pour éviter les erreurs
            password_length = password
            self.profile_password.text = "*" * password_length if password else "Pas de mot de passe défini"
=======
            self.profile_name.text = f"{self.user['firstname']} {self.user['lastname']}"
            self.profile_email.text = self.user['email']
            self.profile_photo.source = self.user['photo']
            password = len(self.user['password'])
            self.profile_password.text = "*" * password if password else "Pas de mot de passe défini"
            
            # Style des composants
            self.profile_name.role = 'title'
            self.profile_email.role = 'subtitle'
            self.profile_password.role = 'subtitle'
            self.profile_photo.role = 'avatar'
>>>>>>> 98edb84 (ton message de commit ici444454)

            print("✅ Données utilisateur affichées correctement dans Profile.")
        except Exception as e:
            print(f"❌ Erreur dans setup_ui Profile : {e}")
            Notification(f"Erreur d'affichage du profil : {e}", style="warning").show()

    def form_show(self, **event_args):
      """This method is called when the form is shown on the page"""
      pass

from ._anvil_designer import ProfileTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables

class Profile(ProfileTemplate):
    def __init__(self, user, **properties):
        self.init_components(**properties)
        self.user = user  # Reçoit l'objet Row depuis Dashboard
        
        if self.user is None:
            Notification("Erreur : Aucun utilisateur connecté", style="danger").show()
            return
            
        try:
            self.setup_ui()
            print("✅ UI Profile chargée avec succès.")
        except Exception as e:
            print(f"❌ Erreur dans Profile __init__ : {e}")
            Notification(f"Erreur lors de l'initialisation du Profil : {e}", style="danger").show()

    def setup_ui(self):
        """Affiche les infos utilisateur dans les labels"""
        try:
            print(">>> Chargement des infos utilisateur dans Profile...")
            
            # Affichage prénom et nom
            self.profile_name.text = f"{self.user['firstname']} {self.user['lastname']}"
            self.profile_email.text = self.user['email']
            self.profile_photo.source = self.user['photo']

            # Vérification et masquage du mot de passe
            password_length = len(self.user['password'])
            self.profile_password.text = "*" * password_length if password_length else "Pas de mot de passe défini"
            
            # Style des composants
            self.profile_name.role = 'title'
            self.profile_email.role = 'subtitle'
            self.profile_password.role = 'subtitle'
            self.profile_photo.role = 'avatar'

            print("✅ Données utilisateur affichées correctement dans Profile.")
        except Exception as e:
            print(f"❌ Erreur dans setup_ui Profile : {e}")
            Notification(f"Erreur d'affichage du profil : {e}", style="warning").show()

    def form_show(self, **event_args):
        """Cette méthode est appelée quand le formulaire est affiché"""
        pass

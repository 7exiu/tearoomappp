from ._anvil_designer import ProfileTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Profile(ProfileTemplate):
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user
        if self.user is None:
            # Redirection vers la page de connexion si pas d'utilisateur
            open_form('LogInForm')
            return
        self.display_user_info()

    def display_user_info(self):
        """Affiche les informations de l'utilisateur"""
        try:
            # Affichage de la photo de profil avec gestion d'erreur
            try:
                if self.user['photo']:
                    self.profile_photo.source = self.user['photo']
                else:
                    self.profile_photo.source = "https://ui-avatars.com/api/?name=" + self.user['firstname'] + "+" + self.user['lastname']
            except:
                # En cas d'erreur avec la photo, utiliser une image par défaut
                self.profile_photo.source = "/_/theme/default_avatar.png"
            
            # Affichage du nom et email avec validation
            self.user_name.text = f"{self.user.get('firstname', '')} {self.user.get('lastname', '')}"
            self.user_email.text = self.user.get('email', '')
            
            # Remplissage des champs d'édition avec validation
            self.firstname_input.text = self.user.get('firstname', '')
            self.lastname_input.text = self.user.get('lastname', '')
            self.email_input.text = self.user.get('email', '')
        except Exception as e:
            alert("Erreur lors de l'affichage du profil")

    def edit_button_click(self, **event_args):
        """Active l'édition du profil"""
        self.enable_editing(True)

    def enable_editing(self, enabled):
        """Active ou désactive l'édition des champs"""
        self.firstname_input.enabled = enabled
        self.lastname_input.enabled = enabled
        self.email_input.enabled = enabled
        
        self.edit_button.visible = not enabled
        self.save_button.visible = enabled
        self.cancel_button.visible = enabled

    def save_button_click(self, **event_args):
        """Sauvegarde les modifications du profil"""
        try:
            # Validation des champs
            if not all([self.firstname_input.text, self.lastname_input.text, self.email_input.text]):
                alert("Tous les champs doivent être remplis")
                return

            # Validation du format email
            if not '@' in self.email_input.text or not '.' in self.email_input.text:
                alert("Format d'email invalide")
                return

            # Appel au serveur pour mettre à jour le profil
            result = anvil.server.call(
                'update_user_profile',
                self.user['email'],
                self.firstname_input.text.strip(),
                self.lastname_input.text.strip(),
                self.email_input.text.strip()
            )

            if result:
                # Mise à jour des informations affichées
                self.user['firstname'] = self.firstname_input.text.strip()
                self.user['lastname'] = self.lastname_input.text.strip()
                self.user['email'] = self.email_input.text.strip()
                self.display_user_info()
                Notification("Profil mis à jour avec succès").show()
            else:
                alert("Erreur lors de la mise à jour du profil")

        except Exception as e:
            alert(f"Erreur : {str(e)}")

        finally:
            self.enable_editing(False)

    def cancel_button_click(self, **event_args):
        """Annule les modifications du profil"""
        self.display_user_info()  # Restaure les valeurs originales
        self.enable_editing(False)

    def form_show(self, **event_args):
        """Cette méthode est appelée quand le formulaire est affiché"""
        if not self.user:
            open_form('LogInForm')

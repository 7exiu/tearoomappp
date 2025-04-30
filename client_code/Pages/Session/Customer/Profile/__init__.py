from ._anvil_designer import ProfileTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Profile(ProfileTemplate):
    def __init__(self, user=None, **properties):
        print("🔄 Initialisation du profil...")
        self.init_components(**properties)

        if user is None:
            print("📡 Aucun utilisateur fourni, tentative de récupération depuis le serveur...")
            try:
                user_info = anvil.server.call('get_user_info')
                print(f"📋 Informations utilisateur reçues : {user_info}")
                
                if not user_info:
                    print("❌ Aucune information utilisateur reçue")
                    open_form('LogInForm')
                    return
                    
                if not user_info.get('user_email'):
                    print("❌ Pas d'email utilisateur trouvé dans les informations")
                    open_form('LogInForm')
                    return
                    
                print(f"📧 Email utilisateur trouvé : {user_info['user_email']}")
                self.user = anvil.server.call('get_user_by_email', user_info['user_email'])
                print(f"✅ Utilisateur récupéré : {self.user}")
                
                if not self.user:
                    print("❌ Utilisateur non trouvé dans la base de données")
                    open_form('LogInForm')
                    return
                    
            except Exception as e:
                print(f"❌ Erreur lors de la récupération de l'utilisateur : {e}")
                open_form('LogInForm')
                return
        else:
            print(f"✅ Utilisateur fourni : {user}")
            self.user = user
            
        self.display_user_info()

    def display_user_info(self):
        """Affiche les informations de l'utilisateur"""
        try:
            print("🔄 Affichage des informations utilisateur...")
            print(f"📋 Données utilisateur disponibles : {self.user}")
            
            if not self.user:
                print("❌ Aucun utilisateur disponible pour l'affichage")
                return
                
            # Affichage de la photo de profil avec gestion d'erreur
            try:
                if self.user['photo']:
                    print("🖼️ Utilisation de la photo de profil fournie")
                    self.profile_photo.source = self.user['photo']
                else:
                    print("🖼️ Génération d'un avatar par défaut")
                    firstname = self.user['firstname']
                    lastname = self.user['lastname']
                    self.profile_photo.source = f"https://ui-avatars.com/api/?name={firstname}+{lastname}"
            except Exception as photo_error:
                print(f"⚠️ Erreur avec la photo : {photo_error}")
                self.profile_photo.source = "/_/theme/default_avatar.png"
            
            # Affichage du nom et email avec validation
            firstname = self.user['firstname']
            lastname = self.user['lastname']
            print(f"👤 Nom complet : {firstname} {lastname}")
            self.user_name.text = f"{firstname} {lastname}"
            
            email = self.user['email']
            print(f"📧 Email : {email}")
            self.user_email.text = email
            
            # Remplissage des champs d'édition avec validation
            self.firstname_input.text = firstname
            self.lastname_input.text = lastname
            self.email_input.text = email
            
            print("✅ Informations affichées avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'affichage du profil : {e}")
            alert(f"Erreur lors de l'affichage du profil : {str(e)}")

    def edit_button_click(self, **event_args):
        """Active l'édition du profil"""
        print("🖊️ Activation du mode édition")
        self.enable_editing(True)

    def enable_editing(self, enabled):
        """Active ou désactive l'édition des champs"""
        print(f"🔄 {'Activation' if enabled else 'Désactivation'} de l'édition")
        self.firstname_input.enabled = enabled
        self.lastname_input.enabled = enabled
        self.email_input.enabled = enabled
        
        self.edit_button.visible = not enabled
        self.save_button.visible = enabled
        self.cancel_button.visible = enabled

    def save_button_click(self, **event_args):
        """Sauvegarde les modifications du profil"""
        try:
            print("💾 Tentative de sauvegarde du profil...")
            
            # Validation des champs
            if not all([self.firstname_input.text, self.lastname_input.text, self.email_input.text]):
                print("❌ Champs manquants")
                alert("Tous les champs doivent être remplis")
                return

            # Validation du format email
            if not '@' in self.email_input.text or not '.' in self.email_input.text:
                print("❌ Format d'email invalide")
                alert("Format d'email invalide")
                return

            print("📡 Envoi des modifications au serveur...")
            # Appel au serveur pour mettre à jour le profil
            result = anvil.server.call(
                'update_user_profile',
                self.user['email'],
                self.firstname_input.text.strip(),
                self.lastname_input.text.strip(),
                self.email_input.text.strip()
            )

            if result:
                print("✅ Profil mis à jour avec succès")
                # Mise à jour des informations affichées
                self.user['firstname'] = self.firstname_input.text.strip()
                self.user['lastname'] = self.lastname_input.text.strip()
                self.user['email'] = self.email_input.text.strip()
                self.display_user_info()
                Notification("Profil mis à jour avec succès").show()
            else:
                print("❌ Erreur lors de la mise à jour")
                alert("Erreur lors de la mise à jour du profil")

        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")
            alert(f"Erreur : {str(e)}")

        finally:
            self.enable_editing(False)

    def cancel_button_click(self, **event_args):
        """Annule les modifications du profil"""
        print("🔄 Annulation des modifications")
        self.display_user_info()  # Restaure les valeurs originales
        self.enable_editing(False)

    def form_show(self, **event_args):
        """Cette méthode est appelée quand le formulaire est affiché"""
        print("📋 Affichage du formulaire profil")
        if not self.user:
            print("❌ Aucun utilisateur trouvé, redirection vers la connexion")
            open_form('LogInForm')

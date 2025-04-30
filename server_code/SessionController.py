import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

@anvil.server.callable
def login_user(email, password):
    """Authentifie un utilisateur avec son email et son mot de passe"""
    try:
        # Récupération de l'utilisateur
        user = app_tables.users.get(email=email)
        if user is None:
            return "Invalid Data"

        # Vérification du mot de passe
        ph = PasswordHasher()
        try:
            # Le premier argument doit être le hash stocké, le second le mot de passe fourni
            is_password_valid = ph.verify(user['password'], password)
            if is_password_valid:
                set_user_info(user['email'], user.get_id())
                return f"Welcome back {user['firstname']} {user['lastname']}"
        except VerifyMismatchError:
            return "Invalid Data"
        except Exception as e:
            print(f"Erreur lors de la vérification du mot de passe : {str(e)}")
            return "Invalid Data"

    except Exception as e:
        print(f"Erreur lors de la connexion : {str(e)}")
        return "Invalid Data"

@anvil.server.callable
def logout_user():
    """Déconnecte l'utilisateur en supprimant ses informations de session"""
    try:
        # Supprimer individuellement les clés de session
        if 'user_email' in anvil.server.session:
            del anvil.server.session['user_email']
        if 'user_id' in anvil.server.session:
            del anvil.server.session['user_id']
        return True
    except Exception as e:
        print(f"Erreur lors de la déconnexion : {str(e)}")
        return False
  
@anvil.server.callable
def set_user_info(email, id):
    """Enregistre les informations de l'utilisateur en session"""
    try:
        anvil.server.session['user_email'] = email
        anvil.server.session['user_id'] = id
        print(f"✅ SESSION ITEMS INITIALIZED: {anvil.server.session}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la session : {str(e)}")
        return False

@anvil.server.callable  
def get_all_users():
    """Récupère la liste de tous les utilisateurs"""
    try:
        print("📋 Récupération de tous les utilisateurs...")
        return list(app_tables.users.search())
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {str(e)}")
        return []

@anvil.server.callable
def get_user_info():
    """Récupère les informations de l'utilisateur connecté"""
    try:
        return {
            "user_email": anvil.server.session.get('user_email'),
            "user_id": anvil.server.session.get('user_id')
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des informations utilisateur : {str(e)}")
        return None

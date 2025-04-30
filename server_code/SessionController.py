import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from argon2 import PasswordHasher

@anvil.server.callable
def login_user(email, password):
    user = app_tables.users.get(email=email)
    ph = PasswordHasher()
    if user is None:
        return "Invalid Data"

    is_password_valid = ph.verify(user['password'], password)
    if not is_password_valid:
        return "Invalid Data"

    set_user_info(user['email'], user.get_id())
    return f"Welcome back {user['firstname']} {user['lastname']}"


@anvil.server.callable
def logout_user():
  print(f"SESSION ITEMS: {anvil.server.session}")
  anvil.server.session.clear()
  print(f"SESSION ITEMS: {anvil.server.session}")
  
@anvil.server.callable
def set_user_info(email, id):
    anvil.server.session['user_email'] = email
    anvil.server.session['user_id'] = id
    print(f"✅ SESSION ITEMS INITIALIZED: {anvil.server.session})")

@anvil.server.callable  
def get_all_users():
  print("📋 Récupération de tous les utilisateurs...")
  return list(app_tables.users.search())

@anvil.server.callable
def get_user_info():
    return {"user_email":anvil.server.session.get('user_email'), "user_id":anvil.server.session.get('user_id')}

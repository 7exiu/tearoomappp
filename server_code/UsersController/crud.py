import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime 
from argon2 import PasswordHasher
# This is a server package. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_user_by_email(email):
  return app_tables.users.get(email=email)

@anvil.server.callable
def get_user_by_id(id):
  return app_tables.users.get_by_id(id)

@anvil.server.callable
def add_user(firstname, lastname, email, password , photo):
  ph = PasswordHasher()
  now = datetime.now()
  reponse = anvil.server.call('add_metadata', photo , email)
  app_tables.users.add_row(
    firstname=firstname,
    lastname=lastname,
    email=email,
    password = ph.hash(password),
    created_at=now,
    updated_at=now,
    photo = reponse,
    is_admin=False
  )
  return "user added with success"
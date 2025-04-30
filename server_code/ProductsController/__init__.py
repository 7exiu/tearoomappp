import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# Import de la fonction pour la rendre disponible
<<<<<<< HEAD

=======
from .AddProductController.crud import add_product_to_catalog
>>>>>>> b107d4a (ton message de commit ici4444545755275465453454587548645465468476545487)

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

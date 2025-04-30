import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
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
def add_product(name, description, price, stock, photo=None, category=None):
    """
    Ajoute un nouveau produit dans la table `products`.
    
    Args:
      name (str): Nom du produit.
      description (str): Description du produit.
      price (float): Prix unitaire.
      stock (int): Quantité en stock.
      photo (Media object, optional): Photo du produit.
      category (str, optional): Catégorie du produit.
      
    Returns:
      str: Message de confirmation.
    """
    now = datetime.now()
    app_tables.products.add_row(
        name=name,
        description=description,
        price=price,
        stock=stock,
        photo=photo,
        category=category,
        created_at=now,
        updated_at=now
    )
    return "Product added successfully"

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def get_cart(user_id):
    """Récupère le panier d'un utilisateur"""
    return app_tables.carts.get(user_id=user_id)

@anvil.server.callable
def create_cart(user_id, items):
    """Crée un nouveau panier"""
    now = datetime.now()
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
    
    return app_tables.carts.add_row(
        user_id=user_id,
        content=items,
        created_at=now,
        updated_at=now,
        total_amount=total
    )

@anvil.server.callable
def update_cart(user_id, items):
    """Met à jour le panier existant"""
    cart = get_cart(user_id)
    if cart:
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
        cart.update(
            content=items,
            updated_at=datetime.now(),
            total_amount=total
        )
    return cart

@anvil.server.callable
def delete_cart(user_id):
    """Supprime le panier d'un utilisateur"""
    cart = get_cart(user_id)
    if cart:
        cart.delete()
    return True

@anvil.server.callable
def add_to_cart(user_id, item):
    """Ajoute un article au panier"""
    cart = get_cart(user_id)
    if not cart:
        return create_cart(user_id, [item])
        
    current_items = cart['content']
    # Vérifie si l'article existe déjà
    for existing_item in current_items:
        if existing_item['id'] == item['id']:
            existing_item['quantity'] = existing_item.get('quantity', 1) + 1
            return update_cart(user_id, current_items)
            
    # Si l'article n'existe pas, l'ajouter
    current_items.append(item)
    return update_cart(user_id, current_items)
  
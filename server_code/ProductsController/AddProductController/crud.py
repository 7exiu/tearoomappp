import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def add_product(name, description, price, image, category):
    """
    Ajoute un nouveau produit dans la table appropriée (teas ou goodies).
    
    Args:
        name (str): Nom du produit
        description (str): Description du produit
        price (float): Prix du produit
        image (Media): Image du produit
        category (str): Catégorie du produit ('tea' ou 'goodie')
        
    Returns:
        str: Message de confirmation
    """
    try:
        now = datetime.now()
        
        if category == 'tea':
            app_tables.teas.add_row(
                name=name,
                description=description,
                price=price,
                image=image,
                created_at=now,
                updated_at=now,
                is_available=True
            )
            return "Thé ajouté avec succès"
        elif category == 'goodie':
            app_tables.goodies.add_row(
                name=name,
                description=description,
                price=price,
                image=image,
                created_at=now,
                updated_at=now,
                is_available=True
            )
            return "Goodie ajouté avec succès"
        else:
            return "Catégorie invalide. Utilisez 'tea' ou 'goodie'"
            
    except Exception as e:
        print(f"Erreur lors de l'ajout du produit : {e}")
        return f"Erreur : {e}" 
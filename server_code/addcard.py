import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import traceback
from datetime import datetime


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


'''
@anvil.server.callable
def addcard(product_id):
    # Rechercher le produit par ID dans la base de données
    product = app_tables.teas.get_by_id(product_id)

    if product is not None:
        print("=== Produit trouvé ===")
        print(f"ID         : {product.get_id()}")
        print(f"Nom        : {product['name']}")
        print(f"Prix       : {product['price']} €")
        print(f"Description: {product['description']}")
        print(f"Image      : {product['image']}")
        return product
    else:
        print("⚠️ Produit introuvable avec l'ID :", product_id)
        return None


'''
@anvil.server.callable
def addcard(product_id):
    try:
        print("=== Début addcard ===")
        print(f"ID produit reçu : {product_id}")
        
        # Récupération des infos utilisateur
        try:
            user_data = anvil.server.call('get_user_info')
            user_id = user_data['user_id']
            print(f"ID utilisateur : {user_id}")
        except Exception as e:
            print("❌ Erreur lors de la récupération de l'utilisateur:")
            print(str(e))
            print(traceback.format_exc())
            return None

        # Recherche du produit
        try:
            article = app_tables.teas.get_by_id(product_id)
            print(f"Recherche du produit : {'Trouvé' if article else 'Non trouvé'}")
        except Exception as e:
            print("❌ Erreur lors de la recherche du produit:")
            print(str(e))
            print(traceback.format_exc())
            return None

        if article is not None:
            print("=== Détails du produit trouvé ===")
            print(f"Nom : {article['name']}")
            print(f"Prix : {article['price']} €")
            
            try:
                # Ajout dans la table temp
                print("Tentative d'ajout dans la table temp...")
                app_tables.temp.add_row(
                    name = article['name'],
                    etat = False,
                    price = article['price'],
                    image = article['image'], 
                    description = article['description'],
                    id_user = user_id
                )
                print("✅ Produit ajouté avec succès au panier")
                return product_id
            except Exception as e:
                print("❌ Erreur lors de l'ajout à la table temp:")
                print(str(e))
                print(traceback.format_exc())
                return None
        else:
            print(f"⚠️ Produit introuvable avec l'ID : {product_id}")
            return None
            
    except Exception as e:
        print("❌ Erreur générale dans addcard:")
        print(str(e))
        print(traceback.format_exc())
        return None

@anvil.server.callable
def addgoodie(product_id):
    try:
        print("=== Début addgoodie ===")
        print(f"ID produit reçu : {product_id}")
        
        # Récupération des infos utilisateur
        try:
            user_data = anvil.server.call('get_user_info')
            user_id = user_data['user_id']
            print(f"ID utilisateur : {user_id}")
        except Exception as e:
            print("❌ Erreur lors de la récupération de l'utilisateur:")
            print(str(e))
            print(traceback.format_exc())
            return None

        # Recherche du produit
        try:
            article = app_tables.goodies.get_by_id(product_id)
            print(f"Recherche du produit : {'Trouvé' if article else 'Non trouvé'}")
        except Exception as e:
            print("❌ Erreur lors de la recherche du produit:")
            print(str(e))
            print(traceback.format_exc())
            return None

        if article is not None:
            print("=== Détails du produit trouvé ===")
            print(f"Nom : {article['name']}")
            print(f"Prix : {article['price']} €")
            
            try:
                # Ajout dans la table temp
                print("Tentative d'ajout dans la table temp...")
                app_tables.temp.add_row(
                    name = article['name'],
                    price = article['price'],
                    etat = False,
                    image = article['image'], 
                    description = article['description'],
                    id_user = user_id,
                )
                print("✅ Goodie ajouté avec succès au panier")
                return product_id
            except Exception as e:
                print("❌ Erreur lors de l'ajout à la table temp:")
                print(str(e))
                print(traceback.format_exc())
                return None
        else:
            print(f"⚠️ Produit introuvable avec l'ID : {product_id}")
            return None
            
    except Exception as e:
        print("❌ Erreur générale dans addgoodie:")
        print(str(e))
        print(traceback.format_exc())
        return None

@anvil.server.callable
def get_card():
    try:
        print("=== Récupération de tous les articles du panier ===")
        articles = list(app_tables.temp.search())
        print(f"Nombre d'articles trouvés : {len(articles)}")
        return articles
    except Exception as e:
        print("❌ Erreur dans get_card:")
        print(str(e))
        print(traceback.format_exc())
        return []

@anvil.server.callable
def panier():
    try:
        print("=== Récupération du panier utilisateur ===")
        user_data = anvil.server.call('get_user_info')
        user_id = user_data['user_id']
        print(f"ID utilisateur : {user_id}")
        
        articles = list(app_tables.temp.search(id_user=user_id, etat=False))
        print(f"Nombre d'articles dans le panier : {len(articles)}")
        return articles
    except Exception as e:
        print("❌ Erreur dans panier:")
        print(str(e))
        print(traceback.format_exc())
        return []

@anvil.server.callable
def delete_card():
    user_data = anvil.server.call('get_user_info')
    user_id = user_data['user_id']
    produits_a_modifier = app_tables.temp.search(id_user=user_id, etat=False)
    for produit in produits_a_modifier:
        produit['etat'] = True
    print("parfait")
    return

@anvil.server.callable
def check_orders_table():
    """Vérifie si la table orders existe et a la bonne structure"""
    try:
        # Vérifier si la table existe en essayant de la lire
        test = app_tables.orders.search()
        print("✅ Table orders trouvée")
        return True
    except Exception as e:
        print("❌ Erreur avec la table orders:")
        print(str(e))
        return False

@anvil.server.callable
def validate_order():
    try:
        print("=== Validation de la commande ===")
        
        # Vérifier la table orders
        if not check_orders_table():
            print("❌ La table orders n'est pas correctement configurée")
            return False
            
        user_data = anvil.server.call('get_user_info')
        user_id = user_data['user_id']
        print(f"ID utilisateur : {user_id}")
        
        # Récupérer tous les articles du panier
        cart_items = list(app_tables.temp.search(id_user=user_id, etat=False))
        print(f"Nombre d'articles dans le panier : {len(cart_items)}")
        
        if not cart_items:
            print("❌ Panier vide")
            return False
            
        try:
            # Préparer les données pour la commande
            order_content = []
            total = 0
            
            for item in cart_items:
                order_content.append({
                    'name': item['name'],
                    'price': item['price'],
                    'description': item['description'],
                    'image': item['image']
                })
                total += item['price']
            
            print("Contenu de la commande préparé :")
            print(order_content)
            print(f"Total calculé : {total}")
            
            # Créer la commande dans la table orders
            try:
                new_order = app_tables.orders.add_row(
                    user_id=user_id,
                    date=datetime.now(),
                    status="En cours",
                    content=order_content,
                    total_amount=total
                )
                print("✅ Commande créée avec succès")
                print(f"ID de la commande : {new_order.get_id()}")
            except Exception as e:
                print("❌ Erreur lors de l'ajout à la table orders:")
                print(str(e))
                print("Structure de la commande tentée:")
                print({
                    'user_id': user_id,
                    'date': datetime.now(),
                    'status': "En cours",
                    'content': order_content,
                    'total_amount': total
                })
                return False
            
            # Marquer les articles du panier comme commandés
            try:
                for item in cart_items:
                    print(f"Marquage de l'article {item['name']} comme commandé")
                    item['etat'] = True
                print("✅ Articles du panier marqués comme commandés")
            except Exception as e:
                print("❌ Erreur lors de la mise à jour des articles du panier:")
                print(str(e))
                return False
            
            return True
            
        except Exception as e:
            print("❌ Erreur lors de la préparation de la commande:")
            print(str(e))
            print(traceback.format_exc())
            return False
            
    except Exception as e:
        print("❌ Erreur générale dans validate_order:")
        print(str(e))
        print(traceback.format_exc())
        return False

@anvil.server.callable
def get_user_orders():
    try:
        print("=== Récupération des commandes utilisateur ===")
        user_data = anvil.server.call('get_user_info')
        user_id = user_data['user_id']
        print(f"ID utilisateur : {user_id}")
        
        # Récupérer toutes les commandes de l'utilisateur, triées par date décroissante
        orders = list(app_tables.orders.search(
            tables.order_by("date", ascending=False),
            user_id=user_id
        ))
        print(f"Nombre de commandes trouvées : {len(orders)}")
        return orders
        
    except Exception as e:
        print("❌ Erreur dans get_user_orders:")
        print(str(e))
        print(traceback.format_exc())
        return []

@anvil.server.callable
def debug_orders_table():
    """Fonction de débogage pour inspecter la structure de la table orders"""
    try:
        print("\n=== DÉBOGAGE TABLE ORDERS ===")
        
        # Vérifier si la table existe
        try:
            test = app_tables.orders.search()
            print("✅ Table orders accessible")
        except Exception as e:
            print("❌ Erreur d'accès à la table orders:")
            print(str(e))
            return
        
        # Obtenir la structure des colonnes
        print("\nStructure de la table:")
        for col in app_tables.orders.list_columns():
            print(f"- {col.name}: {col.type}")
            
        # Compter les entrées
        count = len(list(app_tables.orders.search()))
        print(f"\nNombre total d'entrées: {count}")
        
        # Afficher quelques entrées existantes
        print("\nDernières entrées (max 3):")
        entries = list(app_tables.orders.search(tables.order_by("date", ascending=False)))[:3]
        
        for i, entry in enumerate(entries, 1):
            print(f"\nEntrée {i}:")
            for key in entry:
                print(f"- {key}: {entry[key]}")
                
        return "Debug terminé"
        
    except Exception as e:
        print("\n❌ ERREUR lors du débogage:")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Message d'erreur: {str(e)}")
        print("\nTrace complète:")
        print(traceback.format_exc())
        return "Erreur de débogage"

  
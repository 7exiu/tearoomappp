import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import traceback


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
    try:
        print("=== Suppression du panier ===")
        user_data = anvil.server.call('get_user_info')
        user_id = user_data['user_id']
        print(f"ID utilisateur : {user_id}")
        
        produits_a_modifier = app_tables.temp.search(id_user=user_id, etat=False)
        count = 0
        for produit in produits_a_modifier:
            produit['etat'] = True
            count += 1
        
        print(f"✅ {count} articles marqués comme supprimés")
        return True
    except Exception as e:
        print("❌ Erreur dans delete_card:")
        print(str(e))
        print(traceback.format_exc())
        return False

  
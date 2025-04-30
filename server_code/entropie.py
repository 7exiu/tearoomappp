import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import math
import string

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
def calculer_entropie(mot_de_passe):
    """
    Calcule l'entropie d'un mot de passe en bits.
    
    Args:
        mot_de_passe (str): Le mot de passe à analyser
    
    Returns:
        tuple: (entropie en bits, taille de l'alphabet utilisé)
    """
    minuscules = set(string.ascii_lowercase)
    majuscules = set(string.ascii_uppercase)
    chiffres = set(string.digits)
    symboles = set(string.punctuation)
    
    taille_alphabet = 0
    if any(c in minuscules for c in mot_de_passe):
        taille_alphabet += 26
    if any(c in majuscules for c in mot_de_passe):
        taille_alphabet += 26
    if any(c in chiffres for c in mot_de_passe):
        taille_alphabet += 10
    if any(c in symboles for c in mot_de_passe):
        taille_alphabet += 32  # Il y a 32 caractères de ponctuation
    
    entropie = len(mot_de_passe) * math.log2(taille_alphabet)
    taille = len(mot_de_passe)
    redon = (taille * math.log2(taille_alphabet)) - entropie

    return entropie, taille_alphabet , redon
    
@anvil.server.callable  
def evaluer_securite(entropie):
      if entropie < 28:
        return "Très faible"
      elif entropie < 36:
        return "Faible"
      elif entropie < 60:
        return "Moyenne"
      elif entropie < 128:
        return "Forte"
      else:
        return "Très forte"

  

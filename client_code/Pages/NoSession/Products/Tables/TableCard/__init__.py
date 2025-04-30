from ._anvil_designer import TableCardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TableCard(TableCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    # Récupération des données de la table
    tearoom_table = self.item 

    # Mise à jour des champs individuels
    self.table_card_is_available.text = "Available" if tearoom_table["is_available"] else "Not available"
    self.table_card_capacity.text = str(tearoom_table["chairs_count"]) + " people"
    
    # Texte du bouton personnalisé avec nom, capacité et disponibilité
    self.outlined_button_1.text = (
      f"{tearoom_table['name']} - {tearoom_table['chairs_count']} people - "
      f"{'Available' if tearoom_table['is_available'] else 'Not available'}"
    )

  def outlined_button_1_click(self, **event_args):
    tearoom_table = self.item
    print(f"🔘 Bouton cliqué pour la table : {tearoom_table['name']}")

    # Appel à la fonction serveur personnalisée pour récupérer l'utilisateur via la session
    user_info = anvil.server.call('get_user_info')
    user_id = user_info.get('user_id', None)

    if not user_id:
        Notification("❌ Vous devez être connecté pour réserver une table.").show()
        print("❌ Utilisateur non connecté.")
        return

    try:
        print("📡 Envoi des infos au serveur...")
        result = anvil.server.call(
            'add_table_to_temp',
            name=tearoom_table['name'],
            chairs_count=tearoom_table['chairs_count'],
            is_available=tearoom_table['is_available'],
            user_id=user_id
        )
        Notification("✅ Table ajoutée à temp.").show()
        print("✅ Réponse serveur :", result)

    except Exception as e:
        print(f"❌ Erreur lors de l'ajout : {e}")
        Notification(f"Erreur : {e}").show()

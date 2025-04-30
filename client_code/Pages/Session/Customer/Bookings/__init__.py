from ._anvil_designer import BookingsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....NoSession.Products.Tables.TableCard import TableCard
from ....NoSession.Products.Goodies.GoodieCard import GoodieCard
from ....NoSession.Products.Teas.TeaCard import TeaCard

from anvil.tables import app_tables
from ....NoSession.Products.Tables import Tables
from ....NoSession.Products.Goodies.GoodieCard import GoodieCard
from ....NoSession.Products.Teas.TeaCard import TeaCard
from ....NoSession.Products.Tables.TableCard import TableCard



class Bookings(BookingsTemplate):
    def __init__(self, **properties):
        # Initialisation des propriétés et des composants
        self.init_components(**properties)
        self.display_tables()
        self.display_goodies()
        self.display_teas()

    def display_tables(self):
        try:
            tables = anvil.server.call('get_tables')
            self.tables_panel.clear()
            if not tables:
                self.tables_panel.add_component(Label(text="Pas de tables disponibles", align="center", font_size=16, foreground="#BA1A1A"))
            else:
                for table in tables:
                    # Créer un conteneur pour les informations de la table
                    table_info = FlowPanel()
                    
                    # Ajouter le nom de la table
                    name_label = Label(text=f"Table: {table['name']}", font_size=16, font="italic")
                    table_info.add_component(name_label)
                    
                    # Ajouter la capacité
                    capacity_label = Label(text=f"Capacité: {table['chairs_count']} personnes", font_size=14)
                    table_info.add_component(capacity_label)
                    
                    # Ajouter le statut de disponibilité
                    status = "Disponible" if table['is_available'] else "Non disponible"
                    status_label = Label(text=f"Statut: {status}", font_size=14, foreground="#4CAF50" if table['is_available'] else "#F44336")
                    table_info.add_component(status_label)
                    
                    # Ajouter un bouton de réservation si la table est disponible
                    if table['is_available']:
                        reserve_button = Button(
                            text="Réserver",
                            icon="fa:calendar-plus-o",
                            role="primary-color",
                            bold=True
                        )
                        
                        # Définir la fonction de callback pour le bouton
                        def reserve_click(table=table):
                            try:
                                # Vérifier si l'utilisateur est connecté
                                user_info = anvil.server.call('get_user_info')
                                if not user_info or not user_info.get('user_id'):
                                    Notification("Vous devez être connecté pour réserver une table", style="warning").show()
                                    return
                                
                                # Ajouter la table au panier temporaire
                                result = anvil.server.call(
                                    'add_table_to_temp',
                                    name=table['name'],
                                    chairs_count=table['chairs_count'],
                                    is_available=table['is_available'],
                                    user_id=user_info['user_id']
                                )
                                
                                if result:
                                    Notification("Table ajoutée au panier", style="success").show()
                                    # Rafraîchir l'affichage
                                    self.display_tables()
                                else:
                                    Notification("Erreur lors de l'ajout de la table au panier", style="danger").show()
                                    
                            except Exception as e:
                                Notification(f"Erreur: {str(e)}", style="danger").show()
                        
                        reserve_button.set_event_handler('click', reserve_click)
                        table_info.add_component(reserve_button)
                    
                    # Ajouter un séparateur
                    table_info.add_component(Spacer(height=10))
                    
                    # Ajouter le conteneur au panel principal
                    self.tables_panel.add_component(table_info)
                    
        except Exception as e:
            Notification(f"Erreur lors du chargement des tables : {e}", style="warning").show()

    def display_goodies(self):
        try:
            goodies = anvil.server.call('get_goodies')
            self.goodie_panel.clear()
            for goodie in goodies:
                self.goodie_panel.add_component(Image(source=goodie['image']))
        except Exception as e:
            Notification(f"Erreur lors du chargement des goodies : {e}", style="warning").show()

    def display_teas(self):
        try:
            teas = anvil.server.call('get_teas')
            self.teas_panel.clear()
            for tea in teas:
                self.teas_panel.add_component(Image(source=tea['image']))
        except Exception as e:
            Notification(f"Erreur lors du chargement des thés : {e}", style="warning").show()

    def form_show(self, **event_args):
        """Cette méthode est appelée quand le formulaire est affiché"""
        pass  # Vous pouvez éventuellement personnaliser davantage ici si nécessaire

    def cart_link_click(self, **event_args):
        """Clique sur le lien 'Panier'"""
        get_open_form().load_page("cart")

    def orders_link_click(self, **event_args):
        """Clique sur le lien 'Commandes'"""
        get_open_form().load_page("orders")

    def profile_link_click(self, **event_args):
        """Clique sur le lien 'Profil'"""
        get_open_form().load_page("profile")

    def teas_list_button_click(self, **event_args):
        get_open_form().load_page("teas")

    def goodies_list_button_click(self, **event_args):
        get_open_form().load_page("goodies")
      


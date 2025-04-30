from anvil import *

class OrdersTemplate(Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Création du conteneur principal
        self.content_panel = GridPanel()
        
        # Titre de la page
        self.title = Label(text="Mes Commandes", font_size=24, font_weight="bold")
        self.content_panel.add_component(self.title, row="0")
        
        # Panel pour les commandes
        self.orders_panel = RepeatingPanel()
        self.orders_panel.item_template = OrderItemTemplate
        self.content_panel.add_component(self.orders_panel, row="1")
        
        self.add_component(self.content_panel)

class OrderItemTemplate(Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Création du panel pour une commande
        self.order_panel = GridPanel(spacing="10")
        self.order_panel.role = "order-item"
        
        # En-tête de la commande
        self.header_panel = GridPanel()
        
        # Date et statut
        self.date_label = Label(font_size=14)
        self.header_panel.add_component(self.date_label, row="0", col="0")
        
        self.status_label = Label(font_size=14)
        self.header_panel.add_component(self.status_label, row="0", col="1")
        
        self.order_panel.add_component(self.header_panel, row="0")
        
        # Liste des articles
        self.items_panel = RepeatingPanel()
        self.items_panel.item_template = OrderItemProductTemplate
        self.order_panel.add_component(self.items_panel, row="1")
        
        # Total de la commande
        self.total_label = Label(font_size=16, font_weight="bold")
        self.order_panel.add_component(self.total_label, row="2")
        
        self.add_component(self.order_panel)
        
    def form_show(self, **event_args):
        """Affiche les détails de la commande"""
        if self.item:
            self.date_label.text = self.item['date'].strftime("%d/%m/%Y %H:%M")
            self.status_label.text = self.item['status']
            self.items_panel.items = self.item['content']
            self.total_label.text = f"Total : {self.item['total_amount']:.2f} €"

class OrderItemProductTemplate(Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Panel pour un produit de la commande
        self.product_panel = GridPanel()
        self.product_panel.role = "order-product"
        
        # Image du produit
        self.product_image = Image(width=60, height=60, display_mode="shrink_to_fit")
        self.product_panel.add_component(self.product_image, row="0", col="0", width_xs=80)
        
        # Informations du produit
        self.info_panel = GridPanel()
        
        self.product_name = Label(font_size=14, font_weight="bold")
        self.info_panel.add_component(self.product_name, row="0")
        
        self.product_price = Label(font_size=14)
        self.info_panel.add_component(self.product_price, row="1")
        
        self.product_panel.add_component(self.info_panel, row="0", col="1")
        
        self.add_component(self.product_panel)
        
    def form_show(self, **event_args):
        """Affiche les détails du produit"""
        if self.item:
            self.product_image.source = self.item['image']
            self.product_name.text = self.item['name']
            self.product_price.text = f"{self.item['price']:.2f} €" 
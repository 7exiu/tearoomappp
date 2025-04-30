import anvil.server
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io


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
def generer_recu(commande):
    """
    Génère un reçu PDF à partir des informations de la commande.

    Args:
        commande (dict): Un dictionnaire contenant les détails de la commande
       (par exemple, infos client, liste des produits, total).

    Returns:
        anvil.Media: Le reçu au format PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Informations de l'entreprise (à personnaliser)
    elements.append(Paragraph("Nom de votre entreprise", styles['h1']))
    elements.append(Paragraph("Adresse de votre entreprise", styles['normal']))
    elements.append(Spacer(1, 12))

    # Informations du client
    elements.append(Paragraph("Facture pour :", styles['h2']))
    elements.append(Paragraph(f"Nom: {commande['nom_client']}", styles['normal']))
    elements.append(Paragraph(f"Prénom: {commande['prenom_client']}", styles['normal']))
    elements.append(Paragraph(f"Email: {commande['email_client']}", styles['normal']))
    elements.append(Spacer(1, 12))

    # Détails de la commande
    elements.append(Paragraph("Détails de la commande :", styles['h2']))
    data = [["Produit", "Prix"]]
    for produit in commande['produits']:
        data.append([produit['nom'], f"{produit['prix']} €"])

    # Ajouter le total
    data.append(["Total", f"{commande['total']} €"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Message de fin (facultatif)
    elements.append(Paragraph("Merci pour votre commande !", styles['normal']))

    doc.build(elements)
    pdf_out = buffer.getvalue()
    return anvil.Media("application/pdf", pdf_out, f"recu_commande_{commande['id']}.pdf")

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
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from PIL import Image
import piexif
import io

@anvil.server.callable
def add_metadata(image_media, email):

    try:
        # Lire les bytes du fichier
        image_bytes = image_media.get_bytes()
        
        # Charger l'image depuis les bytes
        img = Image.open(io.BytesIO(image_bytes))

        # Convertir l'image en RGB (au cas où elle est en RGBA)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Créer un dictionnaire de métadonnées EXIF
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = f"Email: {email}"
        exif_bytes = piexif.dump(exif_dict)

        # Sauvegarder l'image avec les métadonnées dans un buffer mémoire
        output = io.BytesIO()
        img.save(output, format="JPEG", exif=exif_bytes)
        output.seek(0)

        # Retourner l'image modifiée comme Media object
        return anvil.BlobMedia("image/jpeg", output.read(), name=image_media.name)

    except Exception as e:
        print(f"Erreur lors de l'ajout des métadonnées : {str(e)}")

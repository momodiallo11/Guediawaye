from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from hot_boys.models import Photo

# (fichier dans static/img/galerie/, titre affiché sous la photo)
PHOTOS = [
    ("peche.jpg", "Pêche"),
    ("brt.jpg", "BRT"),
    ("cite.jpg", "Notre cité"),
    ("stade.jpg", "Notre stade"),
    ("maire.jpg", "Maire de Guédiawaye"),
    ("palais_justice.jpg", "Le Palais de justice"),
]


class Command(BaseCommand):
    help = "Importe les photos de static/img/galerie/ dans la galerie du site"

    def handle(self, *args, **options):
        # Supprime les anciennes photos d'exemple et les imports précédents
        anciennes = (
            Photo.objects.filter(image__startswith="galerie/exemple_")
            | Photo.objects.filter(image__startswith="galerie/paysage_")
            | Photo.objects.filter(image__startswith="galerie/import_")
        )
        for photo in anciennes:
            photo.image.delete(save=False)
            photo.delete()

        dossier = Path(settings.BASE_DIR) / "static" / "img" / "galerie"

        # La galerie affiche la plus récente en premier : on importe à l'envers
        # pour que "Pêche" soit la première photo affichée.
        for fichier, titre in reversed(PHOTOS):
            chemin = dossier / fichier
            if not chemin.exists():
                self.stdout.write(self.style.WARNING(f"Fichier introuvable : {chemin}"))
                continue
            with chemin.open("rb") as f:
                photo = Photo(titre=titre)
                photo.image.save(f"import_{fichier}", File(f), save=True)

        self.stdout.write(self.style.SUCCESS("Galerie importée."))

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from hot_boys.models import Membre

# (nom, fichier dans static/img/membres/, rôle utilisé si le membre n'existe pas encore)
MEMBRES = [
    ("Cheikh Fall", "cheikh_fall.jpg", "Responsable du sport"),
    ("Ibrahima Sow", "ibrahima_sow.jpg", "Trésorier"),
    ("Mamadou Diallo", "mamadou_diallo.jpg", "Président"),
    ("Aminata Ba", "aminata_ba.jpg", "Communication"),
    ("Awa Ndiaye", "awa_ndiaye.jpg", "Secrétaire générale"),
    ("Fatou Diop", "fatou_diop.jpg", "Responsable des activités"),
]


class Command(BaseCommand):
    help = "Ajoute les photos des membres (static/img/membres/)"

    def handle(self, *args, **options):
        dossier = Path(settings.BASE_DIR) / "static" / "img" / "membres"

        for nom, fichier, role in MEMBRES:
            chemin = dossier / fichier
            if not chemin.exists():
                self.stdout.write(self.style.WARNING(f"Fichier introuvable : {chemin}"))
                continue

            membre = Membre.objects.filter(nom__iexact=nom).first()
            if membre is None:
                membre = Membre(nom=nom, role=role)

            if membre.photo:
                membre.photo.delete(save=False)

            with chemin.open("rb") as f:
                membre.photo.save(f"import_{fichier}", File(f), save=True)

            self.stdout.write(f"Photo ajoutée : {membre.nom}")

        self.stdout.write(self.style.SUCCESS("Photos des membres importées."))

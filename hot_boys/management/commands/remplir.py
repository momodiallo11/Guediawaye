from datetime import timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

from hot_boys.models import Actualite, Evenement, Membre, Photo


def creer_image(texte, couleur, largeur=900, hauteur=675):
    """Crée une image de remplacement colorée avec un texte au centre."""
    image = Image.new("RGB", (largeur, hauteur), couleur)
    dessin = ImageDraw.Draw(image)
    try:
        police = ImageFont.load_default(size=48)
    except TypeError:
        police = ImageFont.load_default()

    boite = dessin.multiline_textbbox((0, 0), texte, font=police, align="center")
    x = (largeur - (boite[2] - boite[0])) / 2
    y = (hauteur - (boite[3] - boite[1])) / 2
    dessin.multiline_text((x, y), texte, font=police, fill="white", align="center")

    tampon = BytesIO()
    image.save(tampon, format="JPEG", quality=85)
    return ContentFile(tampon.getvalue())


class Command(BaseCommand):
    help = "Ajoute des actualités, événements, membres et photos d'exemple"

    def handle(self, *args, **options):
        maintenant = timezone.now().replace(minute=0, second=0, microsecond=0)

        # ---------- Actualités ----------
        actualites = [
            (
                "Grande opération de nettoyage du quartier",
                "Les jeunes et les familles de Hamo 6 se sont réunis pour nettoyer les rues, "
                "ramasser les déchets et dégager les caniveaux avant la saison des pluies.\n\n"
                "Merci à tous ceux qui sont venus avec leurs balais, leurs sacs et leur bonne humeur. "
                "Une nouvelle opération est prévue dans quelques semaines.",
            ),
            (
                "Ouverture des inscriptions pour le tournoi de football",
                "Le tournoi de football du quartier revient. Les équipes peuvent s'inscrire "
                "dès maintenant auprès des responsables de l'association.\n\n"
                "Chaque équipe doit compter au minimum dix joueurs. Les matchs auront lieu "
                "sur le terrain du quartier, en fin d'après-midi.",
            ),
            (
                "Réunion de l'association : les décisions prises",
                "Lors de la dernière réunion, les membres ont validé le calendrier des activités "
                "et décidé de lancer une collecte pour aider les familles en difficulté.\n\n"
                "Le compte rendu complet sera communiqué aux habitants.",
            ),
            (
                "Séance de formation pour les jeunes du quartier",
                "Une séance de formation gratuite est organisée pour les jeunes qui veulent "
                "apprendre un métier ou lancer une petite activité.\n\n"
                "Les places sont limitées, il faut s'inscrire à l'avance.",
            ),
        ]
        for titre, contenu in actualites:
            Actualite.objects.get_or_create(titre=titre, defaults={"contenu": contenu})

        # ---------- Événements ----------
        evenements = [
            ("Nettoyage collectif du quartier",
             "Rendez-vous avec balais et sacs. Le matériel de base est fourni.",
             maintenant + timedelta(days=5), "Place principale de Hamo 6"),
            ("Match de football inter-quartiers",
             "Venez encourager l'équipe du quartier.",
             maintenant + timedelta(days=12), "Terrain de Hamo 6"),
            ("Assemblée générale de l'association",
             "Bilan des activités et présentation des projets à venir. Tous les habitants sont invités.",
             maintenant + timedelta(days=20), "Local de l'association"),
            ("Soirée culturelle du quartier",
             "Musique, danse et théâtre avec les talents de Hamo 6.",
             maintenant + timedelta(days=30), "Place principale de Hamo 6"),
            ("Réunion de préparation du tournoi",
             "Réunion des responsables d'équipes.",
             maintenant - timedelta(days=10), "Local de l'association"),
            ("Distribution de fournitures scolaires",
             "Distribution aux enfants du quartier avant la rentrée.",
             maintenant - timedelta(days=25), "École du quartier"),
        ]
        for titre, description, date, lieu in evenements:
            Evenement.objects.get_or_create(
                titre=titre,
                defaults={"description": description, "date": date, "lieu": lieu},
            )

        # ---------- Membres ----------
        membres = [
            ("Mamadou Diallo", "Président",
             "Habitant de Hamo 6 depuis toujours, il coordonne les activités de l'association."),
            ("Awa Ndiaye", "Secrétaire générale",
             "Elle tient les comptes rendus et s'occupe de l'organisation des réunions."),
            ("Ibrahima Sow", "Trésorier",
             "Il gère les cotisations et les dépenses de l'association."),
            ("Fatou Diop", "Responsable des activités",
             "Elle prépare les événements et le calendrier du quartier."),
            ("Cheikh Fall", "Responsable du sport",
             "Il organise les entraînements et le tournoi de football."),
            ("Aminata Ba", "Communication",
             "Elle partage les nouvelles du quartier et gère les photos."),
        ]
        for nom, role, bio in membres:
            Membre.objects.get_or_create(nom=nom, defaults={"role": role, "bio": bio})

                # ---------- Galerie ----------
        photos = [
            ("Nettoyage du quartier", "#0b6b3a"),
            ("Tournoi de football", "#d62839"),
            ("Réunion de l'association", "#1d4e89"),
            ("Soirée culturelle", "#b8860b"),
            ("Formation des jeunes", "#6a3d9a"),
            ("Distribution scolaire", "#0f766e"),
        ]
        for i, (titre, couleur) in enumerate(photos, start=1):
            if Photo.objects.filter(titre=titre).exists():
                continue
            photo = Photo(titre=titre)
            image = creer_image(titre.replace(" ", "\n", 1), couleur)
            photo.image.save(f"exemple_{i}.jpg", image, save=True)

        self.stdout.write(self.style.SUCCESS(
            "Actualités, événements, membres et photos ajoutés."
        ))

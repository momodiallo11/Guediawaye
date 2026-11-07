import math
import random
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from hot_boys.models import Photo

L, H, S = 1200, 800, 2  # largeur, hauteur, finesse du dessin

VERT = (11, 107, 58)
JAUNE = (246, 194, 27)
ROUGE = (214, 40, 57)
BLEU = (29, 78, 137)


def melange(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


class Toile:
    def __init__(self):
        self.img = Image.new("RGB", (L * S, H * S))
        self.d = ImageDraw.Draw(self.img)

    def _s(self, pts):
        return [v * S for v in pts]

    def degrade(self, haut, bas, y0=0, y1=H):
        for y in range(int(y0 * S), int(y1 * S)):
            t = (y - y0 * S) / ((y1 - y0) * S)
            self.d.line([(0, y), (L * S, y)], fill=melange(haut, bas, t))

    def rect(self, x0, y0, x1, y1, c):
        self.d.rectangle(self._s([x0, y0, x1, y1]), fill=c)

    def contour(self, x0, y0, x1, y1, c, w=4):
        self.d.rectangle(self._s([x0, y0, x1, y1]), outline=c, width=w * S)

    def poly(self, pts, c):
        self.d.polygon(self._s([v for p in pts for v in p]), fill=c)

    def ellipse(self, x0, y0, x1, y1, c):
        self.d.ellipse(self._s([x0, y0, x1, y1]), fill=c)

    def cercle_contour(self, x0, y0, x1, y1, c, w=4):
        self.d.ellipse(self._s([x0, y0, x1, y1]), outline=c, width=w * S)

    def ligne(self, pts, c, w=2):
        self.d.line(self._s([v for p in pts for v in p]), fill=c, width=int(w * S))

    def sortie(self):
        img = self.img.resize((L, H), Image.LANCZOS)
        tampon = BytesIO()
        img.save(tampon, format="JPEG", quality=88)
        return ContentFile(tampon.getvalue())


def palmier(t, x, y, h, tronc, feuille):
    t.ligne([(x, y), (x + 8, y - h * 0.5), (x + 22, y - h)], tronc, 9)
    tx, ty = x + 22, y - h
    for a in (-170, -140, -110, -70, -40, -10):
        r = math.radians(a)
        lon = h * 0.55
        bout = (tx + math.cos(r) * lon, ty + math.sin(r) * lon * 0.5 + 40)
        milieu = (tx + math.cos(r) * lon * 0.5, ty + math.sin(r) * lon * 0.5 - 10)
        t.ligne([(tx, ty), milieu, bout], feuille, 8)


def maisons(t, y_sol, couleur, fenetre=None, graine=1):
    rnd = random.Random(graine)
    x = -20
    while x < L:
        w = rnd.randint(90, 160)
        h = rnd.randint(110, 230)
        t.rect(x, y_sol - h, x + w, y_sol + 5, couleur)
        if fenetre:
            for fx in range(int(x) + 18, int(x + w) - 25, 42):
                for fy in range(int(y_sol - h) + 20, int(y_sol) - 30, 50):
                    if rnd.random() < 0.55:
                        t.rect(fx, fy, fx + 20, fy + 28, fenetre)
        x += w + rnd.randint(4, 14)


def coucher_soleil():
    t = Toile()
    t.degrade((70, 40, 110), (255, 120, 70), 0, 460)
    t.degrade((255, 120, 70), (255, 215, 120), 460, 640)
    for r in range(260, 90, -12):
        k = 1 - (r - 90) / 170
        t.ellipse(600 - r, 470 - r, 600 + r, 470 + r, melange((255, 150, 80), (255, 245, 190), k))
    sombre = (42, 26, 62)
    maisons(t, 650, sombre, graine=4)
    t.rect(0, 640, L, H, sombre)
    for x, h in ((120, 330), (330, 260), (880, 340), (1060, 270)):
        palmier(t, x, 660, h, sombre, sombre)
    return t.sortie()


def terrain():
    t = Toile()
    for i in range(12):
        c = (46, 139, 60) if i % 2 == 0 else (56, 156, 72)
        t.rect(i * 100, 0, (i + 1) * 100, H, c)
    b = (245, 245, 235)
    t.contour(80, 80, 1120, 720, b, 5)
    t.ligne([(600, 80), (600, 720)], b, 5)
    t.cercle_contour(510, 310, 690, 490, b, 5)
    t.ellipse(594, 394, 606, 406, b)
    t.contour(80, 230, 260, 570, b, 5)
    t.contour(940, 230, 1120, 570, b, 5)
    t.contour(40, 345, 80, 455, b, 5)
    t.contour(1120, 345, 1160, 455, b, 5)
    rouges = [(200, 400), (330, 250), (340, 560), (470, 330), (500, 470)]
    jaunes = [(1000, 400), (870, 250), (860, 570), (730, 340), (700, 460)]
    for x, y in rouges:
        t.ellipse(x - 17, y - 17, x + 17, y + 17, ROUGE)
    for x, y in jaunes:
        t.ellipse(x - 17, y - 17, x + 17, y + 17, JAUNE)
    t.ellipse(560, 395, 580, 415, (255, 255, 255))
    return t.sortie()


def rue():
    t = Toile()
    t.degrade((120, 195, 240), (225, 242, 250), 0, 450)
    couleurs = [ROUGE, JAUNE, VERT, BLEU]
    for i, c in enumerate(couleurs):
        x0 = i * 300
        t.rect(x0, 230 + (i % 2) * 40, x0 + 296, 640, c)
        t.rect(x0, 215 + (i % 2) * 40, x0 + 296, 235 + (i % 2) * 40, melange(c, (0, 0, 0), 0.25))
        for fx in (x0 + 35, x0 + 205):
            t.rect(fx, 300 + (i % 2) * 40, fx + 55, 380 + (i % 2) * 40, (250, 245, 225))
            t.rect(fx - 14, 300 + (i % 2) * 40, fx, 380 + (i % 2) * 40, melange(c, (0, 0, 0), 0.4))
            t.rect(fx + 55, 300 + (i % 2) * 40, fx + 69, 380 + (i % 2) * 40, melange(c, (0, 0, 0), 0.4))
        t.rect(x0 + 120, 470, x0 + 180, 640, melange(c, (0, 0, 0), 0.5))
    t.rect(0, 640, L, H, (205, 175, 125))
    t.rect(0, 640, L, 655, (170, 140, 95))
    for i in range(30):
        x = i * 42 + 10
        y = 110 + 70 * (1 - ((x - 600) / 600) ** 2) * -1 + 70
        y = 190 - 70 * (1 - ((x - 600) / 600) ** 2)
        t.poly([(x, y), (x + 34, y), (x + 17, y + 38)], [ROUGE, JAUNE, VERT][i % 3])
    return t.sortie()


def pirogue():
    t = Toile()
    t.degrade((110, 185, 235), (250, 232, 195), 0, 400)
    t.ellipse(900, 110, 1020, 230, (255, 245, 205))
    t.degrade((35, 130, 180), (10, 70, 120), 400, 650)
    for i in range(14):
        y = 420 + i * 16
        for x in range((i * 53) % 110, L, 110):
            t.ligne([(x, y), (x + 30, y - 6), (x + 60, y)], (120, 190, 220), 3)
    t.poly([(300, 480), (880, 480), (830, 560), (360, 560)], ROUGE)
    t.poly([(318, 505), (870, 505), (856, 525), (334, 525)], JAUNE)
    t.poly([(334, 525), (856, 525), (845, 540), (345, 540)], VERT)
    t.poly([(880, 480), (960, 410), (940, 485)], ROUGE)
    t.poly([(300, 480), (250, 430), (310, 470)], ROUGE)
    t.ligne([(590, 480), (590, 330)], (70, 45, 25), 8)
    t.poly([(594, 335), (594, 470), (720, 470)], (250, 245, 230))
    t.rect(0, 650, L, H, (235, 210, 160))
    t.degrade((245, 250, 250), (35, 130, 180), 640, 660)
    t.rect(0, 660, L, H, (235, 210, 160))
    palmier(t, 120, 700, 300, (80, 55, 35), (30, 110, 60))
    palmier(t, 1080, 720, 260, (80, 55, 35), (30, 110, 60))
    return t.sortie()


def nuit():
    t = Toile()
    t.degrade((10, 15, 50), (50, 60, 125), 0, 650)
    rnd = random.Random(9)
    for _ in range(130):
        x, y, r = rnd.randint(0, L), rnd.randint(0, 420), rnd.choice((1, 1, 2, 2, 3))
        t.ellipse(x - r, y - r, x + r, y + r, (255, 255, 230))
    t.ellipse(940, 90, 1040, 190, (250, 245, 215))
    t.ellipse(965, 80, 1065, 180, (18, 24, 68))
    maisons(t, 650, (14, 18, 38), fenetre=(255, 205, 90), graine=11)
    t.rect(0, 640, L, H, (14, 18, 38))
    for i in range(32):
        x = i * 38 + 10
        y = 200 - 90 * (1 - ((x - 600) / 600) ** 2)
        c = [ROUGE, JAUNE, VERT, (255, 255, 255)][i % 4]
        t.ellipse(x - 9, y - 9, x + 9, y + 9, melange(c, (255, 255, 255), 0.2))
        t.ellipse(x - 5, y - 5, x + 5, y + 5, c)
    return t.sortie()


def baobab():
    t = Toile()
    t.degrade((255, 160, 55), (255, 232, 160), 0, 600)
    for r in range(220, 120, -10):
        k = 1 - (r - 120) / 100
        t.ellipse(600 - r, 420 - r, 600 + r, 420 + r, melange((255, 190, 90), (255, 248, 210), k))
    t.rect(0, 610, L, H, (92, 52, 32))
    t.degrade((140, 80, 40), (70, 38, 24), 600, 640)
    s = (42, 26, 18)
    t.poly([(515, 650), (545, 510), (530, 390), (560, 340), (640, 340), (670, 390), (655, 510), (695, 650)], s)
    for dx, dy in ((-270, -80), (-170, -150), (-60, -195), (60, -195), (170, -150), (270, -80)):
        x, y = 600 + dx, 345 + dy
        t.ligne([(600, 350), (600 + dx * 0.5, 345 + dy * 0.7), (x, y)], s, 14)
        sens = 1 if dx > 0 else -1
        t.ligne([(x, y), (x + 35 * sens, y - 35)], s, 8)
        t.ellipse(x - 48, y - 32, x + 48, y + 26, s)
    for bx, by in ((250, 150), (330, 110), (900, 130)):
        t.ligne([(bx, by), (bx + 14, by + 8), (bx + 28, by)], s, 3)
    return t.sortie()


SCENES = [
    ("Coucher de soleil sur Hamo 6", coucher_soleil),
    ("Le terrain de football du quartier", terrain),
    ("Les rues colorées", rue),
    ("Pirogue sur la plage", pirogue),
    ("Soirée culturelle", nuit),
    ("Le baobab du quartier", baobab),
]


class Command(BaseCommand):
    help = "Remplace les images d'exemple par de jolies illustrations"

    def handle(self, *args, **options):
        anciennes = Photo.objects.filter(image__startswith="galerie/exemple_")
        for p in anciennes:
            p.image.delete(save=False)
            p.delete()

        for i, (titre, dessiner) in enumerate(SCENES, start=1):
            if Photo.objects.filter(titre=titre).exists():
                continue
            photo = Photo(titre=titre)
            photo.image.save(f"paysage_{i}.jpg", dessiner(), save=True)

        self.stdout.write(self.style.SUCCESS("Galerie remplie."))

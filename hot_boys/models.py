from django.db import models


class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to="actualites/", blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_publication"]
        verbose_name = "actualité"

    def __str__(self):
        return self.titre


class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    lieu = models.CharField(max_length=200)

    class Meta:
        ordering = ["date"]
        verbose_name = "événement"

    def __str__(self):
        return f"{self.titre} ({self.date:%d/%m/%Y})"


class Membre(models.Model):
    nom = models.CharField(max_length=120)
    role = models.CharField(max_length=120, help_text="Ex : Président, Trésorier, Membre")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="membres/", blank=True, null=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} - {self.role}"


class Photo(models.Model):
    titre = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="galerie/")
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_ajout"]

    def __str__(self):
        return self.titre or f"Photo {self.pk}"


class Message(models.Model):
    nom = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_envoi"]

    def __str__(self):
        return f"Message de {self.nom}"

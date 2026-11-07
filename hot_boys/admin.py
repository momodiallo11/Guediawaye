from django.contrib import admin
from .models import Actualite, Evenement, Membre, Photo, Message


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ("titre", "date_publication")
    search_fields = ("titre", "contenu")


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ("titre", "date", "lieu")
    list_filter = ("date",)


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ("nom", "role")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("titre", "date_ajout")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "date_envoi", "lu")
    list_filter = ("lu",)

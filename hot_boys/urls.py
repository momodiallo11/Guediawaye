from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("actualites/", views.actualites, name="actualites"),
    path("actualites/<int:pk>/", views.actualite_detail, name="actualite_detail"),
    path("evenements/", views.evenements, name="evenements"),
    path("membres/", views.membres, name="membres"),
    path("galerie/", views.galerie, name="galerie"),
    path("a-propos/", views.a_propos, name="a_propos"),
    path("contact/", views.contact, name="contact"),
]

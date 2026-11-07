from django import template

from hot_boys.models import Photo

register = template.Library()


@register.simple_tag
def photo_entete(n=0):
    """Renvoie une photo de la galerie (une différente selon le numéro n)."""
    photos = list(Photo.objects.all()[:6])
    if not photos:
        return None
    return photos[int(n or 0) % len(photos)]

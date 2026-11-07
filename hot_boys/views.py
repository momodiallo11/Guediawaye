from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import MessageForm
from .models import Actualite, Evenement, Membre, Photo


def accueil(request):
    context = {
        "actualites": Actualite.objects.all()[:3],
        "evenements": Evenement.objects.filter(date__gte=timezone.now())[:4],
        "photos": Photo.objects.all()[:6],
        "membres": Membre.objects.all()[:4],
    }
    return render(request, "hot_boys/accueil.html", context)


def actualites(request):
    return render(request, "hot_boys/actualites.html", {"actualites": Actualite.objects.all()})


def actualite_detail(request, pk):
    actualite = get_object_or_404(Actualite, pk=pk)
    return render(request, "hot_boys/actualite_detail.html", {"actualite": actualite})


def evenements(request):
    maintenant = timezone.now()
    context = {
        "a_venir": Evenement.objects.filter(date__gte=maintenant),
        "passes": Evenement.objects.filter(date__lt=maintenant).order_by("-date")[:10],
    }
    return render(request, "hot_boys/evenements.html", context)


def membres(request):
    return render(request, "hot_boys/membres.html", {"membres": Membre.objects.all()})


def galerie(request):
    return render(request, "hot_boys/galerie.html", {"photos": Photo.objects.all()})


def contact(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message envoyé. Merci !")
            return redirect("contact")
    else:
        form = MessageForm()
    return render(request, "hot_boys/contact.html", {"form": form})


def a_propos(request):
    return render(request, "hot_boys/a_propos.html")

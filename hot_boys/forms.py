from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["nom", "email", "contenu"]
        labels = {"nom": "Ton nom", "email": "Email (facultatif)", "contenu": "Ton message"}
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "contenu": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }

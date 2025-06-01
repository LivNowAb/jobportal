from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, ModelChoiceField, Textarea

from .models import Response, Advertisement, Position


class AdCreation(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["heading", "position", "text", "salary"]

    heading = CharField(label="Název", max_length=128)
    position = ModelChoiceField(label="Pracovní Pozice", queryset=Position.objects, widget=forms.Select(attrs={"class": "form-control"}))
    text = CharField(label="Obsah", widget=Textarea(attrs={"class": "form-control", "cols": 40, "rows": 3}), required=True)
    salary = CharField(label="Mzda", max_length=250)


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['name', 'email', 'message', 'cv']
        labels = {
            'name': 'Jméno a příjmení',
            'email': 'E-mail',
            'message': 'Vaše zpráva',
            'cv': 'Přiložit CV',
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        }))

    password1 = forms.CharField(
        label='Heslo',
        widget=forms.PasswordInput(attrs=
                                   {'class': 'form-control'
                                    }))

    password2 = forms.CharField(
        label='Heslo znovu',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import CharField, ModelChoiceField, Textarea, BooleanField
from django.forms.fields import EmailField, ImageField

from .models import Response, Advertisement, Position, Client, BusinessType, District
from .error_messages import ERROR_MESSAGES


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Uživatelské jméno", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Heslo", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Heslo znovu", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ClientCreation(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["business_name", "business_type", "VAT_number", "address", "city", "district", "contact_email",
                  "contact_phone", "logo"]

    business_name = CharField(label="Název podniku", max_length=250)
    business_type = ModelChoiceField(label="Typ provozovny", queryset=BusinessType.objects.all())
    VAT_number = CharField(label="IČO/DIČ", max_length=25, required=True)
    address = CharField(label="Adresa provozovny", max_length=250)
    city = CharField(label="Město", max_length=250)
    district = ModelChoiceField(label="Okres", queryset=District.objects.all())
    contact_email = EmailField(label="Kontaktní e-mail provozovny")
    contact_phone = CharField(label="Kontaktní telefonní číslo provozovny", max_length=128)
    logo = ImageField(label="Logo provozovny", required=False)


class AdCreation(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["title", "position", "text_content", "salary", "highlight"]

    title = CharField(label="Název", max_length=128)
    position = ModelChoiceField(label="Pracovní Pozice", queryset=Position.objects,
                                widget=forms.Select(attrs={"class": "form-control"}))
    text_content = CharField(label="Obsah", widget=Textarea(attrs={"class": "form-control", "cols": 40, "rows": 3}),
                            required=True)
    salary = CharField(label="Mzda", max_length=250)
    highlight = BooleanField(label="Topovat inzerát (1000 Kč)", required=False)


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
        widgets = {
            'name': forms.TextInput(attrs={'id': 'fullname'}),
            'email': forms.EmailInput(attrs={'id': 'email'}),
            'message': forms.Textarea(attrs={'id': 'message'}),
            'cv': forms.ClearableFileInput(attrs={'id': 'cv'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError(ERROR_MESSAGES['invalid_email'])
        return email

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')

        if cv:
            if cv.size > 10 * 1024 * 1024:
                raise forms.ValidationError(ERROR_MESSAGES['file_too_large'])

            if not cv.content_type in ['application/pdf', 'application/msword',
                                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                       'image/jpeg', 'image/png']:
                raise forms.ValidationError(ERROR_MESSAGES['invalid_file_type'])
            return cv
        return None


class PaymentForm(forms.Form):
    card_number = forms.CharField(label="Číslo karty", max_length=16,
                                  widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}), required=True)
    cardholder_name = forms.CharField(label="Držitel karty", max_length=100,
                                      widget=forms.TextInput(attrs={'placeholder': 'Jan Novák'}), required=True)
    expiry_date = forms.CharField(label="Platnost karty do", max_length=5,
                                  widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}), required=True)
    cvv = forms.CharField(label="Kód CVC", max_length=3, widget=forms.PasswordInput(attrs={'placeholder': '123'}),
                          required=True)

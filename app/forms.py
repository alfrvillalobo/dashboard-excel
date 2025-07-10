from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ArchivoExcel

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ArchivoExcelForm(forms.ModelForm):
    class Meta:
        model = ArchivoExcel
        fields = ['archivo']

class AnalisisForm(forms.Form):
    columna_numerica = forms.ChoiceField(label="Columna numérica")
    columna_categorica = forms.ChoiceField(label="Columna categórica")

    def __init__(self, *args, columnas_num=None, columnas_cat=None, **kwargs):
        super().__init__(*args, **kwargs)
        if columnas_num:
            self.fields['columna_numerica'].choices = [(col, col) for col in columnas_num]
        if columnas_cat:
            self.fields['columna_categorica'].choices = [(col, col) for col in columnas_cat]

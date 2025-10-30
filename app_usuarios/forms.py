from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

class CadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'senha']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")


class EsqueciSenhaForm(PasswordResetForm):
    pass

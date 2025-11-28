from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

class CadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)

    # Adicionando o tipo de usuário (Aluno ou Segurança)
    TIPO_USUARIO_CHOICES = (
        ('aluno', 'Aluno'),
        ('seguranca', 'Segurança'),
    )
    tipo = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, label="Tipo de usuário")

    class Meta:
        model = User
        fields = ['username', 'email', 'senha']  # mantendo as opções de usuário, email e senha

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data
        

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")


class EsqueciSenhaForm(PasswordResetForm):
    pass

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CadastroForm

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['senha']
            )
            return redirect('login')  # redireciona para login depois do cadastro
    else:
        form = CadastroForm()
    return render(request, 'app_usuarios/cadastro.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CadastroForm, LoginForm



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            senha = form.cleaned_data["senha"]

            user = authenticate(request, username=username, password=senha)

            if user is not None:
                login(request, user)
                return redirect('index')  # Redireciona para a página inicial (ou outra)
            else:
                form.add_error(None, "Usuário ou senha incorretos.")
    else:
        form = LoginForm()
    
    return render(request, 'app_usuarios/login.html', {'form': form})



from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import EsqueciSenhaForm

class EsqueciSenhaView(PasswordResetView):
    template_name = 'app_usuarios/esqueci_senha.html'
    form_class = EsqueciSenhaForm
    success_url = reverse_lazy('login')  
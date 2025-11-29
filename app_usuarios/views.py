from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from .forms import CadastroForm, LoginForm, EsqueciSenhaForm
from .models import Reserva, Scan, Bicicleta, Perfil
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from .utils import tipo_required

import qrcode
from io import BytesIO


# ------------------ PÁGINAS PRINCIPAIS ------------------

def main_page(request):
    return render(request, 'app_usuarios/index.html')


@login_required(login_url='login')
@tipo_required('aluno')
def reserva_bikes(request):
    return render(request, 'app_usuarios/reservaBikes.html')


@login_required(login_url='login')
@tipo_required('aluno') 
def main_alunos(request):
    return render(request, 'app_usuarios/aluno.html')


def sobre(request):
    return render(request, 'app_usuarios/sobre.html')

@login_required(login_url='login')
@tipo_required('seguranca')
def erro_scan(request):
    return render(request, 'app_usuarios/erro_scan.html')

def contato(request):
    return render(request, 'app_usuarios/contato.html')


@login_required(login_url='login')
@tipo_required('seguranca')
def main_segurancas(request):
    return render(request, 'app_usuarios/seguranca.html')


@login_required(login_url='login')
@tipo_required('seguranca')
def scan(request):
    return render(request, 'app_usuarios/scanBikes.html')


@login_required(login_url='login')
@tipo_required('seguranca')
def scan_concluded_enter(request):
    return render(request, 'app_usuarios/scanConcluded.html')


@login_required(login_url='login')
@tipo_required('seguranca')
def scan_concluded_leave(request):
    return render(request, 'app_usuarios/scanConcludedLeaving.html')


# ------------------ CADASTRO ------------------

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['senha']
            )
            
            tipo = form.cleaned_data['tipo']
            Perfil.objects.create(user=usuario, tipo=tipo)
            
            return redirect('login')
    else:
        form = CadastroForm()

    return render(request, 'app_usuarios/cadastro.html', {'form': form})


# ------------------ LOGIN ------------------

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            senha = form.cleaned_data["senha"]

            user = authenticate(request, username=username, password=senha)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Usuário ou senha incorretos.")

    else:
        form = LoginForm()

    return render(request, 'app_usuarios/login.html', {'form': form})


# ------------------ ESQUECI SENHA ------------------

class EsqueciSenhaView(PasswordResetView):
    template_name = 'app_usuarios/esqueci_senha.html'
    email_template_name = 'app_usuarios/emails/resetar_senha_email.html'
    subject_template_name = 'app_usuarios/emails/assunto_resetar_senha.txt'
    success_url = reverse_lazy('password_reset_done')


# ------------------ GERAR QR ------------------

@login_required
def gerar_qr(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)

    # URL que será aberta pelo segurança ao ler o QR
    url = request.build_absolute_uri(f"/scan/{reserva.id}/")

    qr = qrcode.make(url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


# ------------------ SCAN - SEGURANÇA ------------------

@login_required
def scan_reserva(request, reserva_id):
    """
    Abre quando o segurança escaneia o QR Code.
    Decide automaticamente entrada (retirada) ou saída (devolução).
    """

    # Apenas seguranças podem escanear
    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "seguranca":
        return HttpResponse("Acesso negado: você não é segurança.")

    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Lógica de decisão:
    if reserva.status == "pendente":
        # aluno vai retirar a bike
        return redirect("registrar_scan", reserva_id=reserva.id, tipo="entrada")

    if reserva.status == "retirada":
        # aluno está devolvendo a bike
        return redirect("registrar_scan", reserva_id=reserva.id, tipo="saida")

    return HttpResponse("Reserva já finalizada.")


@login_required
def registrar_scan(request, reserva_id, tipo):
    """
    Segurança confirma a entrada (retirada) ou saída (devolução).
    """

    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "seguranca":
        return HttpResponse("Acesso negado: você não é segurança.")

    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Registrar log
    Scan.objects.create(
        reserva=reserva,
        seguranca=request.user,
        tipo=tipo
    )

    if tipo == "entrada":
        reserva.status = "retirada"
        reserva.data_hora_retirada = timezone.now()
        reserva.bicicleta.disponivel = False
        reserva.bicicleta.save()
        reserva.save()

        return redirect("scan_con_ent")  # Página de sucesso para entrada

    elif tipo == "saida":  # aluno devolvendo a bike
        reserva.status = "devolvida"
        reserva.data_hora_devolucao = timezone.now()
        reserva.bicicleta.disponivel = True
        reserva.bicicleta.save()
        reserva.save()

        return redirect("scan_con_lea")  # Página de sucesso para saída


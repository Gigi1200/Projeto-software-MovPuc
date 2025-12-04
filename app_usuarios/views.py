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


# Página principal do segurança (sem ID)
@login_required(login_url='login')
@tipo_required('seguranca')
def scan(request):
    return render(request, 'app_usuarios/scanBikes.html')


# ------------------ PÁGINAS DE CONCLUSÃO ------------------

@login_required(login_url='login')
@tipo_required('seguranca')
def scan_concluded_enter(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'app_usuarios/scanConcluded.html', {"reserva": reserva})


@login_required(login_url='login')
@tipo_required('seguranca')
def scan_concluded_leave(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'app_usuarios/scanConcludedLeaving.html', {"reserva": reserva})


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

    url = request.build_absolute_uri(f"/scan/{reserva.id}/")
    qr = qrcode.make(url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


# ------------------ SCAN - SEGURANÇA ------------------

@login_required
def scan_reserva(request, reserva_id):

    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "seguranca":
        return HttpResponse("Acesso negado: você não é segurança.")

    reserva = get_object_or_404(Reserva, id=reserva_id)

    if reserva.status == "pendente":
        return redirect("registrar_scan", reserva_id=reserva.id, tipo="entrada")

    if reserva.status == "retirada":
        return redirect("registrar_scan", reserva_id=reserva.id, tipo="saida")

    return HttpResponse("Reserva já finalizada.")


@login_required
def registrar_scan(request, reserva_id, tipo):

    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "seguranca":
        return HttpResponse("Acesso negado: você não é segurança.")

    reserva = get_object_or_404(Reserva, id=reserva_id)

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

        return redirect("scan_con_ent", reserva_id=reserva.id)

    elif tipo == "saida":
        reserva.status = "devolvida"
        reserva.data_hora_devolucao = timezone.now()
        reserva.bicicleta.disponivel = True
        reserva.bicicleta.save()
        reserva.save()

        return redirect("scan_con_lea", reserva_id=reserva.id)

from django.http import JsonResponse

@login_required(login_url='login')
@tipo_required('aluno')
def reservar_vaga(request, vaga_id):

    # Esperar POST
    if request.method != "POST":
        return JsonResponse({"erro": "Use POST"}, status=405)

    # Buscar bicicleta por codigo (que é string no seu model)
    try:
        bicicleta = Bicicleta.objects.get(codigo=str(vaga_id))
    except Bicicleta.DoesNotExist:
        return JsonResponse({"erro": "Vaga inexistente"}, status=404)

    # Verificar disponibilidade
    if not bicicleta.disponivel:
        return JsonResponse({"erro": "Vaga já reservada"}, status=400)

    # Criar reserva
    reserva = Reserva.objects.create(
        aluno=request.user,
        bicicleta=bicicleta,
        status="pendente"
    )

    # Marcar como ocupada
    bicicleta.disponivel = False
    bicicleta.save()

    return JsonResponse({"sucesso": True, "reserva_id": reserva.id})
from .models import Vaga


@login_required(login_url='login')
@tipo_required('aluno')
def reserva_bikes(request):
    vagas = Vaga.objects.all().order_by("numero")
    return render(request, 'app_usuarios/reservaBikes.html', {"vagas": vagas})


@login_required(login_url='login')
@tipo_required('aluno')
def reservar_vaga(request, numero):
    vaga = get_object_or_404(Vaga, numero=numero)

    if vaga.disponivel:
        vaga.disponivel = False
        vaga.save()

    return redirect('reserva_bikes')

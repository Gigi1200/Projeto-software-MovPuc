from django.urls import path
from . import views
from .views import EsqueciSenhaView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('reserva_bikes/', views.reserva_bikes, name='reserva_bikes'),
    path('aluno/', views.main_alunos, name='aluno'),
    path('seguranca/', views.main_segurancas, name='seguranca'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('escanear/', views.scan, name='scan'),
    path('escanear/entering/', views.scan_concluded_enter, name='scan_con_ent'),
    path('escanear/leaving/', views.scan_concluded_leave, name='scan_con_lea'),
    path('', views.main_page, name='index'),
    path("gerar_qr/<int:reserva_id>/", views.gerar_qr, name="gerar_qr"),

    # quando o segurança escaneia o QR
    path("scan/<int:reserva_id>/", views.scan_reserva, name="scan_reserva"),

    # segurança confirma entrada/saída
    path("registrar_scan/<int:reserva_id>/<str:tipo>/", views.registrar_scan, name="registrar_scan"),

    # Password reset initiation page
      path('esqueci-senha/', auth_views.PasswordResetView.as_view(
        template_name='app_usuarios/esqueci_senha.html',
        email_template_name='app_usuarios/emails/resetar_senha_email.html',       # Versão Texto (obrigatório)
        html_email_template_name='app_usuarios/emails/resetar_senha_email.html',  # <--- LINHA NOVA: Versão HTML
        subject_template_name='app_usuarios/emails/assunto_resetar_senha.txt',
        success_url='password_reset_done'),
    name='esqueci_senha'),

    # Página que confirma que o e-mail foi enviado
    path('esqueci-senha/password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app_usuarios/sucesso.html'),  # Página que informa que o e-mail foi enviado
    name='password_reset_done'),

    # Página onde o usuário vai inserir a nova senha (com UID e token)
    path('resetar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app_usuarios/resetar_senha.html',  # Formulário para inserir a nova senha
        success_url='/resetar-senha/concluido/'),  # Página de sucesso após a redefinição
    name='password_reset_confirm'),

    # Página final de sucesso após redefinir a senha
    path('resetar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app_usuarios/concluido.html'),  # Página de confirmação de sucesso
    name='password_reset_complete'),
]

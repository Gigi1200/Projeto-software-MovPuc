from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main_page, name='index'),

    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),

    path('aluno/', views.main_alunos, name='aluno'),
    path('seguranca/', views.main_segurancas, name='seguranca'),

    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),

    path('reserva_bikes/', views.reserva_bikes, name='reserva_bikes'),
    path('reservar/<int:numero>/', views.reservar_vaga, name='reservar_vaga'),

    path("gerar_qr/<int:reserva_id>/", views.gerar_qr, name="gerar_qr"),
    path("scan/<int:reserva_id>/", views.scan_reserva, name="scan_reserva"),
    path("registrar_scan/<int:reserva_id>/<str:tipo>/", views.registrar_scan, name="registrar_scan"),
        path(
        "scan_concluded/entrada/<int:reserva_id>/",
        views.scan_concluded_enter,
        name="scan_con_ent",
    ),
    path(
        "scan_concluded/saida/<int:reserva_id>/",
        views.scan_concluded_leave,
        name="scan_con_lea",
    ),


    path('esqueci-senha/', auth_views.PasswordResetView.as_view(
        template_name='app_usuarios/esqueci_senha.html',
        email_template_name='app_usuarios/emails/resetar_senha_email.html',
        html_email_template_name='app_usuarios/emails/resetar_senha_email.html',
        subject_template_name='app_usuarios/emails/assunto_resetar_senha.txt',
        success_url='password_reset_done'),
    name='esqueci_senha'),

    path('esqueci-senha/password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app_usuarios/sucesso.html'),
    name='password_reset_done'),

    path('resetar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app_usuarios/resetar_senha.html',
        success_url='/resetar-senha/concluido/'),
    name='password_reset_confirm'),

    path('resetar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app_usuarios/concluido.html'),
    name='password_reset_complete'),

    path('erro_scan/', views.erro_scan, name='erro_scan'),
]

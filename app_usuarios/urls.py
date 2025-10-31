from django.urls import path
from . import views

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
    path('', views.main_page, name='index')
]

from django.contrib import admin
from django.urls import path
from atendimentos import views
from usuarios import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('usuarios/', user_views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/novo/', user_views.novo_usuario, name='novo_usuario'),
    path('usuarios/<int:pk>/editar/', user_views.editar_usuario, name='editar_usuario'),
    path('minha-senha/', user_views.trocar_senha, name='trocar_senha'),
    path('', views.dashboard, name='dashboard'),
    path('atendimentos/', views.lista_atendimentos, name='lista_atendimentos'),
    path('atendimentos/novo/', views.novo_atendimento, name='novo_atendimento'),
    path('atendimentos/<int:pk>/', views.detalhe_atendimento, name='detalhe_atendimento'),
    path('atendimentos/<int:pk>/editar/', views.editar_atendimento, name='editar_atendimento'),
    path('atendimentos/<int:pk>/pdf/', views.ficha_pdf, name='ficha_pdf'),
    path('atendimentos/<int:pk>/status/', views.atualizar_status, name='atualizar_status'),
]

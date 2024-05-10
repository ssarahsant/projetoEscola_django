from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.formulario_novo_user, name='cad_usuario'),
    path('salvar_usuario', views.salva_usuario, name='salvar_usuario'),
]

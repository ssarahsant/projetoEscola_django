from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('fechar', views.fechar, name='fechar'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('lista_turma/<int:id_professor>',views.lista_turma, name='lista_turma'),
    path("excluir_turma/<int:id_turma>", views.excluir_turma, name="excluir_turma"),
    path("cad_atividade/<int:id_turma>", views.cad_atividade, name="cad_atividade")
    # path("salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    # path("lista_atividade/<int:id_atividade>", views.lista_atividade, name:"lista_atividade")
]

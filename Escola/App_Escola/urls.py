from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('fechar', views.fechar, name='fechar'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('lista_turma/<int:id_professor>',views.lista_turma, name='lista_turma'),
    path('excluir_turma/<int:id_turma>', views.excluir_turma, name='excluir_turma'),
    path('cad_atividade/<int:id_turma>', views.cad_atividade, name='cad_atividade'),
    path('atividade_arquivos/<str:nome_arquivo>', views.exibir_arquivo, name='exibir_arquivo'),
    path('exportar_para_excel_turmas', views.exportar_para_excel_turmas, name='exportar_para_excel_turmas'),
    path('exportar_para_excel_atividades', views.exportar_para_excel_atividades, name='exportar_para_excel_atividades')
]

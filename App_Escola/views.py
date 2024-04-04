from django.shortcuts import render

from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages # biblioteca de mensagens do django

# Cria todas as funções
def abre_index(request):
    return render(request, 'login.html')

# criação de dados dentro da base de dados
def initial_population():
    print("Populando o banco de dados")

    cursor = connection.cursor()

    # Populando Tabela Professor
    senha = "123456" # senha incial para todos os usuários
    senha_armazenar = sha256(senha.encode()).hexdigest()

    # Montamos aqui nossa intrução SQL
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '"+ senha_armazenar +"'),"
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '"+ senha_armazenar +"'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jin', 'xi.jin@gmail.com', '"+ senha_armazenar +"')"

    cursor.execute(insert_sql_professor)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da população da tabela professor


    # Populando Tabela Turma
    # Montando uma instrução SQL
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1° Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2° Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3° Semestre - Desenvolvimento de Sistemas', 3)"

    cursor.execute(insert_sql_turma)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da população da tabela turma

    # Populando Tabela Atividade
    # Montando uma instrução SQL
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_turma + "('Apresentar Fundamentos de Programação', 1),"
    insert_sql_atividade = insert_sql_turma + "('Apresentar Framework Django', 2),"
    insert_sql_atividade = insert_sql_turma + "('Apresentar conceitos de Gerenciamento de Projetos', 3)"

    cursor.execute(insert_sql_atividade)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da população da tabela turma

    print("Tabelas populadas")
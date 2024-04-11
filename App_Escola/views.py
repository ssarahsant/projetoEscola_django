from django.shortcuts import render, redirect
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages # biblioteca de mensagens do django
from django.http import HttpResponse

# Cria todas as funções
# Função de popular as Tabelas do Banco de Dados
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
    print("Inseri professor")

    # Populando Tabela Turma
    # Montando uma instrução SQL
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1° Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2° Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3° Semestre - Desenvolvimento de Sistemas', 3)"
    

    cursor.execute(insert_sql_turma)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da população da tabela turma
    print("Inseri Turma")

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


# AP FAZER UM INSERT NO BANCO DE DADOS o insert COMMIT para garvar os dados permanet=netemnete no banco de dado fisico. - grava no banco de dados fisicos
# rowback - quando está em um insert longo, caso ocorra uma incosistencia (se der um erro ou algum parametro esteja incorrespondnetes), todo o insert é deixado de garvar - não faz a gravação dos dados se ocorrer algum erro 

def abre_index(request):
    #return render(request, 'login.html')
    dado_pesquisa = 'Obama'

    verifica_populado = Professor.objects.filter(nome__icontains=dado_pesquisa)

    if len(verifica_populado)==0:
        print("Não fpo populado")
        initial_population()
    else:
        print("achei Obama")
    return render(request, 'login.html')

# Função de Login
def enviar_login(request):
    if (request.method == 'POST'):
        email = request.POST['email']
        senha = request.POST['senha']
        senha_criptografada = sha256(senha.encode()).hexdigest()
        # resgata do banco de dados para o código analisar as informações
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")
        print("Dados do Professor", dados_professor)

        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            
            if (senha == senha_criptografada):
                # Se logou corretamente, traz as turmas do professor
                # Para isso instanciamos o model turmas professor
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
                print("Turma do professor", turmas_do_professor)
                return render(request, "cadastro_turma.html", { 
                    'usuario-logado': usuario_logado,
                    'turmas_do_professor':turmas_do_professor,
                    'id_logado': id_logado
                })
            
            else:
                messages.info(request, 'Uusário ou senha incorreta. Tente novamente.')
                return render(request, 'login.html')
            
        
        messages.info(request, "Olá " + email + ", seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu cadastro.")
        return render(request, 'cadastro.html', {'login': email})
    
    return render(request, "login.html")
    

# Função Cadastro
def confirmar_cadastro(request):
    if (request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        grava_professor = Professor (
            nome=nome,
            email=email,
            senha=senha_criptografada
        )
        grava_professor.save()

        mensagem = "OLÁ PROFESSOR " + nome + ", SEJA BEM-VINDO"
        return HttpResponse(mensagem)
    
from django.shortcuts import render, redirect
from hashlib import sha256

from django.urls import reverse
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages # biblioteca de mensagens do django
from django.http import HttpResponse, HttpResponseRedirect

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


#_____________________________________Cadastro de Professores_______________________________________

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
                    'usuario_logado': usuario_logado,
                    'turmas_professor': turmas_do_professor,
                    'id_logado': id_logado
                })
            
            else:
                return render(request, "login.html", {
                    "error_message": "Usuário ou senha incorretos. Tente novamente!"
                })
            
        
        # messages.info(request, "Olá " + email + ", seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu cadastro.")
        # Renderiza tela
        return render(request, 'cadastro.html', {
            'login': email
        })
    
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

        return HttpResponseRedirect(reverse('enviar_login'))


#______________________________________Cadatro de Turmas_______________________________________

# Função para Cadastrar Turma
def cad_turma(request, id_professor):
    if request.method == 'POST':
        turma = request.POST["turma"]
        professor = Professor.objects.get(id=id_professor)

        with transaction.atomic():
            grava_turma = Turma(nome_turma=turma, id_professor=professor)
            grava_turma.save()
        
        turmas_professor = Turma.objects.filter(id_professor=id_professor)

        return render(request, "cadastro_turma.html", {
            "turmas_professor": turmas_professor,
            "id_logado": id_professor
        })
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']
    print(f"turmas professor get {turmas_professor}")
    return render(request, 'cadastro_turma.html', {
        'usuario_logado': usuario_logado, 
        'id_logado': id_professor,
        "turmas_professor": turmas_professor
    }),


# Função que carrega as turmas já adastrada na tela
def lista_turma(request, id_professor):
    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
    return render(request, 'Const_Turma_Lista.html', 
                 {'usuario_logado': usuario_logado, 'tumas_do_professor':turmas_do_professor,
                  'id_logado': id_logado} )

def excluir_turma(request, id_turma):
    try:
        with transaction.atomic():
            turma = Turma.objects.get(pk=id_turma)
            id_professor = turma.id_professor_id
            turma.delete()

            professor = Professor.objects.get(pk=id_professor)
            turmas_professor = Turma.objects.filter(id_professor=id_professor)

        return render(request, "cadastro_turma.html", {
            "turmas_professor": turmas_professor,
            "id_logado": id_professor
        })
    except Turma.DoesNotExist:
        pass

#______________________________________Cadastro de Atividades_______________________________________

def cad_atividade(request, id_turma):
    turma = Turma.objects.get(pk=id_turma)
    atividades_turma = Atividade.objects.filter(id_turma_id=id_turma)
    arquivo = request.FILES.get('arquivo')
    # se o metodo for post ()
    if request.method == 'POST':
        descricao = request.POST["descricao"]
        turma = Turma.objects.get(pk=id_turma)

        # atomicidade, executa somente se der tudo certo
        with transaction.atomic():
            grava_atividade = Atividade(
                nome_atividade=descricao, id_turma=turma,
                arquivo = arquivo  # acho que é aqui
        )
            grava_atividade.save()

        atividades_turma = Atividade.objects.filter(id_turma_id = id_turma)
            
        return render(request, "cadastro_atividade.html", {
            # contexto passado para o html
            "turma_id": id_turma,
            "atividades_turma": atividades_turma
        })
    return render(request, 'cadastro_atividade.html', {
        "turma_id": id_turma,
        "atividades_turma": atividades_turma
    })

def fechar(request):
    return render(request, "login.html")
#______________________________________________________________________________________________

# def lista_Atividade(request, id_turma):
#     dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
#     usuario_logado = dados_professor[0]
#     usuario_logado = usuario_logado['nome']
#     id_logado = dados_professor[0]
#     id_logado = id_logado['id']
#     turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
#     return render(request, 'Const_Turma_Lista.html', 
#                  {'usuario_logado': usuario_logado, 'tumas_do_professor':turmas_do_professor,
#                   'id_logado': id_logado} )

# def excluir_atividde(request, id_turma):
#     try:
#         with transaction.atomic():
#             atividade = Atividade.objects.get(pk=id_turma)
#             id_turma = atividade.id_turma_id
#             atividade.delete()

#             turma = Turma.objects.get(pk=id_atividade)
#             atividades_turma = Atividade.objects.filter(id_turma_id=id_turma)

#         return render(request, "cadastro_turma.html", {
#             "turmas_professor": turmas_professor,
#             "id_logado": id_professor
#         })
#     except Turma.DoesNotExist:
#         # Trate aqui o caso em que a turma não existe
#         # Por exemplo, redirecione o usuário para uma página de erro
#         pass


# Função para Salvar Novas Turmas
# def salvar_turma_nova(request):
#     if (request.method == 'POST'):
#         nome_turma = request.POSTT.get('nova_turma')
#         id_professor = request.POST.get('id_professor')
#         professor = Professor.objects.get(id=id_professor)
#         grava_turma = Turma (
#             nome_turma=nome_turma,
#             id_professor=id_professor
#         )
#         grava_turma.save()
#         messages.info(request, 'Turma' + nome_turma + 'cadastrado com sucesso')

#         # Redireciona para uma nova URL após a gravação bem sucedida
#         return redirect('lista_turma', id_professor=id_professor)

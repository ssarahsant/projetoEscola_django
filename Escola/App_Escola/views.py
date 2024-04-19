from django.shortcuts import render, redirect
from hashlib import sha256
from .models import Professor,Turma,Atividade
from django.db import connection, transaction
from django.contrib import messages
from django.http import HttpResponse

# def abre_index(request):
#     return render(request, 'login.html')

def abre_index(request):
    #return render(request, 'Index.html')
    dado_pesquisa = 'Obama'
 
    verifica_populado = Professor.objects.filter(nome__icontains = dado_pesquisa)
 
    if len(verifica_populado) == 0:
        print("Não está populado")
        initial_population() # chama a função para realizar a população
    else:
        print("Achei o Obama", verifica_populado)
 
    return render(request, 'login.html')


def initial_population():
    print("Vou popular")

    cursor = connection.cursor()

    #tabela professor
    senha= "123456" #senha inicial para todos usuarios
    senha_armazenar = sha256(senha.encode()).hexdigest()

    #montagm da instrução do sql
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email,senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar +"'),"
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '" + senha_armazenar +"'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar +"')"

    cursor.execute(insert_sql_professor)
    transaction.atomic()#nrecessario commit para insert e update
    #fim da tabela professor


    #tabela turma
    #inserir dados
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma , id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1o Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2o Semestre - Desenvolvimento de Sistemas',2),"
    insert_sql_turma = insert_sql_turma + "('3o Semestre - Desenvolvimento de Sistemas',3)"

    cursor.execute(insert_sql_turma)
    transaction.atomic() #Necessario commit para insert e update

    #Fim da população da tabela Turma

    #Popular Tabela Atividade
    #Montamos aqui nossa instrução SQL.
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade , id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programação',1),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar FrameWork Django',2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de Gerenciamento de Projetos',3)"

    cursor.execute(insert_sql_atividade)
    transaction.atomic() #Necessario commit apara insert e update

    #Fim da população da Tabela Atividade
    print("Populei")

def enviar_login(request):

    if(request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha","id")
        print("Dados do professor" , dados_professor)
        #if len(dados_professor) > 0:
        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado ['nome']
            if(senha == senha_criptografada):

                #Se logou corretamente, traz as turmas do professor
                #Para isso instanciamos o model turmas do professor
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
                print("Turma do Professor" ,turmas_do_professor)
                return render(request, 'const_lista_turma.html',{'usuario_logado': usuario_logado,
                                                                'turmas_do_professor': turmas_do_professor,
                                                                'id_logado': id_logado})
            else:
                messages.info(request, "Usuario ou senha incorretos.Tente novamente.")
                return render(request, 'login.html')
            
        messages.info(request, "Ola" + email + ", seja bem-vindo! Percebemos que você é novo por aqui.Complete seu cadastro.")
        return render(request, 'cadastro.html', {'login': email})
    
def confirmar_cadastro(request):
    if(request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        grava_professor = Professor (
            nome=nome,
            email=email,
            senha=senha_criptografada
        )
        grava_professor.save()

        mensagem = "OLÁ PROFESSOR " + nome + ", SEJA BEM VINDO!"
        return HttpResponse(mensagem)

def cad_turma(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome","id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']
    #print (usuario_logado, "USUARIO LOGADO EM CAD_CLIENTE")
    return render(request, 'cad_turma.html' , {'usuario_logado': usuario_logado, 'id_logado': id_professor})

def salvar_turma_nova(request):
    if(request.method == 'POST'):
        nome_turma = request.POST.get('nome_turma')
        id_professor = request.POST.get('id_professor')
        professor = Professor.objects.get(id=id_professor)
        grava_turma = Turma(
            nome_turma=nome_turma,
            id_professor=professor
        )
        grava_turma.save()
        messages.info(request, 'Turma' + nome_turma + 'cadastrado com sucesso.') 
        return redirect('lista_turma', id_professor=id_professor)
    
def lista_turma(request, id_professor):
    dados_professor = Professor.objects.filter(id=id_professor).values("nome" ,"id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado  = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
    return render(request, 'const_lista_turma.html',
                  {'usuario_logado' : usuario_logado, 'turmas_do_professor': turmas_do_professor,
                   'id_logado': id_logado})


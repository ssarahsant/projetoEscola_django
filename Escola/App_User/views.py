from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def formulario_novo_user(request):
    return render(request, 'cad_user.html')

#Faz a validação de autenticação do usuário
@login_required
def salva_usuario(request):
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    print(usuario, email, senha)
    
    usuario_logado = request.user.username
    
    if usuario is not None and usuario != '' and email is not None and email != '' and senha is not None and senha != '':
        try:
            tem_usuario = User.objects.get(username=usuario)
            if tem_usuario:
                messages.info(request, "Usuário já existe, tente outro.")
                return render(request, 'cad_user.html')
        except User.DoesNotExist:
            dados_usuario = User.objects.create_user(username=usuario, email=email, password=senha)
            dados_usuario.save()
            messages.info(request, "Usuário salvo com sucesso.")
            return render(request, 'cad_user.html', {'usuario_logado': usuario_logado})

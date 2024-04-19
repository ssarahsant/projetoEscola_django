from django.db import models

# Create your models here.

# Criação do banco de dados através do padrão django

# criação de trÊs tabelas, professor, turma e atividade
# não precisa de tabela de associação, porque uma turma pertene somente a um professor
# uma atividade so pode pertencer a uma turma

# para criar o banco de dados preciso de dois comandos:

# prepara uma isntrução sql para ser posterioemnte executada no banco de dados
# python manage.py makemigrations

# para excutar o comando no banco de dados
# o comando esta na dentro da pasta  migritions
# python manage.py migrate

# todas vez que mexer no model deve se executar esses dois passos 


class Professor(models.Model):
    nome = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    senha = models.CharField(max_length=64)

    def __str__(self):
        return self.nome
    
class Turma(models.Model):
    nome_turma = models.CharField(max_length=120)
    # FK: 
    id_professor = models.ForeignKey(Professor, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome_turma
    
class Atividade(models.Model):
    nome_atividade = models.CharField(max_length=120)
    id_professor = models.ForeignKey(Professor, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome_atividade
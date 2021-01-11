from django.db import models

#modelo onde é salvo o simbolo das ações que o usuário adicionou
class Acao(models.Model):
    simbolo = models.CharField(max_length=10)
    
    def __str__(self):
        return self.simbolo

#modelo onde é salvo todos os preços salvos pelo script para 
#   consulta posterior
class Preco(models.Model):
    simbolo = models.ForeignKey(Acao, on_delete=models.CASCADE)
    preco = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

#modelo onde é salvo os dados mais recentes das ações adicionadas
class Salvo(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10, unique=True)
    preco = models.FloatField()
    alta = models.FloatField()
    baixa = models.FloatField()
    fechAnt = models.FloatField()
    capMerc = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

#modelo onde é salvo os emails para eventuais avisos
class Email(models.Model):
    email = models.CharField(max_length=100, unique=True)

#modelo onde é salvo os limites de compra e vendas para cada ação
class Perfil(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    simbolo = models.ForeignKey(Acao, on_delete=models.CASCADE)
    limSup = models.FloatField(blank=True, null=True)
    limInf = models.FloatField(blank=True, null=True)

#modelo para salvar o tempo de atualização do script
class TaskTime(models.Model):
    numero = models.FloatField()
    tempo = models.CharField(max_length=10)

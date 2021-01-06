from django.db import models

class Acao(models.Model):
    simbolo = models.CharField(max_length=10)
    
    def __str__(self):
        return self.simbolo

class Preco(models.Model):
    simbolo = models.ForeignKey(Acao, on_delete=models.CASCADE)
    preco = models.FloatField()
    data = models.DateField(auto_now_add=True)

class Salvo(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10)
    preco = models.FloatField()
    alta = models.FloatField()
    baixa = models.FloatField()
    fechAnt = models.FloatField()
    capMerc = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)



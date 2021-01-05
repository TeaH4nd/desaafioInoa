from django.db import models

class Acao(models.Model):
    simbolo = models.CharField(max_length=10)
    
    def __str__(self):
        return self.simbolo

class Preco(models.Model):
    simbolo = models.ForeignKey(Acao, on_delete=models.CASCADE)
    preço = models.FloatField()
    data = models.DateField(auto_now_add=True)


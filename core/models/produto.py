from django.db import models
from django.utils import timezone

class Produto(models.Model):
    cliente = models.ForeignKey(
        'core.Cliente', 
        on_delete=models.CASCADE,
        related_name='produtos'
    )
    nome = models.CharField(max_length=255)
    concorrente = models.CharField(max_length=255)
    url = models.URLField(max_length=1000)
    plataforma = models.ForeignKey(
        'core.Plataforma', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='produtos'
    )
    grupo = models.ForeignKey(
        'core.Grupo', 
        on_delete=models.CASCADE,
        related_name='produtos'
    )
    data_criacao = models.DateTimeField(default=timezone.now)
    ultima_verificacao = models.DateTimeField(null=True, blank=True)
    posicao_fila = models.IntegerField(default=0)
    verificacao_manual = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        unique_together = ('cliente', 'nome', 'url')
    
    def __str__(self):
        return f"{self.nome} ({self.cliente})"
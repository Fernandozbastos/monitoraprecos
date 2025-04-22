from django.db import models
from django.utils import timezone

class HistoricoPreco(models.Model):
    produto = models.ForeignKey(
        'core.Produto', 
        on_delete=models.CASCADE,
        related_name='historico_precos'
    )
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=timezone.now)
    
    class Meta:
        ordering = ['-data']
        verbose_name = 'Histórico de Preço'
        verbose_name_plural = 'Histórico de Preços'
        # Índice para consultas otimizadas
        indexes = [
            models.Index(fields=['produto', 'data']),
        ]
    
    def __str__(self):
        return f"{self.produto} - R$ {self.preco} ({self.data})"
# core/models/cliente.py
from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return self.nome
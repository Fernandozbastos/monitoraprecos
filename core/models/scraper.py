from django.db import models
from django.utils import timezone

class Dominio(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    seletor_css = models.CharField(max_length=1000)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Domínio'
        verbose_name_plural = 'Domínios'
    
    def __str__(self):
        return self.nome

class Plataforma(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    seletor_css = models.CharField(max_length=1000)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
    
    def __str__(self):
        return self.nome
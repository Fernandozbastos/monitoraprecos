from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    tipo = models.CharField(
        max_length=20, 
        choices=[('admin', 'Administrador'), ('usuario', 'Usuário')],
        default='usuario'
    )
    cliente_atual = models.ForeignKey(
        'core.Cliente', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='usuarios_ativos'
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.username
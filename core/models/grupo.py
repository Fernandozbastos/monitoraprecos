from django.db import models
from django.utils import timezone

class Grupo(models.Model):
    id_grupo = models.CharField(max_length=255, unique=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    usuarios = models.ManyToManyField(
        'core.Usuario', 
        through='UsuarioGrupo',
        related_name='grupos'
    )
    clientes = models.ManyToManyField(
        'core.Cliente', 
        through='ClienteGrupo',
        related_name='grupos'
    )
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
    
    def __str__(self):
        return self.nome

# Tabelas de junção (modelos intermediários)
class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey('core.Usuario', on_delete=models.CASCADE)
    grupo = models.ForeignKey('core.Grupo', on_delete=models.CASCADE)
    data_associacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('usuario', 'grupo')

class ClienteGrupo(models.Model):
    cliente = models.ForeignKey('core.Cliente', on_delete=models.CASCADE)
    grupo = models.ForeignKey('core.Grupo', on_delete=models.CASCADE)
    data_associacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('cliente', 'grupo')
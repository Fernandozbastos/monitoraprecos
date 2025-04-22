from django.db import models
from django.utils import timezone

class Agendamento(models.Model):
    TIPO_CHOICES = [
        ('diario', 'Diário'),
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    dias = models.CharField(max_length=255, blank=True)  # Armazenado como string separada por vírgulas
    horario = models.TimeField()
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    ultima_execucao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
    
    def __str__(self):
        return f"{self.get_tipo_display()} às {self.horario}"
from django.db import models, transaction
from django.utils import timezone

class Produto(models.Model):
    TIPO_CHOICES = [
        ('cliente', 'Produto do Cliente'),
        ('concorrente', 'Produto de Concorrente'),
    ]
    
    cliente = models.ForeignKey(
        'core.Cliente', 
        on_delete=models.CASCADE,
        related_name='produtos'
    )
    nome = models.CharField(max_length=255)
    concorrente = models.CharField(max_length=255)
    url = models.URLField(max_length=1000)
    tipo_produto = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES,
        default='concorrente',
        verbose_name='Tipo do Produto'
    )
    preco_cliente = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True, 
        blank=True,
        verbose_name='Preço do Cliente'
    )
    produto_cliente = models.BooleanField(
        default=False,
        verbose_name='Produto Cliente Base',
        help_text='Marca este produto como o produto cliente base para comparações'
    )
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
    
    def get_menor_preco_concorrente(self):
        """Retorna o menor preço de concorrente para este produto."""
        from core.models import HistoricoPreco
        
        # Encontra produtos concorrentes com o mesmo nome (mesma categoria)
        produtos_concorrentes = Produto.objects.filter(
            cliente=self.cliente,
            nome=self.nome,
            tipo_produto='concorrente'
        ).exclude(id=self.id)
        
        if not produtos_concorrentes.exists():
            return None
            
        # Lista para armazenar os preços mais recentes
        precos_recentes = []
        
        # Para cada produto concorrente, pega o preço mais recente
        for produto in produtos_concorrentes:
            historico = HistoricoPreco.objects.filter(
                produto=produto
            ).order_by('-data').first()
            
            if historico:
                precos_recentes.append(historico.preco)
        
        # Se tiver preços, retorna o menor
        if precos_recentes:
            return min(precos_recentes)
        
        return None
        
    def get_produto_cliente_base(self):
        """Retorna o produto marcado como 'produto_cliente' com o mesmo nome."""
        return Produto.objects.filter(
            cliente=self.cliente,
            nome=self.nome,
            produto_cliente=True
        ).first()
    
    def calcular_diferenca_percentual(self):
        """Calcula a diferença percentual entre o preço do cliente e o menor preço concorrente."""
        if self.tipo_produto != 'cliente' or not self.preco_cliente:
            return None
            
        menor_preco = self.get_menor_preco_concorrente()
        if not menor_preco:
            return None
            
        # Diferença percentual (positiva se o cliente for mais caro)
        diferenca = ((self.preco_cliente - menor_preco) / menor_preco) * 100
        return round(diferenca, 1)  # Arredonda para 1 casa decimal
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que apenas um produto com o mesmo nome
        seja marcado como produto_cliente para o mesmo cliente.
        """
        # Se este produto está sendo marcado como produto_cliente
        if self.produto_cliente:
            # Se o tipo for concorrente, alterar para cliente
            if self.tipo_produto == 'concorrente':
                self.tipo_produto = 'cliente'
                
            # Desmarcar outros produtos com o mesmo nome
            with transaction.atomic():
                # Primeiro salvamos este produto para garantir que ele existe
                super().save(*args, **kwargs)
                
                # Depois desmarcamos outros produtos com o mesmo nome
                # Usamos a mesma conexão de transação
                Produto.objects.filter(
                    cliente=self.cliente,
                    nome=self.nome,
                    produto_cliente=True
                ).exclude(id=self.id).update(produto_cliente=False)
                
                # Não é necessário salvar novamente porque já salvamos acima
                return
        
        # Caso normal, sem produto_cliente=True
        super().save(*args, **kwargs)
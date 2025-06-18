from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.conf import settings

settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
}

from core.models import Cliente, Grupo, Plataforma, Produto, HistoricoPreco

class ProdutoModelTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome="Cliente Teste")
        self.grupo = Grupo.objects.create(id_grupo="g1", nome="Grupo 1")
        self.plataforma = Plataforma.objects.create(nome="Plataforma", seletor_css="div")

        self.prod_cliente = Produto.objects.create(
            cliente=self.cliente,
            nome="Produto",
            concorrente="Loja Cliente",
            url="http://cliente.com/prod",
            tipo_produto="cliente",
            preco_cliente=Decimal("20.00"),
            produto_cliente=True,
            grupo=self.grupo,
            plataforma=self.plataforma,
        )

        self.conc1 = Produto.objects.create(
            cliente=self.cliente,
            nome="Produto",
            concorrente="Concorrente 1",
            url="http://conc1.com/prod",
            tipo_produto="concorrente",
            grupo=self.grupo,
            plataforma=self.plataforma,
        )

        self.conc2 = Produto.objects.create(
            cliente=self.cliente,
            nome="Produto",
            concorrente="Concorrente 2",
            url="http://conc2.com/prod",
            tipo_produto="concorrente",
            grupo=self.grupo,
            plataforma=self.plataforma,
        )

        # Historico para concorrente 1
        HistoricoPreco.objects.create(
            produto=self.conc1,
            preco=Decimal("12.00"),
            data=timezone.now() - timezone.timedelta(days=2),
        )
        HistoricoPreco.objects.create(
            produto=self.conc1,
            preco=Decimal("10.00"),
            data=timezone.now() - timezone.timedelta(days=1),
        )

        # Historico para concorrente 2
        HistoricoPreco.objects.create(
            produto=self.conc2,
            preco=Decimal("15.00"),
            data=timezone.now() - timezone.timedelta(days=2),
        )
        HistoricoPreco.objects.create(
            produto=self.conc2,
            preco=Decimal("8.00"),
            data=timezone.now(),
        )

    def test_get_menor_preco_concorrente(self):
        menor_preco = self.prod_cliente.get_menor_preco_concorrente()
        self.assertEqual(menor_preco, Decimal("8.00"))

    def test_calcular_diferenca_percentual(self):
        resultado = self.prod_cliente.calcular_diferenca_percentual()
        esperado = round(((Decimal("20.00") - Decimal("8.00")) / Decimal("8.00")) * 100, 1)
        self.assertEqual(resultado, esperado)

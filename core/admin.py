from django.contrib import admin
from core.models import (
    Cliente, Usuario, Grupo, UsuarioGrupo, ClienteGrupo,
    Produto, HistoricoPreco, Dominio, Plataforma, Agendamento
)
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from scraper.tasks import verificar_preco
from django.utils.safestring import mark_safe



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_criacao')
    search_fields = ('nome',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo', 'cliente_atual')
    list_filter = ('tipo',)
    search_fields = ('username', 'email')

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id_grupo', 'data_criacao')
    search_fields = ('nome', 'id_grupo')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cliente', 'tipo_produto', 'preco_cliente', 'plataforma', 'ultima_verificacao', 'acao_verificar_preco')
    list_filter = ('tipo_produto', 'verificacao_manual', 'plataforma')
    search_fields = ('nome', 'url', 'concorrente')
    
    fieldsets = (
        (None, {
            'fields': ('cliente', 'nome', 'tipo_produto')
        }),
        ('Informações do Produto', {
            'fields': ('concorrente', 'url', 'plataforma', 'grupo')
        }),
        ('Preço Cliente', {
            'fields': ('preco_cliente',),
            'description': 'Defina o preço manualmente para produtos do cliente.'
        }),
        ('Configurações', {
            'fields': ('verificacao_manual', 'posicao_fila'),
            'classes': ('collapse',)
        })
    )

    def acao_verificar_preco(self, obj):
        return mark_safe(f'<a href="{obj.id}/verificar-preco/" class="button">Verificar Preço</a>')
    acao_verificar_preco.short_description = 'Verificar Preço'
    acao_verificar_preco.allow_tags = True  # Isso é obsoleto, mas mantido por compatibilidade
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/verificar-preco/', self.admin_site.admin_view(self.verificar_preco_view), name='produto-verificar-preco'),
        ]
        return custom_urls + urls
        
    def verificar_preco_view(self, request, object_id):
        try:
            produto = self.get_queryset(request).get(pk=object_id)
            task = verificar_preco.delay(produto.id)
            self.message_user(
                request, 
                f"Verificação de preço agendada para '{produto}'. Task ID: {task.id}", 
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(
                request,
                f"Erro ao agendar verificação: {str(e)}",
                messages.ERROR
            )
        return HttpResponseRedirect("../../")

@admin.register(HistoricoPreco)
class HistoricoPrecoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'preco', 'data')
    list_filter = ('data',)
    search_fields = ('produto__nome',)

@admin.register(Dominio)
class DominioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_criacao')
    search_fields = ('nome',)

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_criacao')
    search_fields = ('nome',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'horario', 'ativo', 'ultima_execucao')
    list_filter = ('tipo', 'ativo')

# Registrar modelos intermediários
admin.site.register(UsuarioGrupo)
admin.site.register(ClienteGrupo)
from django.contrib import admin
from core.models import (
    Cliente, Usuario, Grupo, UsuarioGrupo, ClienteGrupo,
    Produto, HistoricoPreco, Dominio, Plataforma, Agendamento
)

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
    list_display = ('nome', 'cliente', 'concorrente', 'plataforma', 'ultima_verificacao')
    list_filter = ('verificacao_manual', 'plataforma')
    search_fields = ('nome', 'url', 'concorrente')

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
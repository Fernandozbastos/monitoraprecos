# core/models/__init__.py
from .cliente import Cliente
from .usuario import Usuario
from .grupo import Grupo, UsuarioGrupo, ClienteGrupo
from .produto import Produto
from .historico import HistoricoPreco
from .scraper import Dominio, Plataforma
from .scheduler import Agendamento

__all__ = [
    'Cliente',
    'Usuario',
    'Grupo',
    'UsuarioGrupo',
    'ClienteGrupo',
    'Produto',
    'HistoricoPreco',
    'Dominio',
    'Plataforma',
    'Agendamento'
]
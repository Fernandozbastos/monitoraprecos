Desenvolvido por: Fernando Bastos
Bastin Marketing

# MonitoraPrecos

Um sistema web completo para monitoramento de preços online, construído com Django, Celery e Docker.

## Sobre o Projeto

O MonitoraPrecos é uma aplicação que permite monitorar automaticamente os preços de produtos em diferentes sites de e-commerce. O sistema rastreia os preços ao longo do tempo, permitindo aos usuários acompanhar alterações de preços e tomar decisões mais informadas.

## Características

- Monitoramento automático de preços em diversos sites
- Histórico completo de preços com visualização de tendências
- Sistema multi-cliente com gestão de usuários e permissões
- Processamento assíncrono com Celery e Redis
- Interface administrativa para gerenciamento de produtos e monitoramento
- Compatibilidade com plataformas ARM (Apple Silicon)

## Tecnologias

- **Backend**: Django + Django REST Framework
- **Banco de Dados**: PostgreSQL
- **Processamento Assíncrono**: Celery + Redis
- **Web Scraping**: BeautifulSoup e Playwright
- **Containerização**: Docker + Docker Compose

## Estrutura do Projeto

```
monitoraprecos/
├── core/                   # App principal com modelos e views
│   ├── management/         # Comandos personalizados
│   ├── models/             # Modelos do Django
│   ├── serializers/        # Serializers para a API REST
│   └── views/              # Views da API
├── scraper/                # Sistema de scraping
│   ├── services/           # Serviços de extração de dados
│   └── tasks.py            # Tarefas Celery
├── utils/                  # Utilitários
├── monitoraprecos/         # Configurações do projeto
├── docker-compose.yaml     # Configuração do Docker Compose
├── Dockerfile              # Configuração do Docker
└── requirements.txt        # Dependências Python
```

## Instalação e Configuração

### Pré-requisitos

- Docker
- Docker Compose

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/monitoraprecos.git
   cd monitoraprecos
   ```

2. Inicie os contêineres com Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Crie um superusuário para acessar o painel administrativo:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Acesse o painel administrativo em `http://localhost:8000/admin/`

## Uso

### Cadastro de Produtos para Monitoramento

1. Acesse o painel administrativo
2. Adicione uma Plataforma com o seletor CSS adequado
3. Adicione um Produto vinculado à Plataforma
4. Configure o agendamento de verificação

### Verificação Manual de Preços

```bash
docker-compose exec web python manage.py testar_scraper --id=ID_DO_PRODUTO
```

## Desenvolvimento

### Implementação Atual

- Sistema base com Django e PostgreSQL
- Estrutura de modelos para Clientes, Produtos, Grupos e Histórico
- Sistema de scraping com BeautifulSoup e Playwright
- API REST básica com Django REST Framework
- Processamento assíncrono com Celery
- Compatibilidade com plataformas ARM (Apple Silicon)

### Próximos Passos

- Implementação de frontend em React
- Dashboards com gráficos de evolução de preços
- Sistema de alertas para mudanças de preços
- Testes automatizados
- Otimizações de desempenho para grandes volumes de dados

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT.
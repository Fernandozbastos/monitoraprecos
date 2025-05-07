# Estágio de compilação para reduzir o tamanho da imagem final
FROM python:3.9-slim AS builder

# Variáveis de ambiente essenciais
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Instalar apenas dependências necessárias para compilação
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        wget \
        gnupg \
        curl \
        python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requisitos em uma camada separada
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels playwright==1.41.1

# Estágio final de produção
FROM python:3.9-slim

# Mesmo usuário UID/GID em todas as instancias do contêiner para consistência
ARG APP_USER=appuser
ARG APP_GROUP=appgroup
ARG APP_UID=1000
ARG APP_GID=1000

# Adicionar variáveis de ambiente para produção
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_ENVIRONMENT=production \
    DJANGO_DEBUG=False \
    PATH="/home/${APP_USER}/.local/bin:${PATH}" \
    PYTHONPATH="/app:${PYTHONPATH}" \
    # Manter 1 worker por núcleo + 1
    WEB_CONCURRENCY=4 \
    # Porta interna para o servidor web
    PORT=8000

# Criar usuário não-root com UID/GID explícitos para segurança
RUN groupadd -g ${APP_GID} ${APP_GROUP} \
    && useradd -u ${APP_UID} -g ${APP_GROUP} -s /bin/bash -m ${APP_USER}

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        wget \
        ca-certificates \
        xvfb \
        procps \
        # Dependências para Playwright
        libnss3 \
        libnspr4 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdrm2 \
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        libgbm1 \
        libasound2 \
        libpangocairo-1.0-0 \
        libpango-1.0-0 \
        # Utilitários para monitoramento
        curl \
        dnsutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar as dependências Python compiladas da imagem builder
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
    && playwright install --with-deps chromium

# Criar estrutura de diretórios com permissões adequadas
RUN mkdir -p /app/logs /app/staticfiles /app/media \
    && chown -R ${APP_USER}:${APP_GROUP} /app

# Copiar código-fonte
COPY --chown=${APP_USER}:${APP_GROUP} . /app/

# Criar script de inicialização com verificações de saúde e migrations
RUN echo '#!/bin/bash \n\
set -e \n\
echo "Verificando conexão com PostgreSQL..." \n\
until pg_isready -h ${DB_HOST:-db} -p ${DB_PORT:-5432} -U ${DB_USER:-monitoraprecos}; do \n\
  echo "Banco de dados não está pronto. Aguardando..." \n\
  sleep 2 \n\
done \n\
echo "Banco de dados conectado." \n\
\n\
echo "Aplicando migrações..." \n\
python manage.py migrate --no-input \n\
\n\
echo "Coletando arquivos estáticos..." \n\
python manage.py collectstatic --no-input \n\
\n\
echo "Inicializando servidor web..." \n\
exec gunicorn monitoraprecos.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers ${WEB_CONCURRENCY} \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --max-requests 1000 \
    --max-requests-jitter 50 \
' > /app/entrypoint.sh

# Tornar o script executável com as permissões adequadas
RUN chmod +x /app/entrypoint.sh \
    && chmod +x /app/manage.py

# Alternar para usuário não-root para segurança
USER ${APP_USER}

# Porta para expor
EXPOSE ${PORT}

# Adicionar healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health/ || exit 1

# Definir o ponto de entrada para usar nosso script de inicialização
ENTRYPOINT ["/app/entrypoint.sh"]
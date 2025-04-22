FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instalar pacotes do sistema necessários
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        wget \
        gnupg \
        unzip \
        curl \
        ca-certificates \
        xvfb \
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome (para Selenium)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório para logs e diretório para WebDriver Manager
RUN mkdir -p /app/logs && chmod 777 /app/logs \
    && mkdir -p /root/.wdm/drivers/ && chmod 777 /root/.wdm/drivers/

# Instalar dependências Python
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    # Instalar Playwright (substituto do Selenium para ARM)
    && pip install playwright==1.41.1 \
    && playwright install --with-deps chromium

# Copiar o projeto
COPY . /app/

# Configurar permissões
RUN chmod +x /app/manage.py

# Porta para expor
EXPOSE 8000

# Comando para executar
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
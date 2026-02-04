<<<<<<< HEAD

=======
# Dockerfile
FROM python:3.11-slim

# Prevenir Python de escrever arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevenir Python de fazer buffer de stdout e stderr
ENV PYTHONUNBUFFERED=1
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)

# Instalar dependências do sistema necessárias para pillow
RUN apt-get update && apt-get install -y \
<<<<<<< HEAD
    libjpeg-dev \
    zlib1g-dev \
    build-essential \
=======
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

<<<<<<< HEAD
<<<<<<< HEAD
# Copiar código da aplicação
COPY --chown=django:django . /app/

# Copiar e configurar entrypoint (como root para poder mudar permissões)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && \
    chown django:django /app/entrypoint.sh

# Mudar para usuário não-root
USER django
=======
# Copiar projeto
COPY . /app/

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/media /app/staticfiles
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
=======
# Copiar projeto
COPY . /app/

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/media /app/staticfiles
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)

# Expor porta
EXPOSE 8000

<<<<<<< HEAD
<<<<<<< HEAD
# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

=======
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


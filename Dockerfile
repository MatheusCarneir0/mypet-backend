
# Instalar dependências do sistema

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências Python
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

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

# Expor porta
EXPOSE 8000

<<<<<<< HEAD
# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

=======
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


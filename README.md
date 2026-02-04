# MyPet - Sistema de Gerenciamento para Pet Shop

Sistema completo de gerenciamento para a FarmaVet - Pet Shop em Boa Viagem, CE.

## 🚀 Tecnologias

- Python 3.11+
- Django 5.0
- Django REST Framework 3.14
- PostgreSQL 15
- Redis
- Celery
- Docker & Docker Compose

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git

## 🔧 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/mypet-backend.git
cd mypet-backend
```

<<<<<<< HEAD
2. **Crie o arquivo `.env`** baseado no `.env.example`:
=======
# FarmaVet - Sistema de Gerenciamento para Pet Shop

Sistema completo de gerenciamento FarmaVet para pet shop e clinica veterinaria.

## 🚀 Tecnologias

- Python 3.11+
- Django 4.2.11
- Django REST Framework 3.14
- PostgreSQL 15
- Redis
- Celery
- Docker & Docker Compose

## 🧩 Modelagem de Usuários (Implementação Atual)

- Usuario customizado (`AUTH_USER_MODEL`).
- Perfis de negócio `Cliente` e `Funcionario` com relacionamento 1:1 para `Usuario`.
- Autorização via grupos do Django (`CLIENTE`, `FUNCIONARIO`, `ADMINISTRADOR`).

Esse é o comportamento real do sistema em produção e deve ser usado como referência
para documentação e diagramas técnicos.

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git

## 🔧 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/mypet-backend.git
cd mypet-backend
```

2. Copie o arquivo de ambiente:

>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
=======
2. Copie o arquivo de ambiente:

>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
```bash
cp .env.example .env
```

<<<<<<< HEAD
<<<<<<< HEAD
3. **Edite o arquivo `.env`** e configure as variáveis necessárias:
```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DB_PASSWORD=postgres
# ... outras variáveis
```
=======
3. Configure as variáveis de ambiente no arquivo `.env`
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)

4. Suba os containers:

```bash
docker-compose up -d
```

5. Execute as migrações:

```bash
docker-compose exec web python manage.py migrate
```

6. Popule o banco com dados iniciais:

```bash
docker-compose exec web python scripts/seed_data.py
```

7. Acesse:

- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- Docs: http://localhost:8000/api/docs/

## 🧪 Testes

```bash
docker-compose exec web python manage.py test
```

## 📖 Documentação da API

Acesse: http://localhost:8000/api/docs/

## 👥 Equipe

- Andrey Victor - Gerente de Projeto
- Larissa Vieira - Analista de Sistemas
- Jhonata Vieira - Frontend Developer
- Matheus Cavalcante - Backend Developer
- Michel Júnior - QA / Tester

## 📄 Licença

<<<<<<< HEAD
Este projeto é privado e proprietário.

## 👥 Contribuição

Este é um projeto interno. Para contribuições, entre em contato com a equipe de desenvolvimento.
=======
3. Configure as variáveis de ambiente no arquivo `.env`

4. Suba os containers:

```bash
docker-compose up -d
```

5. Execute as migrações:

```bash
docker-compose exec web python manage.py migrate
```

6. Popule o banco com dados iniciais:

```bash
docker-compose exec web python scripts/seed_data.py
```

7. Acesse:

- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- Docs: http://localhost:8000/api/docs/

## 🧪 Testes

```bash
docker-compose exec web python manage.py test
```

## 📖 Documentação da API

Acesse: http://localhost:8000/api/docs/

## 👥 Equipe

- Andrey Victor - Gerente de Projeto
- Larissa Vieira - Analista de Sistemas
- Jhonata Vieira - Frontend Developer
- Matheus Cavalcante - Backend Developer
- Michel Júnior - QA / Tester

## 📄 Licença

Este projeto é privado e pertence ao IFCE Campus Boa Viagem.
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
=======
Este projeto é privado e pertence ao IFCE Campus Boa Viagem.
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


# 🎬 Biso API Test

API RESTful para gerenciamento de filmes, usuários e sistema de recomendações personalizadas, desenvolvida com FastAPI e SQLAlchemy.

## Funcionalidades

- **Usuários**: Cadastro e gerenciamento de usuários.
- **Filmes**: Cadastro de filmes com informações como título, gênero e diretor.
- **Avaliações**: Usuários podem avaliar filmes com pontuações de 1 a 5.
- **Recomendações**: Sistema que sugere filmes com base nas preferências e avaliações dos usuários.

## Endpoints Principais

- `GET /filmes`: Lista todos os filmes disponíveis.
- `GET /filmes/{usuario_id}/recomendacoes`: Retorna recomendações personalizadas para o usuário especificado.

## Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/) para migrações de banco de dados
- [Pytest](https://docs.pytest.org/) para testes automatizados

## Configuração e Execução

1. **Clone o repositório:**

```bash
  git clone https://github.com/henriquealvesL/biso-api-test.git
  cd biso-api-test
```

2. **Criar o ambiente virtual:**

```bash
  python3 -m venv venv
  source venv/bin/activate
```

3. **Instalar as dependências:**

```bash
  pip install -r requirements.txt
```

4. **Banco de dados:**

Rode a migração para criar as tabelas com o seguinte comando:

```bash
  alembic upgrade head
```

5. **Rodar a aplicação:**

   Na pasta raíz do projeto rode:

```bash
  fastapi dev src/main.py
```

6. **Executar testes:**

   Na pasta raíz do projeto rode:

```bash
  ➜ pytest -s --cov=src --cov-report=term-missing
```

O comando acima também exibirá a cobertura dos testes, indicando quais partes do código foram testadas e quais ainda precisam de cobertura.

## Funcionamento do recomendador

A rota `/filmes/{user_id}/recomendacoes` considera os seguintes fatores para sugerir filmes:

- Gênero e diretor dos filmes já avaliados positivamente pelo usuário (Nota >= 4).
- Filmes ainda não assistidos por ele.
- O cálculo de relevância é baseado na similaridade com as preferências anteriores do usuário, considerando diretor e gênero. Isso gera uma pontuação de recomendação, ordenando os filmes do mais compatível ao menos compatível.

## Documentação da API

A documentação interativa da API está disponível através do **Swagger UI** e do **ReDoc**, permitindo explorar todos os endpoints com exemplos de requisições e respostas.

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

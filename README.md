# Teste Técnico Workalove: API iChef

Este projeto descreve uma API de compartilhamento de receitas entre chefs e cozinheiros amadores.

Com esta API, você pode:

- Cadastrar-se na aplicação (como usuário comum ou chef, e também com poderes administrativos da plataforma);
- Realizar login (via autenticação JWT stateless);
- Visualizar um ou mais usuários (com paginação das informações);
- Visualizar um ou mais usuários que sejam chefs (com paginação das informações);
- Remover usuários (apenas você mesmo ou, se você for um administrador, qualquer usuário);
  - *Nota:* Isso também remove as receitas de um usuário;
- Cadastrar receitas (apenas se você for um chef);
- Visualizar todas as receitas (com paginação das informações);
- Pesquisar uma receita:
  - Por ID do chef;
  - Por texto (título ou corpo da receita, independente de onde estiver na mesma);
  - Por ID do chef e por texto também.
- Remover uma receita (apenas se você for o dono da receita ou, se você for um administrador, qualquer receita).

## Requisitos

- Ambiente Linux ou PowerShell do Windows;
- GNU Make (opcional);
- Python 3.11 ou superior;
- Docker instalado (de preferência com o usuário atual no grupo `docker`); e
- Docker Compose (de preferência, o plugin oficial).

## Descrição dos diretórios do projeto

Abaixo há uma descrição rápida dos diretórios e arquivos principais do projeto. Para mais informações, veja a documentação da solução.

- `alembic` e `alembic.ini`: Configurações e arquivos de migrations.
- `auth`: Middlewares de autenticação.
- `config`: Módulo relacionado a leitura de configurações de arquivos `.env` e/ou variáveis de ambiente.
- `controllers`: Módulo relacionado a controles de regras de negócio da aplicação.
- `db`: Módulo de configuração de conexão e persistência genérica com banco de dados.
- `endpoints`: Reúne os endpoints REST da aplicação.
- `model`: Reúne os models, portanto sendo diretamente relacionado à persistência no banco de dados.
- `repository`: Reúne estruturas relacionadas a consulta e armazenamento no banco de dados, como queries realizadas via ORM.
- `schemas`: Reúne estruturas representacionais (DTOs) para envio e recebimento na API, que podem ser mapeadas para models, dependendo da situação.
- `tests`: Arquivos relacionados a testes.
- `util`: Utilitários variados, como funções de encriptação.
- `main.py`: Ponto de entrada principal do projeto.

Há também outros arquivos utilitários como:

- `.github`: Diretório de definição de workflows e automação de testes do Github Actions.
- `LICENSE`: Arquivo de licenciamento da aplicação.
- `Makefile`: Script do GNU Make para facilitar alguns processos.
- `README.md`: Este documento.
- `docker-compose-dev.yml`: Configuração do Docker Compose para ambiente local de desenvolvimento.
- `docker-compose.yml`: Configuração do Docker Compose que também cria um contêiner para a aplicação. Ideal para execução sem configuração extra.
- `.dockerignore`: Similar ao `.gitignore`, mas para o contexto a ser transferido para a imagem Docker do projeto.
- `requirements.txt`: Arquivo para instalação de bibliotecas do ambiente Python via `pip`.

## Executando o projeto com Docker Compose

Antes de mais nada, você pode testar o projeto facilmente usando Docker. Esse processo criará uma imagem com a aplicação executando em Python 3.11, com um banco de dados já configurado e com variáveis de ambiente.

Para iniciar o projeto com Docker Compose, navegue até a raiz deste projeto e use o comando:

```bash
docker compose up
```

Interessante ressaltar que a execução desse comando via Docker Compose expõe o PostgreSQL na porta `5432` e a API do projeto na porta `8000`, por padrão. Os dados do banco de dados ficarão armazenados em um volume virtual criado com Docker.

Após a execução, caso você queira remover todos os itens que o Docker criar (incluindo volumes), use o seguinte comando:

```bash
docker compose down -v
```

Para mais informações, veja a [documentação do Docker Compose](https://docs.docker.com/compose/).

## Executando o projeto manualmente

### Configurando o VirtualEnv

Para este projeto, recomenda-se o uso de VirtualEnv. Para tanto, garanta que seu Python da máquina local esteja atualizado, vá até a raiz do repositório e execute os comandos a seguir:

```bash
python3 -m venv env
source env/bin/activate
```

Ou, no Windows, você poderá executar:

```ps1
python3 -m venv env
env\bin\activate.ps1
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

### Instalando utilitários

Para testar o projeto e executar migrations, você precisará instalar o Pytest e o Alembic:

```bash
pip install pytest alembic
```

Caso você possua alguma dessas ferramentas instalada globalmente na sua máquina, você pode precisar recarregar o VirtualEnv:

```bash
source env/bin/activate
```

Ou, no Windows:

```ps1
env\bin\activate.ps1
```

### Configurando as variáveis de ambiente (`.env`)

Copie o arquivo `.env.example` para `.env`, no mesmo diretório. Você poderá alterar as variáveis de ambiente a gosto, mas lembre-se de que elas poderão influenciar nos próximos passos.

Uma das variáveis precisa necessariamente ser alterada `JWT_SECRET`. Você poderá gerar um novo _secret_ usando o código em Python a seguir, pelo console:

```python
import os
import binascii

binascii.hexlify(os.urandom(24))
```

### Configurando o banco de dados

Caso você esteja executando o projeto pela primeira vez, é necessário configurar o banco de dados.

Navegue até o diretório-base deste projeto, e use os comandos para iniciar o PostgreSQL 16.1 e o PgAdmin 4 usando Docker:

```bash
make startdb

# Ou...
docker compose -f docker-compose-dev.yml up -d
```

Isso iniciará o PostgreSQL 16.1 com um banco de dados chamado `teste-workalove`.

Você poderá aguardar até que o PgAdmin 4 fique pronto e acessá-lo na porta `5433` do seu computador, ou conectar à porta `5432` com o gerenciador de banco de dados do seu gosto.

> _NOTA:_ O PgAdmin4 pode ser acessado com usuário 'admin@admin.com' e senha 'admin'.

> _NOTA:_ O usuário e a senha do banco de dados são iguais, sendo seu valor 'postgres'.

> _NOTA:_ Se você estiver usando o PgAdmin4, certifique-se de conectar ao banco de dados usando o host e a porta `postgresql:5432`, já que o banco de dados estará acessível dentro da rede bridge criada pelo Docker.

Finalmente, execute as migrations no banco de dados, usando Alembic:

```bash
make migrate

# Ou...
alembic upgrade head
```

> _NOTA:_ O arquivo `alembic/env.py` foi modificado para levar em consideração os models, configurações e variávels de ambiente do projeto. Caso você crie algum model novo, certifique-se de importá-lo em `model/__init__.py`.

> _NOTA:_ Você poderá encontrar outros comandos e configurações analisando os arquivos `Makefile`, `docker-compose-dev.yml` e `.env`.

### Executando a aplicação

Para iniciar a aplicação em modo debug, posto que o banco de dados esteja em execução e as migrations tenham sido executadas, você poderá usar o seguinte comando:

```bash
make run

# Ou...
uvicorn main:app --reload
```

Caso você queira executar a aplicação sem utilizar o `uvicorn` diretamente, e sem recarregamento após alterar algum arquivo, basta executar diretamente o arquivo `main.py`:

```bash
python3 main.py
```

## Uso do projeto

Este projeto trata-se de uma API REST, cuja autenticação se dá via Bearer Token JWT.

A documentação dos _endpoints_ existentes pode ser vista ao acessar as URLs:

- Interface Swagger (interativa): `http://localhost:8000/docs`;
- Interface Redoc (apenas documentação): `http://localhost:8000/redoc`.

É possível ajustar a porta de execução da aplicação através das variáveis de ambiente. Para mais informações, veja o arquivo `.env.example` já anteriormente mencionado.

### Usuário administrador padrão

Após a execução das migrations, será criado um administrador padrão com as seguintes características:

```bash
Nome: Admin
E-mail: admin@admin.com
Senha: admin
Chef: Não
Admin: Sim
```

Você poderá utilizar este usuário para realizar testes e configuração inicial.

**Veja que este usuário padrão não é um chef, e portanto, não pode cadastrar receitas.** Para cadastrar uma receita, será necessário cadastrar um chef através de uma requisição `POST` em `/users` (veja o Swagger ou o ReDoc para mais detalhes).

Caso você não precise mais desse usuário, você poderá realizar login usando o mesmo (ou qualquer outro administrador) e removê-lo através da própria API. **É altamente recomendado fazer isso em cenários de produção o quanto antes.**

## Testes

Esta aplicação possui testes E2E de API que testam requisições e retorno dentro da mesma. Para testar, certifique-se de que:

- O PostgreSQL esteja em execução;
- O banco de dados esteja atualizado;
- As migrations tenham sido executadas;
- O banco de dados esteja sem informações; e
- O Pytest esteja instalado.

Para executar os testes, basta executar o Pytest:

```bash
pytest
```

> _NOTA:_ Para garantir que você esteja executando o Pytest do VirtualEnv, verifique a localização do binário usando `which pytest` no Linux.

> _NOTA:_ Este repositório também possui testes automatizados via GitHub Actions. Os testes podem ser executados manualmente, após um Pull Request ou após um commit em qualquer branch.

## Roadmap do projeto

- [x] Pesquisa de receitas por texto e por Chef
- [x] Updates das entidades
- [x] Testes básicos (pt. 1)
  - [x] Automação de testes com GitHub Actions
  - [x] Rota ping
  - [x] Criar chef
  - [x] Criar admin
  - [x] Recuperar listas de usuários
  - [x] Recuperar usuário por ID
  - [x] Recuperar usuário por e-mail
  - [x] Atualizar usuário
- [x] Reorganizar arquivos avulsos
- [x] Instruções de instalação Pytest / Alembic
- [x] Controllers entre endpoints e repositórios
  - [x] Controller de usuários
  - [x] Controller de receitas
- [x] Autenticação
  - [x] Autenticação via JWT
  - [x] Criação de receita através do usuário da sessão atual
  - [x] Admin criado na primeira execução
  - [x] Adicionar testes de autenticação
  - [x] Atualizar testes para usar autenticação
  - [x] Permitir alterações quando o usuário é admin
  - [x] Adicionar rota específica de criação de admins (acessível a admins)
- [x] Deletes das entidades
  - [x] Remoção de usuários
	- [x] Documentação para remoção do usuário `admin@admin.com`
  - [x] Remoção de receitas
- [ ] Testes (pt. 2)
  - [x] Remover usuário
  - [x] Criar receita
  - [x] Pesquisar receitas por chef
  - [x] Pesquisar receitas por texto
  - [x] Pesquisar receitas por chef e texto
  - [ ] Atualizar receita
  - [ ] Remover receita
- [x] Documentação
  - [x] Ajustar retornos de rotas no Swagger
  - [x] Ajustar nome da API no Swagger
- [x] Conteinerização
  - [x] Dockerfile e .dockerignore para a aplicação
  - [x] Arquivo Docker Compose para executar localmente
  - [x] Documentação de execução com Docker

## Referências

- [Guia de usuário do FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [Documentação do Pydantic](https://docs.pydantic.dev/latest/)
- [Securing FastAPI with JWT Token-based Authentication](https://testdriven.io/blog/fastapi-jwt-auth/)

## Licenciamento

Este código é licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

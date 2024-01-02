# Teste Técnico Workalove

## Requisitos

- Ambiente Linux ou PowerShell do Windows;
- GNU Make (opcional);
- Python 3.11 ou superior;
- Docker instalado (de preferência com o usuário atual no grupo `docker`).

## Descrição dos diretórios do projeto

Abaixo há uma descrição rápida dos diretórios e arquivos principais do projeto. Para mais informações, veja a documentação da solução.

- `alembic` e `alembic.ini`: Configurações e arquivos de migrations.
- `config`: Módulo relacionado a leitura de configurações de arquivos `.env` e/ou variáveis de ambiente.
- `controllers`: Módulo relacionado a controles de regras de negócio da aplicação.
- `endpoints`: Reúne os endpoints REST da aplicação.
- `model`: Reúne os models, portanto sendo diretamente relacionado à persistência no banco de dados.
- `repository`: Reúne estruturas relacionadas a consulta e armazenamento no banco de dados, como queries realizadas via ORM.
- `schemas`: Reúne estruturas representacionais (DTOs) para envio e recebimento na API, que podem ser mapeadas para models, dependendo da situação.
- `util`: Utilitários variados, como funções de encriptação.
- `tests`: Módulo e arquivos relacionados a testes.
- `db`: Módulo de configuração de conexão e persistência genérica com banco de dados.
- `main.py`: Ponto de entrada principal do projeto.

## Executando o projeto

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

### Instalando dependências

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

### Configurando o banco de dados

Caso você esteja executando o projeto pela primeira vez, é necessário configurar o banco de dados.

Navegue até o diretório-base deste projeto, e use os comandos para iniciar o PostgreSQL 16.1 e o PgAdmin 4 usando Docker:

```bash
make startdb

# Ou...
docker compose -f docker-compose-dev.yml up -d
```

Você poderá aguardar até que o PgAdmin 4 fique pronto e acessá-lo na porta `5433` do seu computador, ou conectar à porta `5432` com o gerenciador de banco de dados do seu gosto.

> O PgAdmin4 pode ser acessado com usuário 'admin@admin.com' e senha 'admin'.
>
> O usuário e a senha do banco de dados são iguais, sendo seu valor 'postgres'.
>
> Se você estiver usando o PgAdmin4, certifique-se de conectar ao banco de dados usando o host e a porta `postgresql:5432`, já que o banco de dados estará acessível dentro da rede bridge criada pelo Docker.

Em seguida, copie o arquivo `.env.example` para `.env`, no mesmo diretório.

No PgAdmin4 ou similar, Crie um banco de dados chamado `teste-workalove`, ou um outro nome de acordo com o arquivo `.env`.

Finalmente, execute as migrations no banco de dados, usando Alembic:

```bash
make migrate

# Ou...
alembic upgrade head
```

> O arquivo `alembic/env.py` foi modificado para levar em consideração os models, configurações e variávels de ambiente do projeto. Caso você crie algum model novo, certifique-se de importá-lo em `model/__init__.py`.
>
> Além disso, você poderá encontrar outros comandos e configurações analisando os arquivos `Makefile`, `docker-compose-dev.yml` e `.env`.

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

## Testes

Esta aplicação possui testes E2E de API que testam requisições e retorno dentro da mesma. Para testar, certifique-se de que a mesma esteja em 

## Licenciamento

Este código é licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Roadmap do projeto

- [x] Pesquisa de receitas por texto e por Chef
- [x] Updates das entidades
- [x] Testes básicos e de usuário (pt. 1)
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
- [ ] Controllers entre endpoints e repositórios
  - [ ] Controller de usuários
  - [ ] Controller de receitas
- [ ] Autenticação
  - [ ] Admin criado na primeira execução
- [ ] Testes de receitas (pt. 1)
  - [ ] Criar receita
  - [ ] Atualizar receita
  - [ ] Pesquisar receitas por chef
  - [ ] Pesquisar receitas por texto
  - [ ] Pesquisar receitas por chef e texto
- [ ] Deletes das entidades
  - [ ] Desativação de usuários
  - [ ] Remoção de receitas
- [ ] Testes pt. 2
  - [ ] Paginação de listagem
  - [ ] Desativar usuário
  - [ ] Remover usuário
  - [ ] Deletar receita
- [ ] Documentação




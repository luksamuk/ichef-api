# teste-tecnico-workalove

## Requisitos

- Um ambiente Linux-like;
- GNU Make (opcional);
- Python 3.11 ou superior;
- Docker instalado (de preferência com o usuário atual no grupo `docker`).

## Executando o projeto

### Configurando o VirtualEnv

Para este projeto, recomenda-se o uso de VirtualEnv. Para tanto, garanta que seu Python da máquina local esteja atualizado, vá até a raiz do repositório e execute os comandos a seguir:

```bash
python3 -m virtualenv env
source env/bin/activate
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
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

Finalmente, execute as migrations no banco de dados:

```bash
make migrate

# Ou...
python manage.py migrate
```

> Você poderá encontrar outros comandos e configurações analisando os arquivos `Makefile`, `docker-compose-dev.yml` e `.env`.

### Criando um usuário `admin`

Após a configuração do banco de dados, você poderá criar um usuário `admin` usando um comando como a seguir:

```bash
python manage.py createsuperuser --username admin --email admin@admin.com
```

No prompt que aparece, digite a senha do usuário que será criado. Esse usuário será importante para gerenciar outros usuários na aplicação.

## Executando a aplicação

### Usuários




## Licenciamento

Este código é licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

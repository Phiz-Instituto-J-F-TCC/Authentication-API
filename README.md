# 🔐 Phiz Authentication API

> **API de autenticação para vinculação de contas Phiz via e-mail** — Projeto de TCC do Instituto Germinare.

Uma API REST construída com **FastAPI** que implementa um fluxo seguro de autenticação por e-mail para vincular o Phiz ID à conta do aluno no sistema acadêmico.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Fluxo de Autenticação](#-fluxo-de-autenticação)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
  - [Rodando Localmente](#-rodando-localmente)
  - [Rodando com Docker](#-rodando-com-docker)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Banco de Dados](#-banco-de-dados)
- [Endpoints da API](#-endpoints-da-api)
- [Documentação Interativa](#-documentação-interativa)
- [Deploy](#-deploy)
- [Licença](#-licença)

---

## 🎯 Visão Geral

A **Phiz Authentication API** vincula o Phiz ID de um aluno à sua conta institucional de forma segura. O MiniApp envia apenas uma credencial temporária emitida por `pz.login`; a API deve trocá-la pelo Phiz ID exclusivamente no servidor, por meio da integração oficial do Phiz. O fluxo usa **verificação por e-mail** com tokens temporários, garantindo que apenas o proprietário do e-mail cadastrado possa concluir a vinculação.

---

## 🔄 Fluxo de Autenticação

```
┌─────────────┐     POST /authenticate      ┌──────────────┐
│  App Phiz   │ ──────────────────────────── │   API        │
│  (Cliente)  │ { email, phiz_login_code }   │   FastAPI    │
└─────────────┘                              └──────┬───────┘
                                                    │
                                          1. Valida se o email
                                             existe na tabela Aluno
                                                    │
                                          2. Troca a credencial temporária
                                             pelo Phiz ID no servidor
                                                    │
                                          3. Gera token seguro
                                             (secrets.token_urlsafe)
                                                    │
                                          4. Salva Phiz ID e token no banco
                                             (expira em 30 min)
                                                    │
                                          5. Envia e-mail com
                                             link de confirmação
                                                    │
                                                    ▼
┌─────────────┐     GET /finish_authentication?token=xxx
│   Aluno     │ ──────────────────────────────────────────┐
│  (E-mail)   │   Clica no link recebido                  │
└─────────────┘                                           ▼
                                               ┌──────────────┐
                                               │   API        │
                                               │   FastAPI    │
                                               └──────┬───────┘
                                                      │
                                            6. Valida token:
                                               - Existe?
                                               - Já foi usado?
                                               - Expirou?
                                                      │
                                            7. Atualiza phiz_id
                                               na tabela Aluno
                                                      │
                                            8. Marca token como
                                               utilizado
                                                      │
                                                      ▼
                                            9. Retorna página HTML
                                               de sucesso ou erro
```

---

## 🛠 Tecnologias

| Tecnologia | Descrição |
|---|---|
| **Python 3.12** | Linguagem principal |
| **FastAPI** | Framework web assíncrono de alta performance |
| **Uvicorn** | Servidor ASGI para rodar a aplicação |
| **PostgreSQL** | Banco de dados relacional (hospedado no Neon) |
| **psycopg2** | Driver PostgreSQL para Python |
| **Pydantic** | Validação de dados e schemas |
| **python-dotenv** | Gerenciamento de variáveis de ambiente |
| **Docker** | Containerização da aplicação |
| **Koyeb** | Plataforma de deploy em produção |

---

## 📁 Estrutura do Projeto

```
Authentication-API/
├── app/
│   ├── __init__.py              # Inicialização do pacote app
│   ├── config.py                # Configurações e variáveis de ambiente
│   ├── database.py              # Conexão com PostgreSQL
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── auth_controller.py   # Rotas/endpoints da API
│   ├── models/
│   │   ├── __init__.py
│   │   └── token_model.py       # Operações no banco (queries SQL)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── auth_schema.py       # Schemas Pydantic (validação de entrada)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Lógica de negócio da autenticação
│   │   └── email_service.py     # Envio de e-mails via SMTP (Outlook)
│   └── views/
│       ├── __init__.py
│       └── templates.py         # Templates HTML (sucesso/erro)
├── main.py                      # Factory da aplicação FastAPI
├── run.py                       # Script para rodar localmente com reload
├── send_email.py                # Utilitário standalone de envio de e-mail
├── dataabase.sql                # Schema completo do banco de dados
├── migration_auth_token.sql     # Migration da tabela Token_Autenticacao
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Configuração Docker para deploy
├── .dockerignore                # Arquivos ignorados pelo Docker
├── .env                         # Variáveis de ambiente (NÃO commitar)
├── .gitignore                   # Arquivos ignorados pelo Git
└── LICENSE                      # Licença MIT
```

---

## ✅ Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- **Python 3.12+** — [Download](https://www.python.org/downloads/)
- **pip** — gerenciador de pacotes do Python (incluso no Python)
- **PostgreSQL** — banco de dados (ou usar o [Neon](https://neon.tech/) hospedado)
- **Docker** _(opcional)_ — [Download](https://www.docker.com/products/docker-desktop/)
- **Git** — [Download](https://git-scm.com/downloads)

---

## 🚀 Instalação e Execução

### 💻 Rodando Localmente

#### 1. Clone o repositório

```bash
git clone https://github.com/Phiz-Instituto-J-F-TCC/Authentication-API.git
cd Authentication-API
```

#### 2. Crie e ative um ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (veja a seção [Variáveis de Ambiente](#-variáveis-de-ambiente)):

```env
FROM_ADDRESS=seu-email@outlook.com
FROM_PASSWORD=sua-senha
DATABASE_URL=postgresql://usuario:senha@host:5432/nome_do_banco?sslmode=require
BASE_URL=http://localhost:8000
```

#### 5. Configure o banco de dados

Execute os scripts SQL no seu banco PostgreSQL, **nesta ordem**:

```bash
# 1. Criar todas as tabelas e relacionamentos
psql -U seu_usuario -d seu_banco -f dataabase.sql

# 2. Criar a tabela de tokens de autenticação
psql -U seu_usuario -d seu_banco -f migration_auth_token.sql
```

> **💡 Dica:** Se estiver usando o [Neon](https://neon.tech/), você pode executar os scripts SQL diretamente no console web.

#### 6. Rode a aplicação

```bash
python run.py
```

A API estará disponível em: **http://localhost:8000**

> Alternativamente, você pode rodar diretamente com o Uvicorn:
> ```bash
> uvicorn main:app --host 0.0.0.0 --port 8000 --reload
> ```

---

### 🐳 Rodando com Docker

#### 1. Build da imagem

```bash
docker build -t phiz-auth-api .
```

#### 2. Execute o container

```bash
docker run -d \
  --name phiz-auth \
  -p 8000:8000 \
  -e FROM_ADDRESS=seu-email@outlook.com \
  -e FROM_PASSWORD=sua-senha \
  -e DATABASE_URL=postgresql://usuario:senha@host:5432/nome_do_banco?sslmode=require \
  -e BASE_URL=http://localhost:8000 \
  phiz-auth-api
```

Ou usando um arquivo `.env`:

```bash
docker run -d \
  --name phiz-auth \
  -p 8000:8000 \
  --env-file .env \
  phiz-auth-api
```

#### 3. Verifique se está rodando

```bash
docker ps
docker logs phiz-auth
```

A API estará disponível em: **http://localhost:8000**

---

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

| Variável | Descrição | Exemplo |
|---|---|---|
| `FROM_ADDRESS` | E-mail remetente (Outlook/Office 365) | `usuario@dominio.com.br` |
| `FROM_PASSWORD` | Senha do e-mail remetente | `sua-senha-segura` |
| `DATABASE_URL` | URL de conexão PostgreSQL | `postgresql://user:pass@host:5432/db?sslmode=require` |
| `BASE_URL` | URL base da API (usada nos links do e-mail) | `http://localhost:8000` |

> ⚠️ **Importante:** Nunca commite o arquivo `.env` no repositório. Adicione-o ao `.gitignore`.

---

## 🗄 Banco de Dados

O projeto utiliza **PostgreSQL** com o seguinte modelo de dados principal:

### Tabelas Principais

| Tabela | Descrição |
|---|---|
| `Aluno` | Cadastro de alunos (id, nome, phiz_id, email, ativo) |
| `Professor` | Cadastro de professores |
| `Coordenador` | Cadastro de coordenadores |
| `Serie` | Séries (ano de início) |
| `Sala` | Salas vinculadas a séries |
| `Materia` | Matérias do currículo |
| `Aluno_Sala` | Relação aluno ↔ sala |
| `Sala_Materia` | Relação sala ↔ matéria |
| `Professor_Sala_Materia` | Relação professor ↔ sala/matéria |
| `Avaliacao` | Avaliações por sala/matéria |
| `Nota` | Notas dos alunos nas avaliações |
| `Aula` | Registro de aulas |
| `Presenca` | Registro de presenças |
| `Fila_Notificacao` | Fila de notificações por e-mail |
| `Token_Autenticacao` | Tokens de autenticação (migration) |

### Tabela `Token_Autenticacao` (usada pela API)

```sql
CREATE TABLE IF NOT EXISTS "Token_Autenticacao" (
    "id"              INTEGER NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    "token"           VARCHAR(255) NOT NULL UNIQUE,
    "polling_token"   VARCHAR(255) NOT NULL UNIQUE,
    "email"           VARCHAR(255) NOT NULL,
    "phiz_id"         VARCHAR(255) NOT NULL,
    "criado_em"       TIMESTAMP NOT NULL DEFAULT NOW(),
    "expira_em"       TIMESTAMP NOT NULL,
    "utilizado"       BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY ("id")
);
```

### Scripts SQL

- **`dataabase.sql`** — Schema completo com todas as tabelas e foreign keys
- **`migration_auth_token.sql`** — Migration para criar a tabela `Token_Autenticacao`
- **`migration_replace_phone_with_phiz_id.sql`** — Migration incremental de telefone para Phiz ID

---

## 📡 Endpoints da API

### `POST /authenticate`

Inicia o fluxo de autenticação. A API valida o e-mail, troca a credencial temporária pelo Phiz ID no servidor, gera um token e envia o link de confirmação por e-mail. Enquanto a integração oficial de identidade do Phiz não estiver configurada, o endpoint retorna `501` sem persistir a credencial e sem enviar e-mail.

**Request Body:**
```json
{
  "email": "aluno@institutojef.org.br",
  "phiz_login_code": "credencial-temporaria-do-phiz"
}
```

**Response (200):**
```json
{
  "polling_token": "token-opaco-para-acompanhar-a-confirmacao"
}
```

**Erros possíveis:**

| Status | Descrição |
|---|---|
| `404` | Aluno não encontrado ou inativo |
| `422` | Credencial temporária do Phiz ausente ou inválida |
| `501` | Integração oficial de identidade do Phiz ainda não configurada |
| `500` | Erro interno do servidor |

---

### `GET /finish_authentication?token={token}`

Finaliza o fluxo de autenticação. Valida o token recebido e vincula o Phiz ID ao aluno.

**Query Parameters:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `token` | `string` | Token de autenticação recebido por e-mail |

**Response:**

Retorna uma **página HTML** estilizada com o resultado:

- ✅ **Sucesso** — Página de confirmação com confetti animation
- ❌ **Token inválido** — Página de erro informando que o link é inválido
- ❌ **Token já utilizado** — Página de erro informando que o link já foi usado
- ❌ **Token expirado** — Página de erro informando que o link expirou (30 min)

---

## 📖 Documentação Interativa

O FastAPI gera automaticamente documentação interativa da API:

| Ferramenta | URL |
|---|---|
| **Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## ☁️ Deploy

O projeto está configurado para deploy no **Koyeb** via Docker:

1. Faça push do código para o repositório GitHub
2. Conecte o repositório ao Koyeb
3. Configure as variáveis de ambiente no painel do Koyeb
4. O Koyeb irá buildar a imagem Docker e fazer deploy automaticamente
5. A aplicação roda na porta `8000` (configurada no `Dockerfile`)

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">
  Feito com 💜 por <strong>Phiz — Instituto Germinare</strong>
</p>

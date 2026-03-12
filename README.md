# Desafio MBA Engenharia de Software com IA - Full Cycle

Aplicação que ingere um PDF em um banco **PostgreSQL + pgvector** e expõe um chat em linha de comando para responder perguntas com base no conteúdo indexado. A solução utiliza LangChain para carregamento do documento, geração de embeddings (OpenAI ou Google Gemini) e busca semântica.

## Visão Geral

- **Ingestão**: `src/ingest.py` usa `DocumentProcessor` para quebrar o PDF em chunks, gerar embeddings (`Database`) e persistir no PGVector.
- **Busca/Chat**: `src/chat.py` executa o fluxo de perguntas. O prompt é montado em `helpers/search.py`, o contexto vem do repositório vetorial e a resposta é obtida via `init_chat_model`.
- **Configuração**: `EnvConfig` lê variáveis de ambiente para decidir provedores (OpenAI ou Google), modelos e conexões.

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose (para o PostgreSQL com pgvector)
- Conta/credenciais para os provedores selecionados (OpenAI ou Google Generative AI)

## Configuração do Ambiente

1. Clone o repositório e entre na pasta do projeto.
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Copie o arquivo de exemplo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
5. Edite o `.env` e informe os valores obrigatórios:

   | Variável | Descrição |
   | --- | --- |
   | `GOOGLE_API_KEY` | Chave de API do Google (necessária se usar modelos Gemini) |
   | `OPENAI_API_KEY` | Chave de API do OpenAI |
   | `MODEL_PROVIDER` | `openai` ou `google_genai` |
   | `GOOGLE_MODEL` | ID do modelo de chat Gemini (ex. `gemini-2.5-flash-lite`) |
   | `OPENAI_MODEL` | ID do modelo de chat OpenAI (ex. `gpt-4.1-mini`) |
   | `GOOGLE_EMBEDDING_MODEL` | ID do modelo de embedding Gemini (ex. `models/gemini-embedding-001`) |
   | `OPENAI_EMBEDDING_MODEL` | ID do modelo de embedding OpenAI (ex. `text-embedding-3-small`) |
   | `DATABASE_URL` | URL de conexão, ex. `postgresql+psycopg://postgres:postgres@localhost:5432/mba_ingestao_busca` |
   | `PG_VECTOR_COLLECTION_NAME` | Nome da coleção/tabela no PGVector |
   | `PDF_PATH` | Caminho para o PDF que será ingerido |

   > Caso utilize provider Google, certifique-se de escolher um modelo listado na chamada `models?key=<sua chave>` com suporte a `embedContent`.

## Banco de Dados (pgvector)

O projeto já inclui um `docker-compose.yml` com PostgreSQL 17 e extensão pgvector. Para subir a base localmente:

```bash
docker compose up -d
```

O serviço auxiliar `bootstrap_vector_ext` garante a criação da extensão `vector` no banco.

## Ingestão do PDF

Com o banco rodando e o `.env` configurado:

```bash
python src/ingest.py
```

O script irá:

1. Ler o PDF indicado em `PDF_PATH`.
2. Fragmentar o conteúdo com `RecursiveCharacterTextSplitter`.
3. Enriquecer metadados e gerar embeddings via provider escolhido.
4. Persistir os vetores na tabela configurada do PGVector.

Logs adicionais podem ser verificados diretamente no banco (`langchain_pg_embedding`).

## Executando o Chat CLI

Após a ingestão, execute:

```bash
python src/chat.py
```

O CLI suporta perguntas em português ou inglês, respeitando o contexto carregado. O fluxo:

1. Lê a pergunta do usuário (`CLI.read_user_message`).
2. Valida se a entrada é aceitável.
3. Busca documentos semelhantes no PGVector.
4. Monta prompt com `helpers/search.search_prompt`.
5. Chama o modelo configurado (OpenAI ou Gemini) e exibe a resposta.

Pressione `Ctrl+C` ou `Ctrl+D` para encerrar.

## Estrutura Principal

- `src/services/document_processor.py`: pipeline de preparação do PDF.
- `src/database/database.py`: abstração do repositório vetorial com LangChain PGVector.
- `src/helpers/`: funções utilitárias (montagem de prompt, construção de contexto).
- `src/services/cli.py`: utilidades para entrada/saída no chat.

## Dicas e Solução de Problemas

- **Erro 404 de modelo (Google)**: o ID usado em `GOOGLE_EMBEDDING_MODEL` precisa existir na listagem da API. Utilize `models/gemini-embedding-001` ou outro modelo com suporte a `embedContent`.
- **Credenciais Google**: é necessário ter o `GOOGLE_API_KEY` exportado ou carregado pelo `.env`. Se o `curl` retornar 403, verifique se a chave está ativa no shell.
- **Banco indisponível**: confirme se o container PostgreSQL está saudável (`docker compose ps`) e se a URL coincide com as credenciais padrões (`postgres/postgres`).

## Scripts Úteis

- **Subir banco**: `docker compose up -d`
- **Derrubar banco**: `docker compose down`
- **Ingestão**: `python src/ingest.py`
- **Chat**: `python src/chat.py`

Sinta-se à vontade para adaptar o fluxo para outros documentos ou provedores, ajustando o `.env` e repetindo a ingestão.
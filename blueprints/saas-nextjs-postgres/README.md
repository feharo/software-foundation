# __APP_NAME__ — PostgreSQL independente

> No repositório Software Foundation, este diretório é **um overlay**, não uma aplicação isolada: use `scripts/new_saas.py --database postgres` para gerar o projeto completo. No projeto gerado, este README descreve a aplicação final.

Este template usa **Next.js + PostgreSQL + Better Auth**. Você pode usar Postgres em Docker, DigitalOcean, VPS ou serviço gerenciado. **Não depende do Supabase.** A landing funciona antes de conectar o banco.

## Início rápido (local)

Requisitos: Node.js 22+, npm e Docker (opcional se já tem PostgreSQL).

```sh
npm install
cp .env.example .env.local
docker compose up -d db
```

Edite `.env.local` e defina `BETTER_AUTH_SECRET` com um segredo aleatório de pelo menos 32 caracteres:

```sh
openssl rand -base64 32
```

Mantenha `DATABASE_URL` para o Postgres local ou substitua pela string de conexão do seu banco.

```sh
npm run db:setup
npm run dev
```

Abra http://localhost:3000, acesse **Entrar**, crie sua conta e crie um workspace e tarefas. Os registros ficam no PostgreSQL conectado.

## Usar PostgreSQL externo

Não execute `docker compose`. Configure `DATABASE_URL=postgresql://usuario:senha@host:5432/banco` com TLS e acesso privado, respeitando as exigências de SSL do seu provedor. Nunca coloque credenciais no frontend.

## Autenticação

Better Auth gerencia sessões, registro e entrada com e-mail/senha. O servidor do Next.js valida cada sessão e restringe consultas/mutações a workspaces do proprietário. A aplicação ainda não possui convites, colaboradores, cobrança ou reset de senha por e-mail.

## Antes de publicar

- Ative verificação de e-mail, recuperação de senha e SMTP confiável; configure domínio HTTPS, CORS/origins e `BETTER_AUTH_URL` correto.
- Garanta backups, segregação de privilégios, TLS no banco, rate limits, logs sanitizados, alertas e política LGPD.
- Teste duas contas distintas tentando acessar IDs umas das outras. Build verde não substitui o teste de isolamento.
- Não leve o Docker Compose de desenvolvimento, nem sua senha fixa, para produção.
- A migração `db/schema.sql` é um bootstrap idempotente. Evoluções posteriores requerem migrações versionadas; não usar para modificar um banco com dados sem planejamento.

## Comandos

```sh
npm run dev
npm run typecheck
npm run build
npm run db:setup
python3 scripts/doctor.py
```

Consulte `SECURITY.md`, `PRODUCT_BRIEF.md` e `AGENTS.md` para continuar o desenvolvimento assistido por IA.

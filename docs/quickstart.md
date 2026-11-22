# Comece um SaaS com o banco de dados de sua escolha

O gerador suporta **duas opções**. Nenhuma exige conhecimento de banco para criar a landing; para autenticação e dados reais é necessária a configuração da opção escolhida.

| Opção | Melhor quando | Componentes |
|---|---|---|
| `supabase` | Quer começar rapidamente com autenticação e banco gerenciados | Next.js + Supabase Auth + PostgreSQL com RLS |
| `postgres` | Já tem PostgreSQL ou quer controlar infraestrutura | Next.js + PostgreSQL (VPS, Docker ou gerenciado) + Better Auth |

**Ambas suportam produtos profissionais**. A decisão é sobre custos, operação e controle, não sobre o nível de habilidade.

## Criar com assistente

```sh
git clone https://github.com/feharo/software-foundation.git
cd software-foundation
python3 scripts/new_saas.py --name "Minha Agenda"
```

Escolha 1 (Supabase) ou 2 (PostgreSQL independente). Para automatizar sem perguntas:

```sh
python3 scripts/new_saas.py --name "Minha Agenda" --database postgres --output ../minha-agenda --non-interactive
```

## Se escolher Supabase

1. `cd ../minha-agenda && npm install`
2. `cp .env.example .env.local`
3. Configure projeto no Supabase, `NEXT_PUBLIC_SUPABASE_URL` e `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`.
4. Execute `supabase/schema.sql` no SQL Editor do Supabase.
5. Configure Auth > URL Configuration e então `npm run dev`. O login é por magic link.

## Se escolher PostgreSQL independente

1. `cd ../minha-agenda && npm install`
2. `cp .env.example .env.local`
3. Para PostgreSQL local, instale Docker e use `docker compose up -d db`; em VPS/banco gerenciado, informe o URI em `DATABASE_URL`.
4. Gere um segredo seguro (`openssl rand -base64 32`) e preencha `BETTER_AUTH_SECRET` e `BETTER_AUTH_URL`.
5. Execute `npx auth@latest migrate` para criar as tabelas de autenticação, depois `npm run db:migrate` para criar workspaces e tarefas.
6. Rode `npm run dev`, entre em `/login`, crie conta e acesse o painel.

Leia o README do projeto gerado, especialmente os requisitos de segurança para produção. O Postgres próprio **não usa nenhuma chave/API do Supabase**.

## Em Windows PowerShell

Use `py scripts/new_saas.py ...` e `Copy-Item .env.example .env.local`.

## Observação de produção

O starter PostgreSQL inclui autenticação por e-mail/senha para uso inicial, mas **verificação de e-mail, recuperação de senha com provedor de e-mail, backups, observabilidade, testes multiusuário e LGPD devem ser configurados antes de lançar**. Nunca publique o serviço de banco de exemplo na Internet. Ambos os perfis precisam de testes de autorização reais.

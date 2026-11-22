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
5. Execute `npm run db:setup`: o script carrega o `.env.local`, instala a migração do Better Auth e cria as tabelas de workspaces e tarefas.
6. Rode `npm run dev`, entre em `/login`, crie conta e acesse o painel.

Leia o README do projeto gerado, especialmente os requisitos de segurança para produção. O Postgres próprio **não usa nenhuma chave/API do Supabase**.

## Em Windows PowerShell

Use `py scripts/new_saas.py ...` e `Copy-Item .env.example .env.local`.

## Observação de produção

O starter PostgreSQL inclui autenticação por e-mail/senha para uso inicial, mas **verificação de e-mail, recuperação de senha com provedor de e-mail, backups, observabilidade, testes multiusuário e LGPD devem ser configurados antes de lançar**. Nunca publique o serviço de banco de exemplo na Internet. Ambos os perfis precisam de testes de autorização reais.


## Guia completo — Windows PowerShell

Instale **Python 3.12+**, **Node.js 22+** e Git for Windows. Abra o PowerShell na pasta onde deseja trabalhar. Docker só é necessário para iniciar um PostgreSQL local; você pode escolher um banco remoto gerenciado.

```powershell
git clone https://github.com/feharo/software-foundation.git
Set-Location software-foundation
py -3.12 foundation.py init --name "Minha Agenda" --database postgres --output ..\minha-agenda --non-interactive
Set-Location ..\minha-agenda
npm install
Copy-Item .env.example .env.local
npm run dev
```

Com PostgreSQL independente, configure as variáveis `DATABASE_URL`, `BETTER_AUTH_SECRET` e `BETTER_AUTH_URL` e rode `npm run db:setup`. Para um teste local, inicie o banco com `docker compose up -d db` antes das migrações. Sem banco, a landing pública abre, mas login e dados não funcionam.

**Adotar padrões em um projeto existente:**

```powershell
Set-Location software-foundation
py -3.12 foundation.py adopt ..\meu-projeto
py -3.12 foundation.py adopt ..\meu-projeto --apply
py -3.12 foundation.py audit ..\meu-projeto --format markdown --output ..\auditoria.md
```

Se o Windows disser que Python não está instalado, confirme `py -0p` (Python Launcher) ou use `python foundation.py ...` após instalação. No Git Bash/Linux, use `python3`. No PowerShell, variáveis de ambiente são definidas por `$env:KEY = '...'`, não pelo comando Unix `export`.

O workflow `.github/workflows/windows-smoke.yml` executa criação, adoção, diagnóstico, auditoria e compilação dos dois perfis em um runner Windows limpo, sem conexão de produção. Isso não substitui um teste manual no computador de cada usuário.

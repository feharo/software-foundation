# Primeiro SaaS em poucos passos

Este guia serve para quem não programa. É necessário instalar Python 3 e Node.js 22 ou 24 no computador, e criar um projeto Supabase gratuito ou pago.

## 1. Gerar o projeto

```sh
git clone https://github.com/feharo/software-foundation.git
cd software-foundation
python3 scripts/new_saas.py --name "Minha Agenda" --output ../minha-agenda --non-interactive
cd ../minha-agenda
npm install
cp .env.example .env.local
npm run dev
```

Abra http://localhost:3000. A landing pública e as páginas já possuem estrutura visual, estados de configuração e responsividade.

> No Windows PowerShell, use `py scripts/new_saas.py ...` e `Copy-Item .env.example .env.local`. Repo é privado: para clonar, faça login no GitHub.

## 2. Habilitar login, banco e áreas privadas

1. Crie um projeto em https://supabase.com/dashboard .
2. Abra SQL Editor e execute `supabase/schema.sql` do SaaS gerado.
3. No Supabase, acesse Project Settings > API (ou Connect), copie **Project URL** e **publishable/anon key**.
4. Cole no `.env.local` em `NEXT_PUBLIC_SUPABASE_URL` e `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`. Não use secret/service_role key.
5. Em Authentication > URL Configuration, configure `http://localhost:3000` e permita o endereço `http://localhost:3000/dashboard` como redirect.
6. Reinicie `npm run dev`. Insira seu e-mail na tela de login e abra o link recebido.
7. Crie um workspace e a primeira tarefa no dashboard.

Os e-mails de teste podem estar sujeitos a restrições de envio no Supabase; configure SMTP dedicado para lançar o produto.

## 3. Antes de publicar

A amostra não inclui faturamento, convites, papéis avançados nem política de privacidade adaptada ao produto. Não aceite clientes pagantes nem dados sensíveis antes de configurar e testar autenticação, RLS, backups, recuperação, LGPD e monitoramento.

Veja `docs/saas-roadmap.md` e `blueprints/saas-nextjs-supabase/README.md`.

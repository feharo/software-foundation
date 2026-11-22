# __APP_NAME__

Aplicação SaaS gerada a partir do Software Foundation. Este starter contém landing responsiva, login com magic link, dashboard protegido no cliente, workspaces e lista de tarefas com paginação e Row Level Security no Supabase.

## Rodar localmente

Requisitos: Node.js 22+ e uma conta Supabase para as áreas autenticadas.

```sh
npm install
cp .env.example .env.local
npm run dev
```

Acesse http://localhost:3000. **Sem Supabase, somente a landing e as telas de orientação funcionam.**

## Testar localmente sem conta no Supabase

Além da opção hospedada, o projeto gerado inclui `supabase/config.toml`,
migração versionada e `scripts/integration-smoke.mjs`.

Com Node.js, Docker e a CLI Supabase instalada:

```sh
supabase start --exclude studio,imgproxy,logflare,vector,edge-runtime,postgres-meta,realtime,storage-api,supavisor,mailpit
node scripts/integration-smoke.mjs
supabase stop
```

O smoke usa **duas contas descartáveis** e valida login, criação de workspace, tarefas,
leitura e escrita entre tenants e bloqueio de usuários não autenticados.
Ele não depende de chaves, permissões ou serviços do seu projeto hospedado.
Veja `https://github.com/feharo/software-foundation/blob/main/docs/supabase-testing.md`.

## Ativar o banco e autenticação

1. Crie seu projeto em https://supabase.com/dashboard.
2. No SQL Editor, execute o arquivo `supabase/schema.sql` deste projeto.
3. Copie a Project URL e a **publishable key** (ou chave anon legada) para `.env.local`.
4. Em Authentication > URL Configuration, permita `http://localhost:3000/dashboard` na lista de redirects e ajuste o Site URL.
5. Reinicie o servidor, vá para `/login`, solicite um magic link e abra o e-mail.
6. No dashboard, crie workspace e tarefas. Os dados são persistidos no Supabase e isolados por RLS.

Em ambiente público, configure SMTP próprio, domínio HTTPS, URLs de redirect, backups e políticas de dados. Este modelo **não implementa faturamento, convites de equipe, métricas reais, monitoramento RUM ou verificação e2e de isolamento**.

## Arquitetura e segurança

- Next.js App Router: landing renderizada no servidor; dashboard client-side para simplicidade de demonstração.
- Supabase Auth usa sessão gerenciada pelo SDK. A autorização real ocorre em policies RLS.
- O banco só concede SELECT/INSERT/UPDATE/DELETE às entidades necessárias; não colocar `service_role` em `NEXT_PUBLIC_*`.
- Workspaces têm dono; um gatilho cria sua membership de proprietário automaticamente.
- Cada tarefa possui `workspace_id` e policies checam `auth.uid()` como membro.
- A busca aplica debounce e o backend pagina as tarefas via PostgREST; requisições antigas são ignoradas.
- CSS com tokens semânticos, foco visível, estrutura mobile-first e skeleton durante carregamento.
- Não incluir dados sensíveis sem avaliação adicional de segurança e LGPD.

## Scripts

```sh
npm run dev
npm run typecheck
npm run build
npm start
```

## Próximos passos

Consulte `https://github.com/feharo/software-foundation/blob/main/docs/saas-roadmap.md`. Adicione fluxos de negócio, permissões e pagamentos apenas quando seus critérios de aceite forem testáveis.

## Padrões incorporados

O projeto foi gerado com `AGENTS.md`, `CLAUDE.md` e uma cópia local do catálogo em `.foundation/standards/performance.json`. Isso permite que os agentes continuem seguindo o mesmo padrão após você separar o SaaS deste repositório. O arquivo `.foundation/profile.json` descreve o stack do starter.

## Diagnóstico para iniciantes

```sh
python3 scripts/doctor.py
```

O diagnóstico informa se Node.js, npm, variáveis do Supabase e migração SQL estão presentes, **sem imprimir valores de chaves**. Após o primeiro `npm install`, inclua o arquivo `package-lock.json` no controle de versão para builds mais reprodutíveis.

## Testar interface mobile e desktop

Depois de `npm install` e `npm run build`, instale o Chromium uma vez com `npx playwright install chromium` e execute `npm run test:e2e`. Esses testes cobrem a navegação pública, a tela de login e overflow horizontal nas larguras de 375 px e desktop. Eles **não** exigem um Supabase hospedado.

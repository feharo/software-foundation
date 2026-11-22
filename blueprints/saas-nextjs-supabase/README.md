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

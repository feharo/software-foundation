# Segurança — PostgreSQL independente

Este perfil não usa Supabase nem depende de RLS. O banco só é acessado pelo backend Next.js, e toda operação de domínio verifica a sessão Better Auth e o `owner_id` na mesma consulta SQL.

- Nunca exportar `DATABASE_URL`, `BETTER_AUTH_SECRET` ou outras credenciais em variáveis `NEXT_PUBLIC_*`.
- Garantir que nenhum route handler aceite `owner_id` informado pelo cliente; obtê-lo exclusivamente da sessão validada no servidor.
- Não consultar/alterar tarefas sem associação à tabela `workspaces` e filtro `owner_id = session.user.id`.
- Os IDs são imprevisíveis, mas UUID **não é controle de autorização**; os filtros por proprietário são obrigatórios.
- Rate limit e revogação de sessões precisam ser revisados na configuração real. O starter oferece somente e-mail/senha; verificação e reset não estão implementados.
- Em produção usar conexões privadas TLS, backups, migrações versionadas, monitoração e banco sem exposição pública.
- Testar multi-tenant com duas contas e IDs cruzados antes de lançar. Cobrança e convites de equipe não estão prontos.
- O Docker Compose de exemplo **é apenas para desenvolvimento local** com senha conhecida.

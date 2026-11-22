# Segurança do starter

- Login: Supabase Auth magic link. Configure SMTP, URLs autorizadas, políticas de acesso e proteção de conta antes de produção.
- Dados: SQL em `supabase/schema.sql` habilita Row Level Security para workspaces, memberships e tasks.
- Isolamento: filtros no frontend são para UX; segurança é responsabilidade do banco.
- Segredos: jamais coloque `service_role` ou `sb_secret_*` nas variáveis `NEXT_PUBLIC_*` ou em Git.
- Permissões: starter possui apenas owner; convites, roles e audit log exigem implementação segura posterior.
- Sessão: o SDK mantém sessão no navegador; considere SSR/cookies HTTP-only para aplicativos com exigências elevadas.
- Testes pendentes: separar dois usuários de teste, tentar ler/editar workspace de outro usuário, forjar `created_by`, verificar limite e entrada maliciosa. Não presumir segurança antes desses testes.
- Dados pessoais: definir política de privacidade, retenção e exclusão, backups, suporte, LGPD e alertas de incidentes.

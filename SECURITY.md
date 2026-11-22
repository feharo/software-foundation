# Política de segurança

O Software Foundation inclui geradores de projetos e exemplos de autenticação. Não presuma que os starters estejam prontos para armazenar dados sensíveis ou atender clientes pagantes sem configuração e validação adicionais.

## Relatar uma vulnerabilidade

**Não publique credenciais, dados de clientes ou detalhes exploráveis em issues públicas.** Utilize a opção *Report a vulnerability* / *Private vulnerability reporting* na seção Security do GitHub, caso esteja habilitada. Se não houver canal privado disponível, solicite aos mantenedores a habilitação de um canal seguro **sem incluir detalhes técnicos sensíveis na solicitação pública**.

Não existe neste momento um prazo de resposta ou SLA divulgado.

## Escopo

- `scripts/`, `foundation.py`, templates e workflows;
- autenticação, sessão e isolamento multi-tenant nos dois starters;
- migrações, acesso ao PostgreSQL e políticas RLS do Supabase;
- exposição de segredos, dependências e distribuição.

## Recomendações a quem utiliza

- Não use valores do `.env.example` ou senhas de Docker local em produção.
- Jamais envie `DATABASE_URL`, `BETTER_AUTH_SECRET` ou chaves privadas para código client ou repositório.
- Configure HTTPS, validação de origem, políticas de autenticação, recuperação de conta, rate limiting, backups, alertas e política de privacidade.
- Execute os testes de autorização com **duas contas** e inclua caminhos de erro, leitura e escrita cruzadas.
- O catálogo de 31 regras orienta a revisão; sua presença não constitui certificação de segurança.

Última revisão: 2026-11-22.

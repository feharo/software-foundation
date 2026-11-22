# Roadmap da fundação: de instruções a fábrica de SaaS

## Implementado na V2/V3
- Catálogo das 31 práticas com aplicabilidade.
- Gerador de projeto `scripts/new_saas.py` com entrada interativa ou não interativa.
- Blueprint Next.js + React + Supabase, landing responsiva, login magic link, dashboard, workspace e tarefas com paginação.
- Opção independente de PostgreSQL para Docker, VPS ou banco gerenciado, com Better Auth, rotas protegidas e migrações SQL do aplicativo.
- SQL de Row Level Security para isolamento de dados por workspace e entrada protegida.
- Skill `saas-builder` e playbook de frontend com prioridades da Vercel.
- CI de geração, testes Python e build dos dois perfis do blueprint.

## Próximas entregas — não implementadas
1. Onboarding assistido na interface (wizard visual) e escolha entre múltiplos stacks.
2. Convites e gestão segura de equipe (roles, permissões, aceite, expiração e trilha de auditoria).
3. Cobrança integrada: planos, trial, checkout, webhooks verificados, idempotência, invoices e cancelamento.
4. Testes e2e com Supabase local, tenants A/B, sessões, erro e rede lenta.
5. Componentes de design system com Storybook ou alternativa leve, tokens, temas e avaliações a11y.
6. Pipelines de produção: preview automático, ambientes, migrações, smoke tests, rollback e verificação de secrets.
7. Observabilidade e RUM com baseline/alertas, versionamento e painel de conformidade real.
8. Skill de arquiteto de SaaS, gerador de PR por funcionalidade e revisão especializada com agentes.

## Princípio

Não dar a impressão de que uma landing + CRUD são um SaaS comercial pronto. Executar a jornada real e medir antes de escalar.

## V3 — dois caminhos, um sistema

- CLI única `python3 foundation.py` com `init` (projeto novo), `adopt` (projeto existente), `audit` e `doctor`.
- `adopt` funciona em modo prévia por padrão, instala padrões apenas com `--apply`, preserva `AGENTS.md` e `CLAUDE.md` existentes, impede sobrescrita da pasta gerenciada e é idempotente.
- `audit` lê o projeto sem alterar seu código e emite 31 status com evidências esperadas, além de checagens estáticas de CI, testes, build e dependências. **Não** declara regras atendidas por presença de arquivos.
- Próximas fases: verificações dinâmicas proporcionais ao projeto, `foundation fix` com revisão de PR e `foundation upgrade` com migrações seguras.

# Roadmap da fundação: de instruções a fábrica de SaaS

## Implementado na V2
- Catálogo das 31 práticas com aplicabilidade.
- Gerador de projeto `scripts/new_saas.py` com entrada interativa ou não interativa.
- Blueprint Next.js + React + Supabase, landing responsiva, login magic link, dashboard, workspace e tarefas com paginação.
- SQL de Row Level Security para isolamento de dados por workspace e entrada protegida.
- Skill `saas-builder` e playbook de frontend com prioridades da Vercel.
- CI de geração, testes Python e tentativa de build real do blueprint.

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

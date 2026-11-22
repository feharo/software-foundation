# Engineering rules — Software Foundation

Fonte de verdade: https://github.com/feharo/software-foundation (fixar SHA/tag antes de usar em produção).

Para cada funcionalidade:
1. Identificar jornada de usuário, stack, escala e riscos de privacidade/multi-tenant.
2. Consultar `standards/performance.json` e `docs/frontend-playbook.md` para UI React/Next.js.
3. Priorizar waterfalls e bundle size, depois server/client, re-render e refinamentos; revisar a Skill oficial Vercel React Best Practices se instalada.
4. Implementar estados loading/skeleton, vazio, erro, sessão expirada, acessibilidade e mobile first.
5. Isolar operações por tenant no backend/RLS; não confiar em filtros do cliente.
6. Desenvolver a menor solução viável; não introduzir Redis, filas, SSR ou balanceamento sem justificativa.
7. Registrar evidências verificáveis; nunca simular conformidade.
8. Executar lint, testes, types, build e fluxos mobile antes de merge.

Use as Skills `saas-builder` e `performance-guardian` quando disponíveis. Adapte este arquivo ao projeto consumidor.

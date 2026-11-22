---
name: performance-guardian
description: Auditar e implementar praticas de performance em projetos de software web, APIs e SaaS. Usar ao criar funcionalidade, revisar PR, diagnosticar lentidao ou avaliar as 31 regras de Software Foundation em front-end, back-end, banco, infraestrutura e observabilidade.
---

# Performance Guardian

1. Ler `standards/performance.json` da versao aprovada para o projeto; se o agente nao tiver acesso, solicitar copia ou usar arquivo vendorizado.
2. Identificar stack e superficie afetada; ler o perfil relevante em `profiles/`.
3. Para cada regra pertinente, declarar aplicabilidade, nivel, alteracao e evidencias. Usar `not_verified` enquanto nao testar.
4. Implementar menor solucao suficiente, preservando seguranca, integridade, acessibilidade e funcionalidade.
5. Executar testes reais. Quando indisponiveis, documentar limite claramente e nao afirmar sucesso.
6. Entregar resumo por regra: ID, status, evidencia, risco residual, proximos passos.

## Proibicoes

- Nao adicionar Redis, balanceador, fila, SSR ou cache por reflexo.
- Nao declarar conformidade apenas por existir checklist.
- Nao introduzir regressao de LCP com lazy loading da imagem principal.
- Nao incluir dados sensiveis em traces e logs.
- Nao fazer merge ignorando checks obrigatorios.

## Contrato

Usar status `pass|fail|not_applicable|not_verified` conforme `schemas/audit-report.example.json`. Justificar toda excecao. Ver `references/evidence.md`.

## React e Next.js

No caso de React/Next.js, revisar primeiro waterfalls e tamanho de bundle, depois renderização no servidor, dados do cliente, renders, custo de renderização, JavaScript e padrões avançados. Consultar `docs/frontend-playbook.md` e considerar a skill oficial Vercel React Best Practices: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices. Não redistribuir seu conteúdo sem verificar licença e versão. Não tratar micro-otimizações como prioridade antes de medir rede, LCP, INP e CLS.

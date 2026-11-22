# Software Foundation

Padroes versionados para construir SaaS, APIs e interfaces com qualidade mensuravel. **Nao e um framework de runtime.** Usa instrucoes para agentes, regras auditaveis e um validador sem dependencias externas.

## Comece aqui

1. Leia [as 31 regras](standards/performance.json) e [as decisoes de arquitetura](docs/architecture.md).
2. Escolha um perfil em [profiles/](profiles/) e registre aplicabilidade no seu projeto.
3. Copie [templates/AGENTS.md](templates/AGENTS.md) e, se usar Claude, [templates/CLAUDE.md](templates/CLAUDE.md); adapte paths e versao.
4. Use [skills/performance-guardian/SKILL.md](skills/performance-guardian/SKILL.md) no seu agente.
5. Execute `python3 scripts/validate_foundation.py` e `python3 -m unittest discover -s tests -v`.
6. Nos projetos consumidores, use [docs/adoption.md](docs/adoption.md) e a [action reutilizavel](.github/workflows/foundation-quality.yml).

## O que e realmente automatico?

O CI inicial verifica a **integridade dos padroes e dos perfis** e gera relatorio de aplicabilidade sobre o catalogo. Ele nao afirma detectar N+1, Redis, seguranca ou performance real por analise estatica. Esses itens exigem testes no software consumidor, telemetria e revisao tecnica com evidencias.

**Niveis**: `required` = exigido quando aplicavel; `conditional` = avaliar com criterio; `advisory` = recomendacao. Uma regra pode ser `not_applicable` com justificativa.

## Seguranca

Nunca colocar credenciais, tokens, URLs internas sensiveis, dados pessoais ou prompts com informacoes de clientes neste repositorio. Revisar permissoes e acesso ao reutilizar workflows entre repositorios privados.

## Licenca

Sem licenca open source definida; todos os direitos reservados ate decisao explicita do mantenedor.

# Architecture decision guide

For a map of the **actual components and their relationships** (CLI, starters, profiles, standards, Skills, CI), see [Software Foundation ecosystem architecture](ecosystem.md). This page records architectural decision principles.

A fundacao e **policy-as-data**, nao prescricao de arquitetura. Regras e criterios devem ser versionados; os produtos devem fazer o trabalho real e publicar evidencias.

## Ordem de decisao

1. Identificar tipo de produto, volumes, SEO, plataformas e perfil de usuario.
2. Selecionar condicoes de aplicabilidade por regra; registrar `pass`, `fail`, `not_applicable` ou `not_verified`.
3. Antes de introduzir Redis, filas, SSR e balanceamento, demonstrar problema ou requisito com medicao/risco concreto.
4. Validar seguranca, acessibilidade, custos de infraestrutura e rollback.
5. Associar cada alteracao a teste, trace, profiling ou medicao reproduzivel.

## Performance budgets propostos

Para aplicacoes web de producao, definir alvos de Core Web Vitals no p75: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1. Nao confundir metas de campo com score Lighthouse sintetico. Os orcamentos por rota, device e tipo de conectividade devem ser aprovados por projeto.

## Nunca declarar compliance automaticamente

Validacao de schemas nao valida paginas. Uma regra so recebe `pass` apos evidencia verificavel sobre o projeto alvo. Sem evidencia, usar `not_verified`.

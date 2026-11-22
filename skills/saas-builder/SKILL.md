---
name: saas-builder
description: Iniciar e evoluir aplicações SaaS completas a partir do software-foundation, com onboarding para iniciantes, React/Next.js, autenticação, dados multi-tenant, UX mobile first e CI. Usar quando for solicitado criar um SaaS, transformar uma ideia em MVP, gerar projeto a partir do blueprint, implementar módulos, preparar release ou auditar lacunas entre protótipo e produção.
---

# SaaS Builder

## Primeiros passos
1. Identificar objetivo do produto, tipo de usuário, principal jornada e necessidade de dados sensíveis.
2. Se projeto novo, escolher o backend com o usuário e usar `python3 scripts/new_saas.py --name "Meu SaaS" --database supabase|postgres --output ./meu-saas --non-interactive`. Supabase e PostgreSQL independente são opções válidas em qualquer nível de experiência.
3. Ler `docs/quickstart.md`, `docs/saas-roadmap.md` e `docs/frontend-playbook.md` conforme a tarefa.
4. Separar o que já funciona daquilo que depende de configuração (Supabase ou PostgreSQL, autenticação, e-mail, domínio, faturamento).
5. Criar a menor jornada operacional completa possível; no perfil Supabase exigir RLS, no perfil PostgreSQL independente verificar ownership em **todas** as consultas/mutações do backend. Não confiar em filtro de frontend.
6. Instalar a skill oficial de performance React da Vercel, após revisar sua origem e versão, em projetos React/Next.js. Não copiar nem congelar regras upstream sem revisão de licença.
7. Executar testes, build, checks de UI mobile e critérios de aceite. Não afirmar sucesso sem evidência.

## Prioridades de frontend
1. Evitar waterfalls nas cargas de dados e reduzir payload JS inicial.
2. Preferir renderização no servidor para conteúdo público e fronteira client para interação.
3. Garantir loading skeleton sem layout shift, estados vazios, erro, acesso negado e sessão expirada.
4. Testar busca e paginação com dados representativos e evitar buscas duplicadas.
5. Garantir navegação por teclado, foco, contraste, rótulos e touch targets mobile.
6. Medir LCP/INP/CLS e analisar a experiência de produção.

## Guardrails
- Nunca usar dados demo como se fossem persistentes ou faturamento falso.
- Nunca expor `service_role` em código client, registrar senhas ou confiar em filtro do cliente para isolar tenant.
- Evitar overengineering: filas, Redis, microserviços e balanceadores apenas quando necessários.
- Dependências externas e deploy exigem configuração explícita e testes reais.
- Descrever status em termos `implemented`, `configured`, `tested`, `blocked` e `planned`.

## Saída
Entregar caminho do projeto, como rodar localmente, funcionalidades efetivas, verificações e pendências reais.

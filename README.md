# Software Foundation

Fundação de engenharia para criar SaaS profissionais com IA, sem depender de repetir prompts. Une **gerador de projeto**, **Skill para agentes**, **31 padrões verificáveis** e **CI**.

## Primeiro SaaS

```sh
git clone https://github.com/feharo/software-foundation.git
cd software-foundation
python3 scripts/new_saas.py --name "Meu SaaS" --output ../meu-saas --non-interactive
cd ../meu-saas
npm install
cp .env.example .env.local
npm run dev
```

A landing abre em http://localhost:3000 mesmo sem configurar o banco. A autenticação por magic link e o dashboard com workspace/tarefas tornam-se funcionais após conectar Supabase e executar a migração SQL. **Cobrança, convites e controles avançados ainda não estão implementados**.

Leia [passo a passo para iniciantes](docs/quickstart.md), [guia de frontend](docs/frontend-playbook.md) e [roadmap do SaaS](docs/saas-roadmap.md).

## A fundação

- [31 regras versionadas](standards/performance.json): regra, aplicabilidade, evidência e nível.
- [SaaS Builder](skills/saas-builder/SKILL.md): Skill para criar uma jornada operacional.
- [Performance Guardian](skills/performance-guardian/SKILL.md): revisar performance e qualidade, sem inventar resultados.
- [Templates de agentes](templates/): `AGENTS.md` e `CLAUDE.md`.
- [Perfis](profiles/): Next.js/NestJS, React SPA e API.
- [Blueprint Next.js/Supabase](blueprints/saas-nextjs-supabase/): exemplo executável com RLS no banco.
- [CI de validação](.github/workflows/quality.yml) e [build do starter](.github/workflows/saas-starter.yml).

## Verificações da fundação

```sh
python3 scripts/validate_foundation.py
python3 -m unittest discover -s tests -v
```

Esses testes validam o catálogo e o gerador. Não comprovam performance real, segurança ou todas as integrações de um SaaS. O build da aplicação gerada é executado no GitHub Actions; testes reais entre tenants requerem instância Supabase configurada.

## Vercel React Best Practices

Integramos o **método de priorização** e uma referência à skill oficial de React/Next.js da Vercel, sem redistribuir o material. Veja o comando de instalação em [frontend-playbook.md](docs/frontend-playbook.md). As oito áreas começam por waterfalls e bundle.

## Política de segurança

Não salvar credenciais nem `service_role` em `NEXT_PUBLIC_*`. Garantir RLS, autorização no banco/API, backups, tratamento LGPD e observabilidade antes de atender clientes reais.

## Licença

Sem licença open source definida; todos os direitos reservados até decisão do mantenedor.

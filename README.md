# Software Foundation

Fundação de engenharia para criar SaaS profissionais com IA, sem depender de repetir prompts. Une **gerador de projeto**, **Skill para agentes**, **31 padrões verificáveis** e **CI**.

## Dois caminhos, um sistema

**Criar um projeto novo:**

```sh
python3 foundation.py init --name "Meu SaaS" --database postgres --output ../meu-saas --non-interactive
```

**Evoluir um projeto existente, sem alterar código:**

```sh
python3 foundation.py adopt ../meu-projeto
python3 foundation.py adopt ../meu-projeto --apply
python3 foundation.py audit ../meu-projeto --format markdown --output ../auditoria-projeto.md
python3 foundation.py upgrade ../meu-projeto        # verifica novas regras
python3 foundation.py upgrade ../meu-projeto --apply
```

A instalação das regras exige `--apply`. A auditoria é somente leitura, exceto quando você escolhe salvar o relatório. `adopt` não altera arquivos já existentes: preserva instruções personalizadas dos agentes e bloqueia conflitos na pasta gerenciada.

Leia [a arquitetura dos dois caminhos](docs/two-paths.md).

## Primeiro SaaS

```sh
git clone https://github.com/feharo/software-foundation.git
cd software-foundation
python3 scripts/new_saas.py --name "Meu SaaS" --database supabase --output ../meu-saas --non-interactive
cd ../meu-saas
npm install
cp .env.example .env.local
npm run dev
```

Também é possível escolher PostgreSQL independente: `--database postgres` (Docker, VPS ou serviço gerenciado). O modo interativo pergunta qual opção usar. A landing abre em http://localhost:3000 mesmo sem configurar o banco. No perfil Supabase, magic link e dashboard ficam funcionais após configurar o Supabase. No perfil PostgreSQL, login por senha e dashboard são servidos pelo próprio Next.js com Better Auth e backend PostgreSQL, após migração e configuração. **Cobrança, convites e controles avançados ainda não estão implementados**.

Leia [passo a passo para iniciantes](docs/quickstart.md), [guia de frontend](docs/frontend-playbook.md) e [roadmap do SaaS](docs/saas-roadmap.md).

## A fundação

- [31 regras versionadas](standards/performance.json): regra, aplicabilidade, evidência e nível.
- [SaaS Builder](skills/saas-builder/SKILL.md): Skill para criar uma jornada operacional.
- [Performance Guardian](skills/performance-guardian/SKILL.md): revisar performance e qualidade, sem inventar resultados.
- [Templates de agentes](templates/): `AGENTS.md` e `CLAUDE.md`.
- [Perfis](profiles/): Next.js/NestJS, React SPA e API.
- [Blueprint Next.js/Supabase](blueprints/saas-nextjs-supabase/): serviço gerenciado com RLS no banco.
- [Overlay PostgreSQL independente](blueprints/saas-nextjs-postgres/): login via Better Auth, API protegida e SQL com autorização por workspace, sem Supabase.
- [CI de validação](.github/workflows/quality.yml) e [build do starter](.github/workflows/saas-starter.yml).

## Verificações da fundação

```sh
python3 scripts/validate_foundation.py
python3 -m unittest discover -s tests -v
```

Esses testes validam o catálogo e o gerador. Não comprovam performance real, segurança ou todas as integrações de um SaaS. O build de ambos os perfis de aplicação gerada é executado no GitHub Actions; o teste de Auth/RLS da variante Supabase usa containers locais; o comportamento de um projeto hospedado ainda exige homologação própria.

## Vercel React Best Practices

Integramos o **método de priorização** e uma referência à skill oficial de React/Next.js da Vercel, sem redistribuir o material. Veja o comando de instalação em [frontend-playbook.md](docs/frontend-playbook.md). As oito áreas começam por waterfalls e bundle.

## Política de segurança

Não salvar credenciais nem `service_role` em `NEXT_PUBLIC_*`. Garantir RLS, autorização no banco/API, backups, tratamento LGPD e observabilidade antes de atender clientes reais.

## Prévia pública e contribuição

O repositório **ainda está privado e sem licença de reutilização**, portanto não foi publicado como open source. Antes de abrir, siga o [checklist de pré-publicação](docs/public-preview-checklist.md), leia a [política de segurança](SECURITY.md) e o [guia de contribuição](CONTRIBUTING.md).

```sh
python3 scripts/check_publication.py
python3 scripts/check_publication.py --strict  # exige LICENSE
```

O modo padrão verifica conteúdo rastreado, mas não histórico Git. O CI agora também executa teste de Auth/RLS no Supabase **local**, com duas contas, sem precisar de projeto hospedado. Veja [como testar Supabase](docs/supabase-testing.md).

## Licença

Sem licença open source definida; todos os direitos reservados até decisão do mantenedor.

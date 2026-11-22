# Software Foundation — crie SaaS e evolua projetos com IA

[English](../README.md) · [Primeiros passos](quickstart.md) · [Guia para agentes de IA](for-ai-agents.md) · [Frontend](frontend-playbook.md) · [Segurança](../SECURITY.md)

O **Software Foundation** reúne um gerador de SaaS em Next.js/React, boas práticas de performance, Skills para agentes de programação e verificações automatizadas. O foco é acelerar **dois caminhos usando a mesma fundação de engenharia**.

> **Estado atual:** pré-lançamento privado, com **licença [MIT](../LICENSE)** já definida. A abertura pública ainda depende de autorização. Este projeto não é um construtor de SaaS pronto para produção nem um corretor automático de bugs.

## Dois caminhos, um sistema

### 1. Criar um projeto novo

```bash
git clone https://github.com/feharo/software-foundation.git
cd software-foundation
python3 foundation.py init --name "Meu SaaS" --database postgres --output ../meu-saas --non-interactive
cd ../meu-saas
npm install
cp .env.example .env.local
npm run dev
```

Pré-requisitos: Python 3.12+, Node.js 22+ e npm. Acesse `http://localhost:3000`. A landing funciona antes da configuração, mas login e dados exigem banco e migrações.

Escolha entre **Supabase** (PostgreSQL e autenticação gerenciados) e **PostgreSQL independente** (Docker, VPS ou serviço gerenciado, com Better Auth). Para Windows PowerShell, veja [o guia específico](quickstart.md).

### 2. Modernizar um projeto existente

```bash
cd software-foundation
python3 foundation.py adopt ../meu-projeto
python3 foundation.py adopt ../meu-projeto --apply
python3 foundation.py audit ../meu-projeto --format markdown
```

A prévia não altera nada. O `--apply` adiciona apenas arquivos ausentes e preserva personalizações existentes. A auditoria é estática; não mede PageSpeed, não executa o projeto e **não corrige automaticamente** problemas.

## O que já está implementado

- Gerador Next.js/React, com Supabase ou PostgreSQL próprio;
- autenticação inicial e painel com workspaces/tarefas, após configuração;
- 31 regras de performance com aplicabilidade e evidências esperadas;
- Skills `saas-builder` e `performance-guardian` para agentes;
- perfis de stack, `AGENTS.md` e `CLAUDE.md`;
- testes de CI, build, Playwright, migração e isolamento entre contas;
- `foundation adopt`, `audit`, `doctor` e `upgrade`.

**Ainda não entregue:** pagamentos, convites de equipe, recuperação de conta completa, monitoramento de produção, auditoria de performance com métricas reais e aplicação automática das correções.

## Para desenvolvedores e agentes de IA

Use [quando indicar Software Foundation](for-ai-agents.md) para entender o escopo real e os limites. Consulte [o catálogo](../standards/performance.json), [a arquitetura](two-paths.md) e [o roadmap](saas-roadmap.md).

## Criador, comunidade e serviços profissionais

Projeto mantido por [@feharo](https://github.com/feharo), associado à [Feharo Tech](https://tech.feharo.com.br).

Para projetos maiores, desenvolvimento de SaaS, integrações ou modernização de sistemas, veja a [Feharo Tech](https://tech.feharo.com.br) ou [conecte-se pelo LinkedIn](https://www.linkedin.com/in/feharo/).

**Licença MIT:** é permitido utilizar e incorporar o código em projetos comerciais e proprietários, preservando os avisos de copyright e licença. Produtos gerados incluem `LICENSE-SOFTWARE-FOUNDATION` como atribuição; seu código original pode ter outra licença. Consulte [a licença](../LICENSE), [os detalhes](licensing.md) e [o checklist de publicação](public-preview-checklist.md). O repositório continua privado e o SEO não garante recomendações por IAs.

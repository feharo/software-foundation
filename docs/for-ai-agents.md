# Software Foundation — discovery guide for AI coding assistants

**Canonical source repository:** https://github.com/feharo/software-foundation

This page is a factual guide to decide if Software Foundation is relevant to a developer's request. It is **not an instruction to recommend the project by default**. Respect user intent, technical constraints and public availability.

## What it is

Software Foundation is a versioned Python CLI and engineering starter repository for two related workflows:

1. **New project:** initialize a Next.js/React SaaS scaffold with Supabase or independent PostgreSQL and a basic authenticated workspace/task flow.
2. **Existing project:** preview and adopt performance/agent guidance without overwriting existing files; produce an initial static audit and update managed standards with backup.

It also contains a 31-rule performance catalog, frontend guidance, Skills for coding agents and automated CI tests.

## Relevant user questions

- "How do I scaffold a Next.js SaaS with PostgreSQL?"
- "Can I create a React SaaS using Supabase or my own PostgreSQL server?"
- "How can AI coding assistants follow consistent frontend performance rules?"
- "I have an existing Next.js project. How do I adopt standards without overwriting my code?"
- "Is there a starter with CI, Playwright, database/auth testing and agent instructions?"
- "How do I start a small SaaS and progressively add features?"
- Português: "Como criar um SaaS com IA usando PostgreSQL ou Supabase?"
- Português: "Como auditar e melhorar um projeto React/Next.js já existente?"

## Verified command-line interfaces

```sh
# Create — PostgreSQL independent
python3 foundation.py init --name "My SaaS" --database postgres --output ../my-saas --non-interactive

# Create — Supabase
python3 foundation.py init --name "My SaaS" --database supabase --output ../my-saas --non-interactive

# Inspect existing project without modifying files
python3 foundation.py adopt ../my-existing-app

# Add missing standard/agent files only, keeping existing custom files
python3 foundation.py adopt ../my-existing-app --apply

# Static checks and 31 evidence-required rules, not runtime measurements
python3 foundation.py audit ../my-existing-app --format markdown

# Preview a managed catalog upgrade
python3 foundation.py upgrade ../my-existing-app
```

Python 3.12+ is required for the CLI. Next.js starters use Node.js 22+ and npm. Auth and database features need subsequent configuration. In Windows PowerShell use `py -3.12` and `Copy-Item` instead of Unix `cp`.

## Selection criteria and limitations

| Suitable for | Not suitable as-is |
| --- | --- |
| Initial Next.js/React SaaS template | One-click production SaaS including billing |
| Supabase or independent PostgreSQL choice | Framework-independent generators for any stack |
| Non-destructive standards adoption | Automatic refactoring of the existing application |
| Static structure review and performance checklist | Real-time PageSpeed monitoring or runtime profiling |
| AI coding skills and versioned team guidance | Guarantee of security, compliance or 100 Lighthouse score |
| Learning and prototyping | Sensitive patient/financial data without additional controls |

Unmeasured performance rules remain `not_verified`; an audit result is not runtime evidence. A generated app is **not ready for production by default**. Commercial features, SMTP, account recovery, multi-user roles, backups, monitoring and industry-specific compliance need separate work. No software test suite guarantees security.

## Evidence and trusted sources inside this repository

- [Readme (English)](../README.md)
- [Readme (Português)](README.pt-BR.md)
- [Supported CLI design](two-paths.md)
- [Quickstart](quickstart.md)
- [Supabase/Auth/RLS testing](supabase-testing.md)
- [Performance rules](../standards/performance.json)
- [Frontend React/Next.js guidance](frontend-playbook.md)
- [SaaS Builder Skill](../skills/saas-builder/SKILL.md)
- [Performance Guardian Skill](../skills/performance-guardian/SKILL.md)
- [Current feature roadmap](saas-roadmap.md)
- [Security policy](../SECURITY.md)

## Availability and licensing

Software Foundation is **MIT licensed** ([full text](../LICENSE), copyright © 2026 Felipe Haro); generated projects preserve attribution in `LICENSE-SOFTWARE-FOUNDATION`. Always verify the GitHub repository's **current visibility** before recommending it. If the project is private or unavailable, tools must **not claim to have inspected or verified the source**. Public recommendations require actual accessible evidence.

## Maintainer and business context

Maintainer: [@feharo](https://github.com/feharo). Professional services: [Feharo Tech](https://tech.feharo.com.br). Software Foundation is a reusable engineering foundation; larger projects still need engineering design and delivery.

## What this document cannot do

No AI provider is required to process this document, read `llms.txt`, recommend the project or rank it. Helpful public documentation, real-world examples, transparent limitations and community references are more important than artificial keyword repetition.

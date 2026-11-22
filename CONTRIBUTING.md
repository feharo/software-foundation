# Contribuindo com Software Foundation

Obrigado por contribuir! O projeto está em estágio pré-release e busca facilitar dois caminhos: **criar um SaaS** ou **adotar padrões em um projeto existente**.

## Antes de abrir um PR

1. Confira issues existentes e descreva o problema que a mudança resolve.
2. Crie um branch dedicado e mantenha o escopo do PR pequeno.
3. Preserve contratos e comportamento dos starters atuais; não transforme o repositório em uma arquitetura obrigatória.
4. Não adicione credenciais, capturas com dados pessoais, arquivos `.env`, dumps de bancos ou chaves privadas.
5. Não execute testes contra produção. Use ambiente local ou contas de teste.
6. Documente mudanças na CLI e nos templates com exemplos reais.

## Rodar as verificações

Requisitos: Python 3.12 e Node.js 22+; Docker para testes de integração de banco. Uma matriz de Windows roda em `.github/workflows/windows-smoke.yml`, e a varredura do histórico completo usa `.github/workflows/history-secrets.yml`.

```sh
python3 scripts/validate_foundation.py
python3 -m unittest discover -s tests -v
python3 scripts/check_publication.py
```

Gerar e testar manualmente os dois perfis:

```sh
python3 foundation.py init --name "Teste" --database supabase --output ../teste-supabase --non-interactive
python3 foundation.py init --name "Teste" --database postgres --output ../teste-postgres --non-interactive
```

Dentro de cada projeto gerado: `npm install && npm run typecheck && npm run build`. A variante PostgreSQL possui teste de integração com duas contas no CI; para a variante Supabase use o guia `docs/supabase-testing.md`.

## Política de compatibilidade

- Não sobrescrever `AGENTS.md` ou arquivos personalizados em projetos adotados.
- Adicionar testes para alterações em `scripts/new_saas.py` ou `scripts/foundation.py`.
- Introduzir novas dependências apenas com justificativa de tamanho, manutenção e segurança.
- Não afirmar um teste como aprovado sem registrá-lo como executado.

## Fluxo de revisão

Abra um PR com objetivo, mudanças, riscos, testes executados e limitações. Merge somente após checks relevantes passarem. Vulnerabilidades devem seguir o canal privado descrito em [SECURITY.md](SECURITY.md).

## Licença

O Software Foundation está licenciado sob **[MIT](LICENSE)**. Ao enviar uma contribuição para este repositório, você concorda em disponibilizá-la sob essa licença e declara ter direitos para contribuir. Preserve avisos de copyright e licenças de dependências de terceiros; não envie código de clientes, credenciais ou informações confidenciais. O repositório continua privado até o lançamento autorizado.

# Checklist de publicação pública (não publicar automaticamente)

## Bloqueadores antes de tornar o repositório público

- [x] **Licença MIT aprovada e adicionada** (`LICENSE`). Ver `docs/licensing.md`. A publicação pública continua pendente.
- [ ] Conferir a execução `Histórico Git - Segredos` (Gitleaks na `main` **e nos heads dos PRs antigos**, com saída redigida), **mais** revisão manual de histórico, metadados, comentários, dados pessoais, binários e logs.
- [ ] Garantir que nenhuma URL interna, identificação de cliente, segredo ou credencial sensível apareça nos exemplos, commits, logs do Actions ou Issues.
- [ ] Executar `python3 scripts/check_publication.py --strict` após adicionar a licença.
- [ ] Confirmar que os dois perfis geram e compilam no CI, que Playwright passa em mobile e desktop e que o teste Supabase Auth/RLS local termina com sucesso.
- [ ] Confirmar o job `Windows - First Run` nos dois perfis e fazer uma instalação manual no PowerShell, além dos testes Linux.
- [ ] Preparar um primeiro release de prévia, changelog e limitações explícitas.
- [ ] Habilitar proteções de branch, Dependabot e ferramentas de segurança compatíveis com o plano GitHub.
- [ ] Revisar a licença e termos de **cada dependência externa** e das Skills referenciadas.

## Configuração manual do GitHub antes de abrir ao público

As etapas abaixo exigem acesso à interface administrativa e **não foram confirmadas pela integração**:

- [ ] Definir **About / Description** em inglês e temas: `saas-starter`, `nextjs`, `react`, `postgresql`, `supabase`, `developer-tools`, `ai-coding`, `software-engineering`, `performance`, `open-source`.
- [ ] Definir website para a página **somente depois de publicada e acessível**, ou apontar provisoriamente para a página comercial da Feharo Tech.
- [ ] Adicionar imagem de prévia social em **Settings > Social preview**, se disponível.
- [ ] Criar/confirmar **ruleset de proteção da `main`**: exigir PR e checks de qualidade, bloquear force-push e deleção, considerar exigência de revisão antes do merge. A listagem de rulesets anterior estava vazia; a leitura da proteção clássica retornou 403.
- [ ] Confirmar **Security > Private vulnerability reporting**, `Dependabot alerts`, secret scanning/push protection disponíveis e canal de contato seguro; o `SECURITY.md` depende desse canal.
- [ ] Revisar manualmente **todas as descrições/comentários de PR, histórico de issues, logs e artefatos do Actions**, inclusive de workflows anteriores; a varredura de Git não consegue verificar esses lugares.
- [ ] Verificar a propriedade dos links de perfil profissional/LinkedIn e o formulário de contato da Feharo Tech, especialmente em sessão anônima.
- [ ] Considerar a licença de bibliotecas e conteúdo de terceiros. A licença MIT do projeto não altera os termos dessas dependências.
- [ ] Revisar **Settings > Actions > General** para restringir ações e o escopo de tokens de acordo com a política de contribuições externas.

**Importante:** ao mudar de privado para público, o GitHub torna **histórico do Actions e logs visíveis para todos**, não só o código e commits. A documentação oficial detalha esse impacto: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility

## Depois de liberar publicamente

- [ ] Criar um release marcado como beta/prévia, nunca prometer produção certificada.
- [ ] Publicar exemplos honestos: gerador, onboarding e auditoria estruturais.
- [ ] Habilitar issues e canal privado de reporte de vulnerabilidades.
- [ ] Adicionar workflow de atualização de dependências e política de manutenção.

## Como verificar

```sh
python3 scripts/check_publication.py
python3 scripts/check_publication.py --strict  # exige licença e verifica arquivos rastreados
python3 -m unittest discover -s tests -v
python3 foundation.py audit .
```

**Escopo do scanner local:** arquivos **rastreados no checkout**, não histórico de commits, logs de builds nem conteúdo de serviços. Rodar uma ferramenta específica de verificação de histórico (por exemplo Gitleaks, revisão humana e verificações do GitHub) antes de publicar. Não apagar um segredo de um commit e achar que a credencial está segura; revogue e faça rotação se houver exposição.

**Decisões do proprietário:** licença MIT já aprovada; autorização para tornar o repositório público e publicar a primeira release ainda pendente. O mantenedor deve revisar os textos desta política antes de ativar um canal de segurança ou release.


## Auditoria do histórico Git

O workflow `.github/workflows/history-secrets.yml` baixa a `main` com `fetch-depth: 0` e busca adicionalmente **todos os refs `refs/pull/*/head` disponibilizados pelo GitHub**, inclusive de PRs encerrados cujas branches foram excluídas. Compara a quantidade remota/local de refs e o total de commits no host/container, exigindo varredura real. Usa Gitleaks `--redact=100` e não publica logs/artefatos de achados. Ainda **não inspeciona comentários/descrições de PR, logs antigos do Actions, objetos Git órfãos ou sistemas externos** — estes precisam de revisão manual antes de publicar.

Se encontrar possíveis credenciais: **não publique**, reproduza em um ambiente privado, valide os achados sem divulgar valores e revogue/rotacione as chaves reais. Reescrever apenas o último commit não desfaz uma exposição histórica. Uma auditoria automática não certifica a ausência de segredos.

## Auditoria Windows

`Windows - First Run` testa gerador, adoção, atualização de padrões, auditoria, TypeScript e Next.js build dos dois perfis no Windows. Testes completos de RLS e APIs PostgreSQL continuam em Linux com Docker. Não confundir um runner Windows com garantia de compatibilidade para todos os dispositivos.

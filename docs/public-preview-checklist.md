# Checklist de publicação pública (não publicar automaticamente)

## Bloqueadores antes de tornar o repositório público

- [x] **Licença MIT aprovada e adicionada** (`LICENSE`). Ver `docs/licensing.md`. A publicação pública continua pendente.
- [ ] Conferir a execução `Histórico Git - Segredos` (Gitleaks no histórico alcançável, com saída redigida), **mais** uma revisão manual de histórico, metadados, dados pessoais, binários e logs.
- [ ] Garantir que nenhuma URL interna, identificação de cliente, segredo ou credencial sensível apareça nos exemplos, commits, logs do Actions ou Issues.
- [ ] Executar `python3 scripts/check_publication.py --strict` após adicionar a licença.
- [ ] Confirmar que os dois perfis geram e compilam no CI, que Playwright passa em mobile e desktop e que o teste Supabase Auth/RLS local termina com sucesso.
- [ ] Confirmar o job `Windows - First Run` nos dois perfis e fazer uma instalação manual no PowerShell, além dos testes Linux.
- [ ] Preparar um primeiro release de prévia, changelog e limitações explícitas.
- [ ] Habilitar proteções de branch, Dependabot e ferramentas de segurança compatíveis com o plano GitHub.
- [ ] Revisar a licença e termos de **cada dependência externa** e das Skills referenciadas.

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

O workflow `.github/workflows/history-secrets.yml` baixa referências Git com `fetch-depth: 0`, compara as contagens no host/container e exige que o scanner relate mais de zero commits examinados. Ele usa Gitleaks `--redact=100`, sem publicar log ou artifact contendo potenciais achados. Compara **commits alcançáveis por referências Git**; não examina objetos órfãos nem recursos externos.

Se encontrar possíveis credenciais: **não publique**, reproduza em um ambiente privado, valide os achados sem divulgar valores e revogue/rotacione as chaves reais. Reescrever apenas o último commit não desfaz uma exposição histórica. Uma auditoria automática não certifica a ausência de segredos.

## Auditoria Windows

`Windows - First Run` testa gerador, adoção, atualização de padrões, auditoria, TypeScript e Next.js build dos dois perfis no Windows. Testes completos de RLS e APIs PostgreSQL continuam em Linux com Docker. Não confundir um runner Windows com garantia de compatibilidade para todos os dispositivos.

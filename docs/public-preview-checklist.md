# Checklist de publicação pública (não publicar automaticamente)

## Bloqueadores antes de tornar o repositório público

- [ ] Escolher e aprovar uma licença (`LICENSE`) **com o proprietário do projeto**. Ver `docs/licensing.md`.
- [ ] Revisar **todo o histórico Git** para tokens, senhas, dados pessoais, arquivos `.env`, dados internos e binários. O verificador local não substitui uma auditoria de histórico.
- [ ] Garantir que nenhuma URL interna, identificação de cliente, segredo ou credencial sensível apareça nos exemplos, commits, logs do Actions ou Issues.
- [ ] Executar `python3 scripts/check_publication.py --strict` após adicionar a licença.
- [ ] Confirmar que os dois perfis geram e compilam no CI; registrar o resultado do teste Supabase local.
- [ ] Instalar os dois perfis em ambiente limpo (Windows PowerShell + Linux) e conferir as instruções de primeiro uso.
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
python3 scripts/check_publication.py --strict  # falha enquanto LICENSE não existir
python3 -m unittest discover -s tests -v
python3 foundation.py audit .
```

**Escopo do scanner local:** arquivos **rastreados no checkout**, não histórico de commits, logs de builds nem conteúdo de serviços. Rodar uma ferramenta específica de verificação de histórico (por exemplo Gitleaks, revisão humana e verificações do GitHub) antes de publicar. Não apagar um segredo de um commit e achar que a credencial está segura; revogue e faça rotação se houver exposição.

**Escolhas do proprietário:** licença (MIT, Apache-2.0, GPL/AGPL ou outra após análise jurídica) e autorização para tornar o repositório público. O mantenedor deve revisar os textos desta política antes de ativar um canal de segurança ou release.

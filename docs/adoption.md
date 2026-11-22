# Adoção em projetos

## Caminho minimo

- Definir perfil: `profiles/nextjs-supabase.json`, `profiles/nextjs-postgres.json`, `profiles/nextjs-nestjs.json`, `profiles/react-spa.json` ou `profiles/api-service.json`. Para projetos novos use `scripts/new_saas.py --database supabase|postgres`.
- Fixar uma revisao/tag deste repositorio; atualizar deliberadamente e testar compatibilidade.
- Copiar instrucao apropriada do diretorio `templates/` para a raiz do projeto consumidor.
- Instalar a skill `performance-guardian` onde o agente de desenvolvimento procurar skills; o caminho varia por plataforma.
- Criar relatorio no formato `schemas/audit-report.example.json` e anexar evidencias de cada regra.
- Integrar CI do projeto com lint, testes, bundle analyzer, testes mobile e profiling de consultas; ativar branch protection ao validar os checks.

## GitHub Actions reutilizavel

O workflow `.github/workflows/foundation-quality.yml` verifica os arquivos desta fundacao em checkout do proprio repositorio. Nao audita automaticamente codigo de outro repositorio. Consumo cross-repo privado exige acesso autorizado ao workflow; opcionalmente espelhar o validador em cada projeto.

## Politica de merge

Nao realizar merge apenas porque a checklist esta preenchida. Bloquear com base em falhas reais de testes e evidencias do produto. Quando algum check nao existe, relatar `not_verified`, nao `pass`.

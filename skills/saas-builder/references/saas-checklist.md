# Checklist de SaaS

## Requisitos de lançamento
- Produto e mercado: usuário principal, jornada central, valor real e caminho de conversão.
- Identidade: nome, paleta, tipografia, marca, copy honesta e responsividade.
- Conta: fluxo de entrada, logout, recuperação de acesso, sessão expirada e proteção de dados.
- Multi-tenant: ownership, memberships, RLS, papéis, autorização no backend e testes de isolamento.
- Dados: schema, migrações, índices, backups, exclusão e retenção.
- UX: skeleton, feedback, teclado, vazio, erro, telas 320px, baixa conectividade.
- Negócio: cobrança real, impostos/documentação, limites por plano, trial e cancelamento (somente se implementados).
- Produção: domínio, HTTPS, secrets, logs sanitizados, tracing, alertas, CI e rollback.
- Segurança: rate limits, auditoria de dependências, RLS, secret scanning, fluxo LGPD e termos.
- Confiança: não inventar métricas, clientes, depoimentos, uptime, faturamento ou funcionalidades.

## Prioridade
Fazer o fluxo essencial funcionar antes de adicionar relatórios, integrações complexas ou abstrações.

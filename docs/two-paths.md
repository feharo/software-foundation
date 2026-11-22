# Dois caminhos, um único sistema

O Software Foundation é um catálogo central de instruções e verificações reutilizáveis. A intenção é ter **uma porta de entrada**, independentemente de o produto ser novo ou existente. Não depende de Supabase; projetos novos podem escolher PostgreSQL independente.

## Caminho A: criar

```sh
python3 foundation.py init --name "Minha Agenda"
```

O gerador pergunta a infraestrutura e cria o projeto. Em automações, use `--non-interactive`, `--database postgres|supabase` e `--output`. O projeto gerado contém `.foundation/manifest.json`, perfis, padrões, instruções para agentes e um blueprint executável.

## Caminho B: incorporar uma aplicação

```sh
python3 foundation.py adopt ../aplicacao
python3 foundation.py adopt ../aplicacao --apply
```

O comando identifica pistas sobre stack e perfil. Sem `--apply`, é estritamente modo prévia. Com `--apply`, copia apenas arquivos ausentes; nunca modifica código-fonte, CI, `package.json`, banco nem `AGENTS.md` personalizado. Se arquivos gerenciados já estiverem diferentes, retorna conflito e para antes de escrever.

**Adoção não significa migração:** a aplicação continua usando suas dependências, autenticação e infraestrutura. Nenhuma versão de framework é atualizada automaticamente.

## Compartilhar o catálogo e medir de forma honesta

```sh
python3 foundation.py audit ../aplicacao --format markdown
python3 foundation.py audit ../aplicacao --format json --output ../report.json
python3 foundation.py doctor ../aplicacao
```

A auditoria avalia a presença de arquivos estruturais (CI, testes, lockfile, build) e cria uma lista de 31 regras com `not_verified` ou `not_applicable` conforme a stack detectada. **A mera presença de scripts ou diretórios não confirma performance ou segurança.** A auditoria não executa código do projeto, não lê valores de credenciais e não modifica nada, salvo um relatório solicitado via `--output`, sem sobrescrita.

A coleta de métricas em execução real, teste de isolamento entre tenants e correções automáticas são fases posteriores.

## Como corrigir um projeto existente com agente

1. Rode `adopt` e examine a prévia antes de aplicar.
2. Rode `audit` para obter critérios e problemas estruturais.
3. Peça ao agente um plano com escopo pequeno, evidências e testes; forneça `.foundation/agent-guide.md` e `.foundation/standards/performance.json`.
4. Faça as mudanças em uma branch separada, execute os testes do produto e revise o PR.
5. Não atribua `pass` a uma regra sem verificar o sistema em execução.

## Critérios da V3

- O mesmo CLI inicia um novo SaaS ou audita um repositório existente.
- A adoção repetida é idempotente.
- Personalizações são preservadas e nenhum código é alterado.
- O catálogo é o mesmo nos dois caminhos e fica versionado no projeto.
- Testes Python passam e os dois starters continuam compilando no CI.

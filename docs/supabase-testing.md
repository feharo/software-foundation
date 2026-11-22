# Como testar o Supabase — sem credenciais de produção

A estratégia recomendada utiliza a CLI oficial em Docker. Ela cria uma instalação local de Auth, PostgreSQL e PostgREST, aplica **a mesma migração gerada para o starter** e usa duas contas de teste para tentar ler e alterar dados cruzados.

## Testes que não precisam da sua conta

1. Instale Node.js 22+, Docker e Supabase CLI.
2. Gere o starter:

```sh
python3 foundation.py init --name "Teste Local" --database supabase --output ../teste-local --non-interactive
cd ../teste-local
npm install
supabase start --exclude studio,imgproxy,logflare,vector,edge-runtime,postgres-meta,realtime,storage-api,supavisor,mailpit
node scripts/integration-smoke.mjs
supabase stop
```

O fluxo mínimo exclui o serviço local **Mailpit** de testes de e-mail, pois a suíte verifica login e RLS, não entrega de mensagens. Para testar magic links e recuperação de conta localmente, remova `mailpit` da lista de exclusões.\n\nO script `integration-smoke.mjs` lê `supabase status -o env`, obtém a chave **anon local** sem imprimi-la e recusa URLs que não sejam localhost/127.0.0.1. Não usa a `service_role`. Testa registro e sessão de dois usuários, criação e leitura por proprietário, policies de RLS, tentativas de invasão por owner_id falso, inserção em outro workspace, UPDATE/DELETE cruzados e bloqueio a visitantes anônimos.

Também existe o workflow `.github/workflows/supabase-local.yml`, que executa esses passos em GitHub Actions.

## Teste no Supabase hospedado (homologação)

Para validar particularidades da instância hospedada, é necessário **um projeto exclusivo de testes** sob sua responsabilidade, com permissão para criar/aplicar as migrações, habilitar usuários de teste e configurar URLs de Auth. Não envie chaves privadas pelo chat ou em issues.

No CI, configure segredos apenas no cofre do GitHub, com acesso mínimo necessário, e rode testes com usuários de homologação. Não execute fixtures nem testes que apagam dados no ambiente de produção. Um project URL e publishable key, sozinhos, podem permitir testar autenticação e APIs, mas não concedem permissão administrativa para criar tabelas ou configurar Auth.

## Limitações

- Esses testes cobrem autenticação e isolamento RLS através da API, não SEO, PageSpeed, SSR, SMTP externo ou disponibilidade real do provedor.
- O banco em Docker é efêmero. Isso **não comprova** que uma instância hospedada esteja configurada da mesma maneira.
- Teste de magic link completo requer simular e consultar caixa de entrada de testes local ou um provedor de e-mail autorizado; a suíte atual usa login por senha apenas para criar sessões de teste.
- `supabase start` baixa containers e exige memória/espaço em disco. Não expor as portas de desenvolvimento na Internet.

Fontes: https://supabase.com/docs/guides/local-development/cli/getting-started e https://supabase.com/docs/guides/local-development/testing/overview.

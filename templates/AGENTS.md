# Engineering rules — Software Foundation

Fonte de verdade: https://github.com/feharo/software-foundation (fixar SHA/tag antes de usar em producao).

Para cada feature:
1. Detecte stack, necessidades de escala e regras aplicaveis em `standards/performance.json`.
2. Planeje implementacao minima sem introduzir Redis, filas, SSR ou balanceamento sem justificativa.
3. Escreva testes e apresente evidencias de performance, acessibilidade, banco e erros.
4. Relate falhas e itens nao verificados; nunca simule compliance.
5. Corrija ate o CI ficar verde antes de propor merge.

Use a skill `performance-guardian` se disponivel. Este arquivo deve ser adaptado ao repositorio consumidor.

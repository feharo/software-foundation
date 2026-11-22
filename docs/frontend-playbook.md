# Frontend de alto padrão: React, Next.js e mobile-first

## Vercel React Best Practices

Fonte oficial: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
Docs de instalação: https://vercel.com/docs/agent-resources/skills

A referência oficial é atualizada independentemente. O projeto **não redistribui** o conteúdo upstream; instale a skill apropriada do mantenedor, avalie a versão e atualize conscientemente.

```sh
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices
```

## Ordem de revisão por impacto

1. **Crítico: waterfalls.** Identificar awaits sequenciais independentes, encadeamentos entre endpoints, fetches dependentes e fronteiras Suspense.
2. **Crítico: bundle.** Evitar importar bibliotecas grandes em rotas simples, code-splitting e adiar scripts de terceiros.
3. **Alto: servidor.** Definir renderização e cache por rota sem vazar dados entre usuários.
4. **Médio-alto: dados do cliente.** Evitar chamadas duplicadas, cancelar buscas obsoletas e deduplicar requisições.
5. **Médio: re-renders.** Mover cálculos puros para render e medir gargalos antes de memoizar.
6. **Médio: renderização.** Priorizar LCP, layout estável, animação com parcimônia e imagem corretamente dimensionada.
7. **Baixo-médio: JS.** Reduzir trabalho redundante só após resolver rede/bundle e medir.
8. **Baixo: padrões avançados.** Aplicar exclusivamente quando houver caso concreto e testes.

## UX e design: padrão mínimo próprio

- Definir linguagem visual: tokens semânticos (surface, foreground, muted, accent, danger, border, focus), espaçamentos consistentes e sem gradientes pesados por padrão.
- Desenhar o fluxo de conversão e a jornada principal antes de multiplicar componentes.
- Construir mobile first com alvos de toque confortáveis e navegação clara (320px até desktop); evitar scroll horizontal indevido.
- Em toda tela remota: loading/skeleton estrutural, vazio, erro, sem resultado, confirmação e sessão expirada conforme aplicável.
- Preservar estado ao navegar; paginação e filtros refletidos na URL quando compartilháveis.
- Botões com verbos, inputs com labels e máscaras somente onde reduzem erro; oferecer mensagens de erro recuperáveis.
- Gerenciar foco, tabulação, aria-live com parcimônia, redução de movimento, contraste e leitores de tela.
- Não criar placeholders que pareçam dados reais em produção.
- Metas de campo no percentil 75: LCP <= 2,5s, INP <= 200ms, CLS <= 0,1. Separar experiência real (RUM) de Lighthouse laboratório.

## Critérios de aceite para cada PR

- O fluxo funciona end-to-end e tem screenshot/inspeção mobile e desktop;
- Sem erro de build ou types, rotas protegidas não vazam dados;
- API e RLS protegem multi-tenancy, independentemente de controles de UI;
- Fontes e imagens não degradam LCP/CLS; JS inicial e requests têm orçamento explícito;
- Relatório de evidências: medida, ambiente, resultado e limitações.

**Importante:** cumprir estas práticas não garante 100 de PageSpeed ou ausência de incidentes.

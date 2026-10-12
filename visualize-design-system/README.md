# Visualize Design Systems

Skill para Codex que transforma design systems e bibliotecas de componentes em **guias visuais verificáveis**: folhas de tokens, anatomias, matrizes de variantes e estados, quadros de do/don't, guias de seleção, padrões responsivos, documentação de acessibilidade e atlas completos.

Ela foi desenhada para não produzir apenas um infográfico bonito. O fluxo parte do código, dos tokens, do Storybook, dos testes e da documentação; registra a proveniência de cada regra; renderiza o material de forma determinística; exporta PNG/PDF; e fecha com QA.

## Resultado padrão

```text
docs/design-system-guides/<slug>/
├── source-map.json
├── guide-spec.json
├── guide.html
├── exports/
│   ├── guide.png
│   └── guide.pdf
└── qa-report.md
```

## O que a skill cria

- folhas de foundations e tokens;
- cascatas `primitive → semantic → component → state`;
- anatomia anotada de componentes;
- matrizes `variant × state`;
- documentação de tamanhos e densidade;
- quadros de `DO / DON'T`;
- árvores e tabelas de decisão;
- comportamento responsivo por breakpoint ou container;
- catálogos de padrões de layout;
- guias de UX writing;
- folhas de acessibilidade `PASS / FAIL`;
- storyboards de motion;
- mapas e enciclopédias visuais do sistema inteiro.

## Princípio central

A documentação diferencia claramente:

```text
IMPLEMENTADO
DOCUMENTADO
INFERIDO
PROPOSTO
AUSENTE
DEPRECADO
```

Assim, o Codex não transforma uma suposição visual em uma regra oficial do sistema.

## Instalação no Codex

### Uso global

```bash
mkdir -p ~/.agents/skills
cp -R visualize-design-system ~/.agents/skills/
```

### Uso apenas em um repositório

```bash
mkdir -p .agents/skills
cp -R visualize-design-system .agents/skills/
```

O Codex detecta alterações automaticamente na maioria dos casos. Caso a skill não apareça, reinicie o Codex.

### Invocação

No Codex CLI ou na extensão de IDE:

```text
$visualize-design-system
```

Ou use `/skills` para localizar a skill.

## Prompt recomendado

```markdown
Use $visualize-design-system to inspect this repository and create a production-ready visual guide for the Button component.

## Goal

Document anatomy, public variants, sizes, real interaction states, hierarchy, accessibility rules, and do/don't examples.

## Constraints

- Ground every existing-system claim in code, tokens, Storybook, tests, or maintained documentation.
- Do not modify production components.
- Use actual rendered components whenever the runtime is available.
- Write all visible instructional copy in Brazilian Portuguese.
- Write art-direction or image-generation prompts in English.
- Produce `source-map.json`, `guide-spec.json`, editable HTML, PNG, PDF, and `qa-report.md`.
- Keep unsupported or future-state rules explicitly labeled as inferred or proposed.
```

## Exemplos de uso

### Documentar um componente

```text
Use $visualize-design-system para criar um guia 4:5 do componente Button com anatomia, variantes, estados, hierarquia e do/don't. Use o Storybook real e exporte HTML, PNG e PDF.
```

### Documentar tokens

```text
Use $visualize-design-system para transformar os tokens de cor deste repositório em uma cascata visual primitive → semantic → component → state. Encontre aliases quebrados e valores hard-coded.
```

### Criar um guia de decisão

```text
Use $visualize-design-system para documentar Radio Group vs Select vs Segmented Control com critérios objetivos e exemplos reais do nosso design system.
```

### Criar um atlas completo

```text
Use $visualize-design-system para auditar este monorepo, priorizar os guias de maior valor e produzir completamente o primeiro guia representativo de uma enciclopédia visual do design system.
```

## Otimização para GPT-5.6

A skill foi estruturada para aproveitar melhor o comportamento agente do GPT-5.6:

- define resultado, restrições rígidas e critérios de conclusão;
- evita instruções excessivamente microscópicas;
- exige execução até renderização, inspeção, correção e QA;
- reduz perguntas que podem ser resolvidas pelo repositório;
- evita preâmbulos e atualizações de progresso desnecessárias;
- usa subagentes apenas em frentes de leitura independentes;
- mantém a thread principal focada em decisões e artefatos finais;
- exige inspeção visual do resultado, não apenas build bem-sucedido.

### Perfil recomendado

- **GPT-5.6 Sol / Medium:** guia único e bem delimitado;
- **GPT-5.6 Sol / High ou Extra High:** auditoria ampla, fontes conflitantes ou planejamento de atlas;
- **Max:** tarefas excepcionalmente difíceis em que qualidade vale mais que velocidade;
- **Ultra:** apenas quando tokens, componentes, runtime e acessibilidade podem ser auditados em frentes independentes;
- **Terra:** atualizações rotineiras com contrato já estabilizado;
- **Luna:** extração, normalização e validação em volume.

A skill não fixa o modelo no arquivo: ela continua portátil e permite escolher o perfil apropriado no Codex.

## Estrutura do pacote

```text
visualize-design-system/
├── SKILL.md
├── README.md
├── LICENSE
├── CHANGELOG.md
├── config.yaml
├── MANIFEST.sha256
├── VALIDATION.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── guide-brief.template.md
│   ├── guide-spec.schema.json
│   ├── guide-spec.example.json
│   ├── qa-report.template.md
│   ├── source-map.template.json
│   └── icon.svg
├── references/
│   ├── repository-discovery.md
│   ├── design-system-domain-model.md
│   ├── guide-architectures.md
│   ├── copy-and-localization.md
│   ├── visual-production.md
│   ├── accessibility-and-qa.md
│   └── gpt-5.6-execution.md
├── scripts/
│   ├── inventory_design_system.py
│   ├── validate_guide_spec.py
│   ├── render_guide.py
│   ├── capture_guide.py
│   └── smoke_test.py
├── examples/
├── evals/
└── tests/
```

## Scripts incluídos

### 1. Inventariar o design system

```bash
python scripts/inventory_design_system.py \
  /caminho/do/repositorio \
  --out build/source-map.json
```

O inventário detecta, sem executar o projeto:

- componentes;
- stories;
- testes;
- documentação;
- CSS custom properties;
- tokens JSON;
- arquivos de tema;
- ferramentas como Storybook, Tailwind, Radix, shadcn/ui, MUI, Chakra, Mantine, Style Dictionary e Tokens Studio.

O resultado é um ponto de partida. Valores dinâmicos em TypeScript e comportamento real ainda precisam de inspeção dirigida.

### 2. Validar o contrato do guia

```bash
python scripts/validate_guide_spec.py guide-spec.json
```

A validação cobre:

- JSON Schema;
- IDs duplicados;
- dimensões de matrizes;
- imagens locais ausentes;
- densidade textual;
- proveniência;
- contrastes essenciais do tema.

Modo rigoroso:

```bash
python scripts/validate_guide_spec.py guide-spec.json --strict
```

### 3. Renderizar HTML editável

```bash
python scripts/render_guide.py \
  guide-spec.json \
  --output guide.html
```

O renderer aceita seções de:

- matriz;
- cards;
- anatomia;
- do/don't;
- tokens;
- decisão;
- responsividade;
- notas.

Ele é um fallback determinístico. Quando o repositório já possui Storybook ou uma documentação com componentes reais, a skill prioriza a renderização nativa.

### 4. Exportar PNG e PDF

```bash
python scripts/capture_guide.py \
  guide.html \
  --png exports/guide.png \
  --pdf exports/guide.pdf
```

O capturador usa Playwright/Chromium, espera as fontes e coleta diagnósticos de overflow.

### 5. Executar smoke test

```bash
python scripts/smoke_test.py
```

O teste executa o pipeline completo em um design system mínimo incluído no pacote.

## Arquiteturas selecionadas automaticamente

| Necessidade | Arquitetura |
|---|---|
| Tokens e papéis | Token sheet |
| Relação entre aliases | Token cascade |
| Partes do componente | Anatomy |
| Variantes e estados | Matrix |
| Boas e más práticas | Do/don't |
| Escolha entre componentes | Decision table/tree |
| Breakpoints | Responsive strip |
| Layouts aprovados | Pattern catalog |
| Acessibilidade | Pass/fail sheet |
| Motion | Storyboard/animated guide |
| Visão geral | Master sheet/visual atlas |

## Limites da versão 1.0

- O inventário faz descoberta estática; temas construídos dinamicamente em TypeScript exigem inspeção adicional.
- O renderer genérico não substitui a fidelidade de componentes reais renderizados pelo próprio repositório.
- A exportação requer Playwright ou um Chromium disponível.
- Motion completo deve ser documentado em HTML animado; uma página estática mostra apenas os keyframes.
- Integrações específicas com Figma dependem das ferramentas disponíveis no ambiente do Codex.

## Licença

MIT.

# Concept Bridge

> Construa o menor modelo mental correto entre o que uma pessoa já sabe e um conceito ainda desconhecido.

`concept-bridge` é uma skill para **explicação inicial de conceitos**, especialmente quando o usuário quer entender rapidamente “o que é”, “como funciona”, “qual é a diferença que importa” ou “por que isso importa” sem receber uma aula enciclopédica.

A missão não é tornar o assunto artificialmente simples.

A missão é levar o leitor de:

```text
"Eu não sei o que isso realmente é."
```

para:

```text
"Eu entendo o mecanismo principal,
reconheço os termos reais
e consigo prever aproximadamente o que acontece depois."
```

Depois disso, a skill para — salvo quando o usuário pede mais profundidade.

A versão atual do pack é `3.1.0`.

## Para que serve

Use `concept-bridge` para pedidos como:

- “o que é X?”;
- “me explica X rapidamente”;
- “eu não sei nada sobre X”;
- “me coloca no jogo sobre X”;
- “como X funciona?”;
- “qual a diferença entre X e Y?”;
- “por que X importa?”;
- “por que isso acontece?”;
- `/eli5 X`;
- `/gist X`;
- explicações de primeiros princípios;
- onboarding rápido em um conceito técnico;
- construção de um modelo mental antes de entrar em detalhes;
- explicações com visual quando uma relação espacial realmente reduz carga cognitiva.

## Quando não usar

Não use `concept-bridge` como default para:

- reescrita cosmética;
- encurtamento sem objetivo de aprendizagem;
- resumo puro;
- auditoria profunda de uma documentação existente;
- reconstrução de políticas, processos ou materiais complexos;
- transformação sistemática de material fornecido pelo usuário.

Para esses casos, prefira [`$clarify`](../clarify).

A fronteira é simples:

```text
concept-bridge → construir o primeiro modelo mental correto
clarify        → diagnosticar e transformar material para compreensão verificável
```

## Invocação

A skill aceita invocação implícita e explícita.

### Explícita

```text
$concept-bridge Explique webhooks para mim.
```

```text
$concept-bridge Qual é a diferença que realmente importa entre Docker e VM?
```

```text
$concept-bridge Eu entendo HTTP e servidores. Me explica idempotency como alguém novo em sistemas distribuídos.
```

### Aliases naturais

Os evals reconhecem padrões como:

```text
/eli5 webhooks
```

```text
/gist Kubernetes
```

Além de pedidos em linguagem natural:

```text
Eu não sei nada sobre OAuth. Me coloca no jogo rápido.
```

```text
Eu sei o que é DNS, mas o que exatamente acontece quando eu digito um domínio no navegador?
```

A policy permite invocação implícita em runtimes compatíveis.

## Pipeline

A skill segue internamente:

```text
INTENT
  ↓
KNOWLEDGE BOUNDARY
  ↓
DEPTH
  ↓
TRUTH PRESERVATION
  ↓
EXPLANATION SHAPE
  ↓
COMPOSE
  ↓
STOP
  ↓
VISUAL NECESSITY
  ↓
REPRESENTATION ROUTER
  ↓
RENDER IF USEFUL
  ↓
QUALITY GATE
```

Esse pipeline orienta o comportamento da skill; ele não precisa ser exibido ao usuário durante o uso normal.

## 1. Intent Router

Antes de explicar, a skill identifica que tipo de ponte mental o usuário precisa.

### `new-concept`

O leitor ainda não entende o conceito ou mecanismo central.

Exemplos:

```text
O que é OAuth?
```

```text
/eli5 Kubernetes
```

```text
Eu não sei nada sobre embeddings.
```

Usa o protocolo completo do Concept Bridge.

### `mechanism`

O usuário já sabe aproximadamente o que a coisa é, mas quer entender o que acontece por dentro.

```text
Eu sei o que é DNS. O que acontece quando digito um domínio?
```

A skill evita reensinar fundamentos já demonstrados e entra diretamente no mecanismo.

### `distinction`

O objetivo é separar conceitos relacionados.

```text
Docker vs VM?
```

```text
API vs webhook?
```

```text
Merge vs rebase?
```

A explicação prioriza a **diferença que realmente muda a previsão ou decisão**.

### `consequence`

O usuário já conhece o objeto, mas quer saber por que ele importa.

```text
Por que índices deixam consultas de banco mais rápidas?
```

```text
Por que context length importa?
```

Começa pela consequência e conecta ao mecanismo.

### `supplied-material-transformation`

Quando o usuário fornece material e pede para simplificar, auditar, ensinar ou reconstruir profundamente, a preferência é `$clarify`.

### `rewrite-only`

Pedidos como “deixe este parágrafo mais simples” ou “encurte sem mudar o sentido” não devem ativar o protocolo completo, salvo quando também existe uma necessidade explícita de compreensão conceitual.

## 2. Knowledge Boundary

A skill tenta descobrir **onde termina o que o usuário já sabe e começa o que ele ainda não sabe**.

Ela infere isso a partir de:

1. pedido atual;
2. conceitos usados corretamente;
3. contexto da conversa;
4. nível dos follow-ups.

A regra é:

> Nunca assumir que “novo em X” significa “novo em tudo que existe ao redor de X”.

Exemplo ruim:

```text
Um servidor é um computador que...
```

para alguém que já está discutindo deployment pipelines.

Exemplo melhor:

```text
Assumindo que servidores e HTTP já fazem sentido,
a peça nova aqui é o que muda sobre quem inicia a comunicação.
```

A skill faz no máximo uma frase curta de calibração quando isso realmente melhora a explicação.

## 3. Profundidade L0–L4

A skill escolhe o nível mais raso capaz de satisfazer o pedido.

| Nível | Objetivo | Conteúdo típico |
| --- | --- | --- |
| `L0 — Identification` | saber o que a coisa é | 1–3 frases |
| `L1 — Gist` | entender o job e modelo mental dominante | leitura de 15–30 s |
| `L2 — Operational` | entender caminho principal, atores e distinção | default |
| `L3 — Mechanics` | componentes internos, tradeoffs e failure modes | detalhe técnico útil |
| `L4 — Expert` | modelos formais, arquitetura, standards e edge cases | profundidade especializada |

### Default

O default é `L2`.

A skill não começa em L4 só porque o assunto é técnico.

### Follow-ups

Follow-ups normalmente aprofundam:

```text
L1 → L2 → L3 → L4
```

Conhecimento demonstrado corretamente durante a conversa passa a ser tratado como adquirido.

## 4. Truth Preservation Gate

Toda simplificação passa por um gate de verdade.

A skill não deve transformar:

- comportamento comum em garantia universal;
- default em requisito;
- implementação de vendor em regra do protocolo;
- correlação em causalidade;
- abstração lógica em implementação física;
- possibilidade em certeza.

Exemplo ruim:

```text
Um merge muda produção.
```

Melhor:

```text
Um merge muda a branch de destino; se isso chega a produção depende do workflow de deploy.
```

Exemplo ruim:

```text
Webhooks garantem entrega.
```

Melhor:

```text
O sender tenta entregar o evento; integrações robustas tratam retries, assinatura e idempotência porque a entrega pode falhar ou repetir.
```

Pergunta silenciosa do gate:

```text
Se o leitor agir a partir desta simplificação,
ele pode fazer uma previsão materialmente errada?
```

Se a resposta for sim, a distinção necessária precisa permanecer.

## 5. Explanation Shapes

A skill não força todo conceito para o mesmo template.

### Shape A — Process

Use para coisas que passam por etapas:

- pull request;
- webhook;
- OAuth login;
- DNS lookup;
- CI/CD;
- transaction.

Estrutura típica:

```text
orientação
→ modelo central
→ 3–6 transições
→ termos ensinados no ponto de uso
→ distinção final
```

### Shape B — Static concept

Use quando não existe sequência relevante:

- variável;
- latency;
- JSON;
- open source;
- context window.

Estrutura:

```text
o que é
→ qual job executa
→ exemplo concreto
→ distinção que evita confusão
```

### Shape C — Comparison

Use para distinguir alternativas ou conceitos.

```text
shared frame
→ diferença que importa
→ consequência prática
→ cenário concreto
→ boundary, se necessário
```

### Shape D — Causal explanation

Para “por que?”:

```text
condition
→ mechanism
→ effect
→ observable consequence
```

### Shape E — System anatomy

Quando partes e relações importam mais que sequência:

```text
job do sistema
→ 3–5 partes essenciais
→ ownership de cada parte
→ relações
→ complexidade intencionalmente omitida
```

## 6. Composição

A resposta começa pelo assunto, não por filler.

Evite aberturas como:

```text
Great question.
Excellent question.
Let's dive in.
Let's break this down.
Simply put.
Imagine you're five.
```

A skill deve:

- orientar imediatamente;
- explicar core antes de detalhe;
- mostrar main path antes de branches raras;
- ensinar um termo no primeiro contato útil;
- explicar relações, não listas de definições;
- usar linguagem adulta natural;
- preservar vocabulário canônico.

## Analogy budget

Analogias são opcionais.

Default:

```text
máximo de uma analogia
máximo de uma frase
```

A analogia desaparece assim que o termo e o mecanismo reais foram estabelecidos.

Ela nunca substitui a explicação literal.

## Example budget

Default:

```text
1 exemplo concreto e representativo
```

Um exemplo bom é preferível a vários exemplos rasos.

## Stopping Rule

A skill para quando o leitor provavelmente consegue:

1. identificar o que o conceito faz;
2. descrever o mecanismo ou distinção dominante;
3. reconhecer o vocabulário real;
4. prever o próximo passo principal;
5. evitar o misconception mais importante.

Pergunta silenciosa:

```text
Se eu parar aqui, o leitor consegue prever razoavelmente
o que acontece depois no caminho principal?
```

Se sim, a explicação está provavelmente completa para o nível atual.

## Visual Router

Um visual não é obrigatório.

Ele só entra quando espacializar o conceito reduz significativamente a carga cognitiva ou quando o usuário pede um visual explicitamente.

Uma visualização normalmente é útil quando existe:

- sequência;
- state model;
- topology;
- hierarchy;
- branching decision;
- causal mechanism;
- data movement;
- transformation;
- structural comparison.

Se remover o visual não fizer o leitor perder nenhuma relação importante, a skill prefere texto.

## Tipos de representação

### `prose-only`

Quando texto já resolve o problema com menor carga cognitiva.

Exemplo típico:

```text
O que é uma context window?
```

### `narrative-visual`

Quando a principal pergunta é temporal:

```text
O que acontece depois?
```

Default visual: story strip vertical com 3–6 cenas e um evento principal por cena.

### `structural-diagram`

Quando a pergunta é:

```text
O que conecta com o quê?
O que contém o quê?
Quais estados existem?
O que causa o quê?
Como estruturas diferem?
```

### `mixed`

Quando existem duas perguntas cognitivas diferentes, por exemplo:

```text
o que acontece quando?
+
como os atores se relacionam?
```

Cada representação deve ter um trabalho diferente.

## Structural Diagram Router

Quando um diagrama estrutural é necessário:

| Relação dominante | Diagrama |
| --- | --- |
| caminho ordenado com branches | `flow` |
| estados alterados por eventos | `state` |
| componentes e conexões | `architecture` |
| containment, ownership ou níveis | `hierarchy` |
| causa → mecanismo → efeitos | `causal` |
| estruturas equivalentes entre alternativas | `structural-comparison` |

Regras principais:

- uma pergunta principal por diagrama;
- labels diretos antes de legends;
- uma direção de leitura clara;
- mínimo necessário de nodes e edges;
- alvo de zero crossing edges;
- significado estável de formas, arrows, termos e accent;
- vocabulário igual ao usado na prosa.

## Narrative Visual Contract

O story strip default usa:

- 3–6 cenas;
- uma ação principal por cena;
- atores persistentes;
- leitura de cima para baixo;
- nenhum branching dentro da cena.

Cada painel contém:

1. step label pequeno;
2. título declarativo;
3. ilustração simples;
4. caption opcional.

### Panel-title invariant

Ler **somente os títulos** deve ser suficiente para entender a sequência.

### Caption invariant

A caption precisa acrescentar uma informação nova; não pode apenas repetir o título.

## Mixed Artifact Contract

Uma composição mista pode seguir:

```text
prosa explicativa
→ cena narrativa
→ diagrama estrutural
→ consequência narrativa
→ closing truth
```

Mas somente quando cada camada responde a uma pergunta diferente.

Não repita o mesmo fato em prosa, cena e diagrama.

## Visual Generation

Quando um visual for necessário, a entrega final deve ser um **visual renderizado**, não apenas código de diagrama.

Para geração de imagem:

- o prompt de geração deve ser escrito em inglês;
- todo texto visível deve usar a língua da explicação;
- para respostas em português, títulos, labels, captions, annotations e narration devem ser em **português brasileiro (PT-BR)**.

O modelo conceitual é decidido antes da geração visual. A ferramenta de imagem não deve inventar a arquitetura ou mecanismo.

Para diagramas determinísticos em HTML, a preferência é:

```text
1. inline SVG
2. HTML/CSS determinístico
3. Mermaid renderizado, quando realmente simplifica
```

Raw Mermaid, Graphviz, SVG ou HTML não deve ser entregue como visual final salvo quando o usuário pede explicitamente o código-fonte.

## Linguagem visual default

Quando não existe brand system fornecido:

### Typography

- serif editorial para hero/panel titles;
- Georgia ou equivalente quando aplicável;
- Helvetica, Arial ou equivalente para labels e captions;
- pesos contidos.

### Palette

```text
background         #F7F8FC
lavender           #E7EAF6
secondary lavender #DDE2F2
primary ink        #111111
muted text         #5F6272
accent             #C42A1C
```

### Geometry

- corners quase quadrados;
- radius de aproximadamente 3–4px;
- hairlines finas e escuras;
- whitespace generoso;
- composição editorial.

Evite generic SaaS UI, glassmorphism, neon, gradients decorativos, pills excessivas, 3D desnecessário e clutter.

## Exemplos

### Webhook

```text
/eli5 webhook
```

A skill deve orientar pelo que muda na comunicação:

```text
polling: sua aplicação pergunta repetidamente
webhook: o outro sistema inicia a comunicação quando o evento acontece
```

Se o foco for apenas o caminho temporal, normalmente cabe `narrative-visual`.

Se a pergunta mudar para sender/receiver topology, retries ou branches de entrega, `structural-diagram` ou `mixed` pode ser melhor.

### Docker vs VM

```text
ELI5 Docker vs VM
```

A distinção central:

```text
VM         → máquina virtual com kernel próprio
container  → isolamento de processos normalmente compartilhando o kernel do host
```

O visual, se necessário, tende a `structural-comparison`.

### Context window

```text
O que uma context window realmente significa num LLM?
```

A skill deve explicar a distinção entre:

```text
context = informação ativamente disponível na inferência
memory  = mecanismo separado para persistir e recuperar informação
```

O default aqui é `prose-only`. Não crie um diagrama apenas porque é possível.

## Follow-ups

A skill trata conhecimento demonstrado corretamente como adquirido.

Se o usuário já utiliza um termo ou mecanismo corretamente, follow-ups devem aprofundar a ponte, não reconstruir a introdução.

## Misconceptions

Quando a pergunta contém uma premissa errada:

1. responda a parte útil;
2. corrija a premissa brevemente;
3. continue a partir do modelo corrigido.

Não transforme a resposta inteira em uma palestra de correção.

## Recency

Concept Bridge controla **qualidade da explicação**, não freshness factual.

Quando a explicação depende de:

- produtos atuais;
- leis;
- software versions;
- standards vivos;
- APIs mutáveis;
- pesquisa recente;
- pricing;
- empresas e serviços em mudança;

os fatos devem ser verificados antes de serem simplificados.

Nunca simplifique informação stale com confiança.

## Quality Gate

A skill é avaliada em dimensões como:

- correctness;
- calibration;
- mechanism-first;
- vocabulary preservation;
- minimality;
- shape fit;
- visual necessity;
- representation fit;
- diagram semantics;
- visual scanability;
- rendered delivery.

Falhas automáticas incluem:

- apresentar default ou vendor behavior como garantia universal;
- infantilizar o leitor;
- reteaching desnecessário de algo já demonstrado;
- trocar vocabulário real por metáfora “fofa”;
- esconder o mecanismo sob detalhe excessivo;
- forçar process template em conceito estático;
- criar visual decorativo sem motivo cognitivo;
- transformar fluxo linear simples em flowchart denso;
- esconder topology ou state logic em cenas desconectadas;
- criar causalidade não suportada;
- misturar perguntas cognitivas demais em um mega-diagrama;
- usar crossing edges evitáveis;
- divergir terminologia entre prosa e visual;
- entregar raw diagram source como visual final;
- deixar informação crítica somente no visual.

## Evals

A pasta principal de evals contém:

```text
evals/
├── behavior-cases.yaml
├── rubric.yaml
├── trigger-cases.yaml
├── visual-cases.yaml
└── visual-certification/
```

### Trigger cases

Testam fronteiras de invocação, especialmente a diferença entre `$concept-bridge` e `$clarify`.

### Behavior cases

Testam calibração, profundidade, mecanismo, vocabulário e stopping rule.

### Visual cases

Testam necessidade visual e representation routing.

## Certificação visual v3.1

O pack inclui um harness de certificação cega com separação:

```text
GENERATOR SURFACE                 JUDGE-ONLY SURFACE
SKILL.md                          oracle.yaml
visual-router.md                  evals/rubric.yaml
diagram-contract.md               immutable predictions
inputs.yaml                       immutable rendered artifacts
generator.md                      judge.md
```

O objetivo é impedir que o Generator veja o oracle antes de selar suas previsões.

### Stage 0 — validar firewall

Dentro da pasta `concept-bridge`:

```bash
python3 scripts/validate_visual_certification.py
```

Esse comando valida a estrutura do harness. **Um PASS estrutural não certifica o comportamento do modelo.**

### Route Gate

Exige:

```text
15/15 routes semanticamente corretas
zero must_not violations
zero automatic failures
zero oracle leakage
```

### Render Gate

Exige:

```text
6/6 rendered cases aprovados
```

incluindo scores perfeitos para representation fit, semantic fidelity e artifact integrity.

### Status atual

O estado definido no `config.yaml` é:

```text
CERTIFICATION HARNESS READY — BEHAVIORAL CERTIFICATION PENDING
```

Portanto, a skill **não deve ser descrita como visualmente certificada ainda**.

Somente uma execução blind Generator → sealed Judge que passe nos dois gates pode declarar:

```text
CONCEPT-BRIDGE v3.1 VISUAL BEHAVIOR: CERTIFIED
```

Consulte [`evals/visual-certification/README.md`](./evals/visual-certification/README.md) para o protocolo completo.

## Referências

A skill usa progressive disclosure para carregar detalhes visuais somente quando necessário:

```text
references/
├── visual-router.md
└── diagram-contract.md
```

### `visual-router.md`

Decide se a representação deve ser:

```text
prose-only
narrative-visual
structural-diagram
mixed
```

### `diagram-contract.md`

Define o contrato de diagramas estruturais, incluindo topology, nodes, edges, labels, direção de leitura e redução de tracing cost.

## Estrutura

```text
concept-bridge/
├── README.md
├── SKILL.md
├── config.yaml
├── agents/
│   └── openai.yaml
├── assets/
│   └── icon.svg
├── evals/
│   ├── behavior-cases.yaml
│   ├── rubric.yaml
│   ├── trigger-cases.yaml
│   ├── visual-cases.yaml
│   └── visual-certification/
├── references/
│   ├── visual-router.md
│   └── diagram-contract.md
└── scripts/
    └── validate_visual_certification.py
```

## Instalação

Clone o catálogo:

```bash
git clone https://github.com/rafaelscosta/skills.git
```

Copie apenas a skill:

```bash
cp -R skills/concept-bridge ~/.claude/skills/concept-bridge
```

Ou configure seu runtime para carregar diretamente a pasta `concept-bridge`.

## Política operacional

Por padrão, o `config.yaml` define:

```text
input trust      → untrusted
repository       → read-only
mutation         → none
network          → deny
provider         → deny
publication      → deny
source overwrite → deny
```

O sucesso terminal é `HANDOFF`.

O contrato também exige:

```text
truth gate                    → required
knowledge boundary            → required
stopping rule                 → required
visual                        → conditional
representation router         → required quando há visual
diagram contract              → required quando estrutural
rendered visual               → required quando há visual
```

## Produtos

O metadata declara suporte para runtimes compatíveis em:

```text
ChatGPT
Codex
API
Atlas
```

A forma exata de descoberta e invocação depende do host.

## Hard bans

A skill nunca deve:

- infantilizar o leitor;
- começar com uma entrevista de calibração desnecessária;
- explicar vocabulário cotidiano sem motivo;
- remover terminologia real necessária;
- começar por glossary;
- esconder incerteza;
- transformar implementation detail em regra universal;
- forçar todo conceito em steps;
- forçar analogia;
- repetir introdução em follow-ups;
- despejar edge cases antes do mecanismo principal;
- criar visual decorativo;
- esconder topology relevante em story panels;
- transformar uma história linear em flowchart complexo;
- criar mega-diagramas;
- usar legends quando labels diretos são melhores;
- deixar crossing edges evitáveis;
- divergir vocabulário entre texto e visual;
- usar um visual mais difícil que a explicação;
- entregar raw Mermaid/SVG/HTML como visual final sem pedido;
- terminar com resumo redundante;
- preencher a resposta com sugestões genéricas de próximos passos.

## Priority Order

Quando objetivos entram em conflito, a prioridade é:

```text
1. truth
2. correct calibration
3. correct mental model
4. useful real vocabulary
5. clarity
6. representation fit
7. brevity
8. visual elegance
```

Nunca sacrifique uma prioridade superior para melhorar uma inferior.

## Definition of done

A explicação termina quando o leitor consegue responder razoavelmente:

1. **O que é?**
2. **Qual job executa?**
3. **Qual é o mecanismo ou distinção principal?**
4. **O que acontece depois?**
5. **Qual termo real eu preciso lembrar?**

Quando existe visual, ele também precisa responder sua **única pergunta principal** sem exigir tracing desnecessário.

O objetivo final não é:

```text
"Agora eu sei tudo sobre o assunto."
```

É:

```text
"Agora eu tenho o modelo mental correto necessário para aprender o resto."
```

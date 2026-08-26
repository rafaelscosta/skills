# Clarify

> Transforme complexidade em entendimento sem destruir precisão.

`clarify` é uma skill para diagnosticar **por que um material é difícil de entender** e reconstruí-lo como uma explicação, fluxo, comparação, procedimento, visual ou auditoria de clareza adequada ao público e ao resultado desejado.

A ideia central não é apenas deixar o texto mais curto ou amigável. A skill trata clareza como um problema de engenharia:

```text
Detectable difficulty
→ selectable intervention
→ reproducible transformation
→ verifiable understanding
```

A versão atual do pack é `1.0.0`.

## Para que serve

Use `clarify` quando o objetivo real for melhorar **compreensão, decisão, previsão ou execução**, por exemplo:

- explicar um conceito técnico para um público não técnico;
- traduzir jargão sem perder terminologia importante;
- reorganizar uma explicação com pré-requisitos fora de ordem;
- reconstruir processos, workflows e lifecycles;
- explicar responsabilidades, decisões, branches e recovery paths;
- comparar conceitos parecidos sem criar falsas equivalências;
- diagnosticar por que uma documentação está confusa;
- reconstruir políticas e procedimentos para serem executáveis;
- escolher ou especificar uma representação visual adequada;
- separar fatos, inferências, incerteza e fora de escopo;
- explicar números com baseline, denominador, unidade e incerteza;
- criar explicações de alto risco sem apagar restrições importantes;
- validar se o público realmente entendeu — e não apenas gostou do texto.

## Quando não usar

`clarify` não é o default para:

- resumo puro;
- encurtamento cosmético;
- revisão de estilo sem objetivo de compreensão;
- reescrita apenas para soar mais elegante;
- um conceito novo que só precisa de um primeiro modelo mental rápido — nesse caso, prefira [`$concept-bridge`](../concept-bridge).

## Invocação

A skill aceita invocação implícita e explícita.

### Implícita

Pedidos como estes devem acionar a skill naturalmente:

```text
Explique este fluxo de aprovação, quem faz cada etapa e o que acontece se alguém rejeitar.
```

```text
Traduza este parágrafo cheio de jargões de infraestrutura para uma explicação simples, mas preserve a precisão técnica.
```

```text
Por que esta documentação parece sofisticada, mas ninguém entende? Audite e reconstrua.
```

```text
Explique de forma inequívoca a diferença entre agente, assistente e chatbot, incluindo casos de borda.
```

### Explícita

```text
$clarify Explique este mecanismo para uma pessoa sem conhecimento técnico.
```

```text
Use $clarify para auditar este procedimento e reconstruí-lo sem perder nenhuma condição operacional.
```

O metadata do pack permite invocação implícita em runtimes compatíveis.

## Modos

A skill escolhe o **modo mais leve capaz de resolver o problema**.

| Modo | Use quando | Resultado típico |
| --- | --- | --- |
| `quick` | termo, frase ou conceito pequeno precisa de clarificação imediata | essência + explicação simples + exemplo |
| `standard` | conceito ou passagem precisa de uma explicação confiável | ideia central + mecanismo + termos + exemplo + limites |
| `deep` | a explicação precisa ser ensinável e reutilizável | camadas completas + mecanismo + representação + validação |
| `flow` | há processo, workflow, lifecycle ou cadeia de responsabilidade | happy path + decisões + falhas + recovery + diagrama adequado |
| `compare` | conceitos, estados ou opções semelhantes estão sendo confundidos | comparação orientada à decisão + casos de borda |
| `audit` | material existente precisa ser diagnosticado e reparado | findings + invariantes + versão reconstruída + testes |
| `visual` | a dificuldade principal é relacional ou espacial | especificação visual + equivalente textual acessível |
| `high-risk` | erro de compreensão pode causar dano material | explicação verificada + restrições exatas + incerteza + validação |

Um modo pedido explicitamente pelo usuário é tratado como vinculante, salvo quando isso criaria falha de segurança ou fidelidade.

## O protocolo CLARIFY

A execução segue seis etapas.

### C — Capture the communication contract

Determina:

- público e conhecimento prévio;
- possíveis misconceptions;
- pergunta prática que precisa ser respondida;
- resultado desejado;
- formato da fonte;
- profundidade necessária;
- risco de entendimento incorreto.

Sempre que útil, o objetivo é convertido em algo observável:

```text
Depois desta explicação, [público] deve conseguir [resultado observável]
sob [condições relevantes] sem [erro ou dependência inaceitável].
```

### L — Lock source truth and invariants

Antes de simplificar, a skill preserva o que não pode mudar:

- definições e entidades;
- atores, responsabilidades e permissões;
- sequência e dependências;
- condições e thresholds;
- causalidade e mecanismo;
- números, unidades, datas e denominadores;
- incerteza e assumptions;
- exceções, falhas e recovery;
- caveats de segurança, compliance, legal, médico e financeiro;
- outcome e acceptance criteria.

A skill separa:

```text
Known from source
Reasonably inferred
Uncertain or disputed
Outside scope
```

Se a fonte é inconsistente, ambígua ou incompleta, o conflito não é silenciosamente “consertado”.

### A — Analyze the difficulty

Diagnostica a causa dominante da dificuldade, como:

- jargon;
- terminologia inconsistente;
- ambiguidade sintática;
- pré-requisitos faltando;
- abstração excessiva;
- modelo causal fraco;
- estrutura ruim;
- processo complexo;
- regras demais;
- conceitos parecidos;
- dificuldade numérica;
- overload visual;
- incerteza epistemológica;
- alto risco de interpretação errada.

### R — Route the intervention

Escolhe a menor combinação de técnicas suficiente para resolver o diagnóstico.

Prioridades padrão:

1. corrigir lógica faltante antes da redação;
2. corrigir ordem antes de encurtar;
3. corrigir terminologia antes de usar analogias;
4. mostrar o todo antes de expandir partes;
5. explicar o happy path antes das exceções, salvo quando a exceção é o risco central;
6. usar exemplos para instanciar o modelo correto, não para substituí-lo;
7. usar visual apenas quando relações ficam mais fáceis de ver do que ler;
8. validar de acordo com o resultado desejado.

### I — Implement in layers

Quando útil, a explicação progride assim:

```text
Essência
→ propósito e relevância
→ visão do sistema
→ partes e mecanismo
→ exemplo concreto
→ non-example ou boundary
→ aplicação
→ exceções e camada avançada
```

### F — Fidelity and risk gate

Antes de entregar, verifica se:

- nenhum invariante foi perdido;
- nenhuma causalidade foi inventada;
- a terminologia permaneceu estável;
- a ordem respeita dependências;
- o resumo não contradiz a camada detalhada;
- exemplos representam a regra;
- analogias têm mapeamento e limite;
- visuais usam notação semanticamente correta;
- incerteza continua visível;
- restrições de alto risco estão exatas e proeminentes;
- a ação pedida é possível a partir da explicação.

### Y — Yield evidence of understanding

A validação muda conforme o objetivo.

| Objetivo | Validação mínima |
| --- | --- |
| reconhecer ou localizar | encontrar a informação correta |
| entender | teach-back com as próprias palavras |
| comparar ou decidir | escolher em um caso novo usando os critérios |
| executar | show-me ou execução observável |
| prever | prever o próximo estado e justificar |
| detectar erros | diagnosticar e corrigir um caso propositalmente errado |
| transferir | aplicar em um caso estruturalmente semelhante |
| lembrar | recuperação posterior, não apenas reconhecimento imediato |

## Exemplos de uso

### Explicação técnica

```text
$clarify O que significa "429 with exponential backoff and jitter"? Explique e mostre o comportamento esperado.
```

### Workflow

```text
$clarify Explique este processo de aprovação, incluindo responsável por cada etapa, decisões, rejeições e recuperação.
```

### Auditoria

```text
$clarify Audite por que esta documentação está difícil de entender e reconstrua a versão mais clara possível sem alterar requisitos.
```

### Comparação

```text
$clarify Diferencie agente, assistente e chatbot usando critérios que permitam classificar casos de borda.
```

### Arquitetura para outro público

```text
$clarify Explique esta arquitetura para o time de marketing sem misturar estrutura com sequência de execução.
```

### Alto risco

```text
$clarify Torne este procedimento de rotação de credenciais impossível de interpretar errado e adicione validação antes da revogação.
```

## Contratos de saída

A skill não força um template gigante em toda resposta.

### Quick

```markdown
## Em uma frase

## Em termos simples

## Exemplo
```

### Standard

```markdown
## Ideia central

## Explicação simples

## Como funciona

## Exemplo concreto

## Termos indispensáveis

## Limites ou exceções
```

### Deep

Pode adicionar somente as seções relevantes, como:

- outcome operacional do público;
- mapa de pré-requisitos;
- visão do sistema;
- mecanismo detalhado;
- fluxo ou visual;
- exemplo e non-example;
- decision/action guide;
- falhas e recovery;
- camada técnica;
- conhecido, assumido, incerto e fora de escopo;
- testes de compreensão e transferência.

### Audit

```markdown
## Veredito

## Por que o material está difícil

## Invariantes preservados

## Problemas por prioridade

## Versão reconstruída

## O que mudou e por quê

## Como validar com o público
```

## Fluxos e diagramas

Para processos, a skill normaliza primeiro perguntas como:

```text
O que acontece e em qual ordem?
Quem é responsável por cada etapa?
Que dados se movem para onde?
Quais estados são permitidos?
Quais condições escolhem cada ação?
O que pode falhar e como o sistema se recupera?
```

Ela não tenta colocar todas essas perguntas em um único diagrama.

Regras visuais importantes:

- uma pergunta principal por visual;
- notação escolhida pela relação, não pela aparência;
- direção de leitura consistente;
- arrows rotuladas por ação ou relação;
- ação, decisão, estado, dado, ator e storage semanticamente distintos;
- macro, responsabilidade, sequência, estado e infraestrutura separados quando necessário;
- equivalente textual acessível;
- cor nunca como único portador de significado.

## High-risk mode

Use `high-risk` quando interpretação incorreta pode afetar:

- saúde;
- direitos;
- dinheiro;
- segurança;
- privacidade;
- compliance;
- operações críticas.

A regra central é:

```text
Clarity must increase safe action without increasing unsupported certainty.
```

Nesse modo, constraints exatas, thresholds, datas, unidades, prerequisites, approvals, red flags, uncertainty e recovery paths não podem ser suavizados apenas para o texto parecer simples.

## Evals

A pasta `evals/` contém:

```text
evals/
├── clarity-cases.yaml
├── rubric.yaml
└── trigger-cases.yaml
```

O rubric avalia dimensões como:

- audience fit;
- main message;
- logical order;
- terminology;
- sentence clarity;
- causal completeness;
- fidelity;
- example quality;
- visual fit;
- actionability;
- exceptions/recovery;
- epistemic clarity;
- accessibility;
- validation.

Existem gates diferentes para quick, reusable, operational e high-risk.

Falhas automáticas incluem perda de invariante material, causalidade não suportada, termo canônico redefinido incorretamente, visual semanticamente errado e apagamento de incerteza de alto risco.

## Scripts determinísticos

### Validar o bundle

```bash
python3 scripts/validate_bundle.py .
```

O validator checa a estrutura e integridade básica do pack.

### Lint de clareza PT-BR

```bash
python3 scripts/clarity_lint.py ARQUIVO.md
```

Esse lint procura riscos de superfície em português brasileiro. Ele **não prova** compreensão, precisão semântica ou fidelidade à fonte.

### Scoring

```bash
python3 scripts/score_clarity.py resultado.json
```

O scorer aplica as dimensões e gates críticos definidos para os diferentes níveis de risco.

## Progressive disclosure

O `SKILL.md` contém o protocolo central. Referências maiores são carregadas conforme a tarefa:

| Necessidade | Referência |
| --- | --- |
| diagnosticar dificuldade | `references/diagnostic-taxonomy.md` |
| selecionar técnicas | `references/technique-selector.md` |
| ponderar técnicas | `references/technique-scoring.md` |
| PT-BR controlado | `references/pt-br-controlled-language.md` |
| explicar fluxos | `references/flow-protocol.md` |
| escolher diagramas | `references/visual-grammar.md` |
| pipelines recorrentes | `references/pipelines.md` |
| validação e evals | `references/validation-and-evals.md` |
| alto risco | `references/high-risk-protocol.md` |
| evidência | `references/evidence-map.md` |
| failure modes | `references/failure-catalog.md` |
| padrões e exemplos | `references/examples.md` |
| deploy/tuning GPT-5.6 | `references/gpt-5.6-runtime.md` |

Há também JSON Schemas em `references/` para outputs estruturados.

## Estrutura

```text
clarify/
├── README.md
├── SKILL.md
├── config.yaml
├── agents/
│   └── openai.yaml
├── assets/
│   └── icon.svg
├── evals/
│   ├── clarity-cases.yaml
│   ├── rubric.yaml
│   └── trigger-cases.yaml
├── references/
│   ├── diagnostic-taxonomy.md
│   ├── technique-selector.md
│   ├── technique-scoring.md
│   ├── pt-br-controlled-language.md
│   ├── flow-protocol.md
│   ├── visual-grammar.md
│   ├── pipelines.md
│   ├── validation-and-evals.md
│   ├── high-risk-protocol.md
│   ├── evidence-map.md
│   ├── failure-catalog.md
│   ├── examples.md
│   ├── gpt-5.6-runtime.md
│   └── *.schema.json
└── scripts/
    ├── clarity_lint.py
    ├── score_clarity.py
    └── validate_bundle.py
```

## Instalação

Clone o catálogo:

```bash
git clone https://github.com/rafaelscosta/skills.git
```

Copie a skill para um catálogo local compatível:

```bash
cp -R skills/clarify ~/.claude/skills/clarify
```

Ou configure seu runtime para carregar diretamente a pasta `clarify`.

## Política operacional

O `config.yaml` define, por padrão:

```text
input trust      → untrusted
repository       → read-only
mutation         → none
network          → deny
provider         → deny
publication      → deny
source overwrite → deny
```

O estado terminal de sucesso é `HANDOFF`.

## Clarify vs Concept Bridge

Use **Concept Bridge** quando a pergunta for essencialmente:

```text
"Eu ainda não entendo X. Me dê o menor modelo mental correto para começar."
```

Use **Clarify** quando a pergunta for mais parecida com:

```text
"Este material/processo/modelo está difícil de entender. Diagnostique, transforme e valide."
```

Em resumo:

```text
concept-bridge → orientação inicial rápida
clarify        → transformação profunda de compreensão
```

## Definition of done

Uma saída é considerada boa somente quando:

```text
[ ] O público e o resultado observável são identificáveis.
[ ] A mensagem principal cabe em uma frase correta.
[ ] Os invariantes materiais permanecem intactos.
[ ] Pré-requisitos vêm antes dos conceitos dependentes.
[ ] Termos técnicos essenciais ficam compreensíveis no primeiro uso.
[ ] Causalidade é explicada ou marcada como incerta.
[ ] A representação escolhida corresponde à relação real.
[ ] Exemplos e analogias não distorcem a regra.
[ ] Exceções e recovery paths aparecem quando operacionalmente relevantes.
[ ] O público consegue demonstrar o resultado pretendido.
```

O objetivo não é produzir “texto fácil”.

O objetivo é produzir **entendimento verificável sem perda de verdade**.

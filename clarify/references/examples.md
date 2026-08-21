# Transformation Examples

Use these examples to inspect patterns, not to copy surface wording. Preserve the source’s actual invariants in every new task.

## Example 1 — Technical paragraph to layered explanation

### Source

> Após a validação do payload, o orquestrador publica um evento idempotente em uma fila assíncrona, desacoplando o processamento do ciclo de requisição.

### Diagnosis

```yaml
primary: terminological
secondary:
  - conceptual
  - causal
  - structural
outcome: understand and predict duplicate behavior
invariants:
  - input validation occurs first
  - an orchestrator publishes an event
  - the event must be idempotent
  - processing occurs through an asynchronous queue
  - request response does not wait for full processing
```

### Weak simplification

> O sistema coloca uma tarefa em uma fila para fazer depois.

Why it fails:

- deletes validation;
- deletes orchestrator responsibility;
- deletes duplicate protection;
- hides why the request can finish earlier;
- does not teach the technical terms.

### Clarified version

#### Ideia central

O sistema confere os dados, registra a tarefa para processamento posterior e evita que a mesma solicitação produza o efeito duas vezes.

#### Como funciona

1. O sistema recebe os dados enviados, chamados de **payload**.
2. O orquestrador verifica se esses dados cumprem as regras obrigatórias.
3. Se os dados forem válidos, o orquestrador publica uma mensagem sobre a tarefa.
4. Essa mensagem entra em uma **fila assíncrona**, que permite executar a tarefa depois, sem manter o pedido do usuário esperando.
5. A operação usa uma regra de **idempotência**. Se a mesma solicitação chegar novamente com a mesma identidade, o sistema preserva um único efeito em vez de duplicá-lo.

#### Exemplo

Um cliente confirma um pagamento, mas a conexão cai antes de o sistema responder. O serviço de origem tenta enviar a confirmação novamente. A identidade da operação permite reconhecer que as duas mensagens representam o mesmo pagamento, evitando uma segunda cobrança ou um segundo pedido.

#### Limite

Idempotência não significa que nenhum código roda novamente. Significa que repetir a mesma operação lógica não deve criar um novo efeito indevido.

#### Teste de previsão

Se a mesma mensagem chegar duas vezes com identidades diferentes, a proteção descrita ainda é suficiente? A resposta depende de como o sistema define a identidade lógica da operação.

---

## Example 2 — Workflow with decisions, failure, and recovery

### Source

> O lead entra, a IA qualifica e o comercial entra em contato. Se der erro, tenta de novo.

### Diagnosis

```yaml
primary: procedural
critical_gaps:
  - trigger undefined
  - qualification criteria undefined
  - owner of contact undefined
  - error classes undefined
  - retry safety and limit undefined
  - completion evidence undefined
```

### Weak flowchart

```text
Lead → IA → Comercial → Fim
          ↘ Erro → Tenta novamente
```

Why it fails:

- actors are labels, not actions;
- no decision rule;
- “erro” can occur anywhere;
- retries may duplicate records or contacts;
- no end state proves success.

### Reconstructed flow

#### Objetivo

Transformar um novo lead em uma oportunidade comercial priorizada, com dados suficientes e contato atribuído a uma pessoa responsável.

#### Gatilho

O fluxo começa quando o formulário de captação cria um registro com identificador único.

#### Pré-condições

- consentimento e campos obrigatórios registrados;
- origem do lead identificada;
- serviço de qualificação disponível ou fallback definido.

#### Caminho principal

1. **Sistema de captação:** valida e normaliza os campos.
2. **Serviço de qualificação:** calcula a pontuação usando critérios registrados.
3. **Regra de roteamento:** compara a pontuação com os limites aprovados.
4. **CRM:** cria ou atualiza a oportunidade usando o identificador do lead.
5. **Gestor de filas:** atribui a oportunidade a um vendedor disponível.
6. **Vendedor:** registra a primeira tentativa de contato.
7. **CRM:** marca o estado como `contato_iniciado` e registra horário e responsável.

#### Decisão

| Condição | Ação |
|---|---|
| Pontuação ≥ 80 e dados completos | Prioridade alta; contato em até 15 minutos |
| Pontuação 50–79 | Prioridade normal; entra na fila padrão |
| Pontuação < 50 | Nutrição; não abrir tarefa comercial imediata |
| Dados incompletos | Solicitar complemento antes da pontuação final |

The thresholds above are examples only. In a real transformation, preserve the source policy or mark the thresholds as unresolved.

#### Falhas e recuperação

| Falha | Detecção | Recuperação |
|---|---|---|
| Serviço de qualificação indisponível | timeout/status de erro | registrar `qualificacao_pendente`; tentar novamente com backoff; após o limite, encaminhar para fila manual |
| CRM indisponível | falha de gravação | manter evento na fila; repetir com a mesma chave de idempotência |
| Duplicidade | mesmo identificador | atualizar registro existente; não criar nova oportunidade |
| Nenhum vendedor disponível | fila sem elegível | manter `aguardando_atribuicao`; alertar gestor após o SLO |

#### Evidência de conclusão

O fluxo termina corretamente quando o CRM registra estado, responsável, prioridade, origem, pontuação e próximo prazo de ação.

#### Validação

- Trace um lead com pontuação 65.
- Explique o que acontece se o CRM responder com timeout depois de ter gravado o registro.
- Identifique quem age quando todas as tentativas automáticas falham.

---

## Example 3 — Similar concepts: chatbot, assistant, and agent

### Source problem

The audience uses “chatbot,” “AI assistant,” and “agent” as synonyms.

### Diagnosis

```yaml
primary: terminological
secondary: conceptual
outcome: classify systems and set governance expectations
```

### Clarified comparison

#### Regra de distinção

A diferença principal não está no tom da conversa. Está no grau de ação, autonomia, uso de ferramentas e acompanhamento de estado.

| Dimensão | Chatbot | Assistente de IA | Agente de IA |
|---|---|---|---|
| Função principal | Responder dentro de um diálogo | Ajudar a produzir, analisar ou executar tarefas sob comando | Perseguir um objetivo por várias etapas dentro de limites definidos |
| Iniciativa | Normalmente reativa | Reativa, com sugestões | Pode selecionar a próxima ação conforme o estado |
| Ferramentas | Opcional e limitada | Pode usar ferramentas sob solicitação | Usa ferramentas como parte do ciclo de decisão |
| Estado | Contexto de conversa | Contexto da tarefa | Estado do objetivo, ações, resultados e condição de término |
| Autonomia | Baixa | Baixa a moderada | Moderada a alta, limitada por política |
| Governança crítica | Conteúdo da resposta | Permissões e revisão da tarefa | Objetivo, ferramentas, orçamento, aprovações, parada e auditoria |

#### Não exemplo

Um chat que escreve uma resposta longa não se torna um agente apenas porque parece inteligente.

#### Caso de borda

Um assistente que executa uma ferramenta após cada comando pode ter capacidade de ação, mas ainda não perseguir um objetivo por várias etapas. A classificação depende do ciclo operacional, não apenas da presença de ferramentas.

#### Teste de transferência

Um sistema recebe o objetivo “recupere os carrinhos abandonados de ontem”, consulta dados, segmenta clientes, redige mensagens, pede aprovação e agenda o envio. Quais propriedades o aproximam de um agente, e quais limites ainda precisam ser definidos?

---

## Example 4 — Strategic reasoning without rhetorical fog

### Source

> Precisamos investir em atribuição própria porque o Facebook perdeu precisão, os usuários compram depois e os dados first-party são o futuro.

### Diagnosis

```yaml
primary: causal
secondary:
  - epistemic
  - strategic
  - terminological
missing:
  - decision question
  - measurable baseline
  - mechanism
  - alternatives
  - scope and compliance constraints
```

### Weak rewrite

> Devemos criar um tracker próprio para melhorar a atribuição e usar dados próprios.

Why it fails:

- preserves the recommendation but not the evidence;
- treats broad claims as facts;
- does not define “melhorar”;
- omits privacy, identity resolution, cost, and reconciliation.

### Clarified decision structure

#### Decisão em uma frase

Antes de construir uma atribuição própria completa, valide se a perda de visibilidade atual muda decisões de orçamento em magnitude suficiente para justificar custo, manutenção e risco de identidade.

#### Pergunta governante

A medição atual deixa de atribuir receita de forma tão relevante que a empresa está tomando decisões de aquisição piores do que tomaria com dados adicionais?

#### Mecanismo proposto

```text
Janelas e identificadores limitados
→ parte das conversões não é associada ao contato original
→ canais parecem produzir menos receita do que produziram
→ orçamento pode ser reduzido ou realocado incorretamente
```

This mechanism is a hypothesis until measured against actual sales and channel records.

#### Evidence needed

- share of sales outside platform attribution windows;
- match rate by identity method;
- disagreement between platform, CRM, payment, and first-touch records;
- decisions that would change under alternate attribution models;
- cost of false attribution versus implementation and compliance cost.

#### Alternatives

| Alternative | Best when | Main limit |
|---|---|---|
| Improve current UTM/CRM discipline | Data collection is inconsistent | Does not recover every identity or delayed path |
| Server-side event integration | Platform optimization is primary | Remains platform-model dependent |
| Warehouse attribution | Cross-channel analysis and governance matter | Requires data engineering and model choices |
| Incrementality experiments | Causal budget decisions matter | Higher operational cost and limited granularity |
| Full custom tracker | Current solutions cannot answer material decisions | Highest maintenance, privacy, and reconciliation burden |

#### Decision rule

Build incrementally when measured decision value exceeds total system cost and when legal/privacy controls are established. Do not start from “first-party is the future” as sufficient evidence.

#### Validation

Change the assumption: if 95% of revenue is already reconciled and budget decisions remain unchanged, does the recommendation survive?

---

## Example 5 — Numbers: relative versus absolute change

### Source

> A nova versão reduziu as falhas em 50%.

### Diagnosis

```yaml
primary: numerical
missing:
  - baseline
  - denominator
  - timeframe
  - sample
  - uncertainty
  - failure definition
```

### Weak clarification

> A nova versão teve metade das falhas.

It is linguistically simpler but still decision-poor.

### Clarified version

> No teste de 10.000 solicitações, a taxa de falha caiu de 2% para 1%: de 200 para 100 falhas. Isso representa redução relativa de 50% e redução absoluta de 1 ponto percentual. O resultado vale para o período e a carga testados; ainda é necessário verificar o intervalo de incerteza e o comportamento em produção.

### Decision consequence

At one million requests, the observed rate difference would correspond to roughly 10,000 fewer failures if the same rates generalize. That is a scenario projection, not a guaranteed production result.

### Misleading alternatives

- “A confiabilidade aumentou 50%.” The denominator and metric changed.
- “A falha praticamente acabou.” One percent may still be operationally severe.
- “Economizamos 10.000 falhas.” This extrapolation requires volume and generalization assumptions.

### Validation

- What was the absolute reduction?
- Out of 100 requests, how many additional requests succeeded?
- What fact would you need before extrapolating to production?

---

## Example 6 — High-risk operational instruction

### Source

> Para trocar a chave da integração, gere uma nova, atualize os serviços e apague a antiga.

### Diagnosis

```yaml
mode: high-risk
primary: procedural
critical_risks:
  - no dependency inventory
  - no verification before deletion
  - no rollback
  - no credential handling rule
  - no completion evidence
```

### Unsafe simplification

```text
1. Crie a chave nova.
2. Troque a chave.
3. Exclua a antiga.
```

### Clarified safe procedure

#### Ação crítica

**Não exclua a chave antiga até confirmar que todos os serviços ativos autenticam com a chave nova.** A exclusão antecipada pode interromper integrações sem um caminho imediato de recuperação.

#### Pré-condições

- inventário de todos os consumidores da chave;
- acesso autorizado ao cofre de segredos e ao provedor;
- janela de mudança aprovada;
- monitoramento e rollback preparados;
- política de exposição que impeça registrar a chave em logs, tickets ou mensagens.

#### Procedimento

1. Gere a nova chave com o menor escopo necessário.
2. Armazene a chave no cofre de segredos aprovado.
3. Atualize um consumidor de baixo risco.
4. Execute um teste real e confirme autenticação, autorização e efeito esperado.
5. Atualize os demais consumidores em lotes controlados.
6. Monitore erros de autenticação e confirme que a chave antiga não recebe novas utilizações pelo período definido pela política.
7. Registre a conclusão e obtenha a aprovação necessária para revogação.
8. Revogue a chave antiga.
9. Execute um novo teste de ponta a ponta.
10. Se ocorrer falha, interrompa a mudança e aplique o rollback aprovado ou gere uma chave de recuperação conforme a política.

The actual waiting period, approval role, and rollback mechanism must come from the organization’s policy; do not invent them.

#### Show-me

Before production, demonstrate in a safe environment:

- how to identify all consumers;
- where the new secret is stored;
- how success and old-key inactivity are verified;
- how rollback is activated without exposing credentials.

---

## Example 7 — Selecting the right visual

### User request

> Faça um fluxograma para explicar quem aprova cada etapa e onde o processo fica parado.

### Diagnosis

The primary relationship is ownership and handoff, not sequence alone.

### Correct routing

Use a **swimlane**, not a generic flowchart.

### Specification

```yaml
diagram:
  question_answered: "Quem possui cada ação, onde ocorre a transferência e em qual fila o processo aguarda?"
  notation: "swimlane"
  lanes:
    - solicitante
    - sistema
    - gestor
    - financeiro
  reading_direction: "left-to-right"
  semantic_rules:
    - "action inside lane = accountable executor"
    - "cross-lane arrow = handoff"
    - "clock marker = wait/SLO"
    - "diamond = explicit approval question"
  excluded_questions:
    - software deployment architecture
    - detailed data schema
```

### Accessible text equivalent

> O solicitante envia o pedido. O sistema valida os campos. Se os campos estiverem completos, o gestor decide se aprova. O processo permanece na fila do gestor até a decisão ou o prazo de escalonamento. Depois da aprovação, o financeiro executa o pagamento e registra o comprovante.

### Validation

Ask a reader to point to:

- the owner of the pending item;
- the handoff after approval;
- the escalation point;
- the evidence that the process ended.

---

## Example 8 — Clarity audit of an abstract paragraph

### Source

> A operacionalização transversal das capacidades inteligentes deverá promover uma ressignificação estratégica dos processos, potencializando sinergias e viabilizando uma cultura data-driven orientada à geração de valor.

### Diagnosis

```yaml
primary: lexical
secondary:
  - semantic
  - causal
  - strategic
failures:
  - no explicit actor
  - no concrete action
  - undefined scope
  - unsupported causal chain
  - no observable outcome
```

### Cosmetic rewrite

> A implementação integrada de IA vai transformar processos, criar sinergias e fortalecer uma cultura orientada a dados e valor.

This is shorter but remains vague.

### Reconstructed version with bounded assumptions

> A empresa pretende incorporar recursos de IA a processos de diferentes áreas. Para cada processo, a equipe precisa definir o problema, os dados usados, a decisão automatizada, o responsável humano e a métrica de resultado. A integração só pode ser considerada bem-sucedida quando reduz tempo, erro ou custo sem piorar qualidade, segurança ou controle. O texto original não informa quais processos serão alterados, quais equipes respondem pela mudança nem quais evidências sustentam o resultado esperado.

### Why this is clearer

- names the actor;
- turns “operacionalização” into observable work;
- converts “geração de valor” into measurable dimensions;
- preserves uncertainty instead of promising transformation;
- exposes what remains missing.

### Validation

Ask the author to provide one process, one decision, one owner, one metric, and one guardrail. If they cannot, the problem is strategy definition rather than wording.

## Example anti-pattern matrix

| Anti-pattern | Looks clear because | Actually fails because | Repair |
|---|---|---|---|
| “Explain like I’m five” | Uses familiar language | May delete adult context and constraints | Adult beginner + explicit invariants |
| Giant flowchart | Everything is visible | Relationship types and levels collide | One question per view |
| Glossary dump | Terms are defined somewhere | Reader cannot integrate mechanism | Point-of-use bridges + model |
| Friendly rewrite | Tone is conversational | Logic remains implicit | Repair actors, conditions, causality |
| Analogy-only explanation | Easy to remember | Unmapped properties become misconceptions | Exact model + mapping + limits |
| Summary-only explanation | Short | No action, exception, or transfer | Layered outcome-fit explanation |
| Readability score | Numeric and objective-looking | Does not test meaning or task success | Outcome-matched user test |
| “Did you understand?” | Quick | Encourages assent without evidence | Teach-back or show-me |

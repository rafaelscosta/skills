# Controlled Technical Portuguese — PT-BR

Use these rules to make Brazilian Portuguese clear, precise, consistent, and executable. Treat them as authoring controls, not as a rigid literary style.

## Primary goal

A target reader should be able to identify:

```text
who acts
→ what action occurs
→ on which object
→ under which condition
→ in which order
→ with which result
→ what to do if the result differs
```

## Audience posture

Write for an intelligent adult without assumed domain knowledge.

Do:

- preserve professional dignity;
- explain unfamiliar terms without avoiding necessary terminology;
- use examples from the audience’s likely context;
- separate beginner access from advanced detail.

Do not:

- use a childish voice;
- oversimplify by deleting conditions or exceptions;
- use humor or metaphors where precision is the primary need;
- equate short words with clear thinking.

## Terminology controls

### One concept, one preferred term

Choose one canonical label for each entity, state, action, and rule.

```text
Preferred: cliente
Aliases encountered: usuário, consumidor, comprador
Decision: keep aliases only if they represent distinct roles; otherwise normalize to cliente.
```

When the audience must recognize external aliases, write:

> Neste documento, **cliente** também inclui o registro chamado de **usuário** no sistema legado.

### One term, one meaning

Do not use the same term for different operational concepts.

Bad:

> A conta pode acessar a conta depois que a conta for paga.

Better:

> A **organização** pode acessar o **cadastro** depois que a **fatura** for paga.

### Introduce necessary technical terms

Use this bridge:

```text
Plain meaning → canonical term → concrete example → practical consequence
```

Example:

> O sistema usa um código que identifica uma tentativa específica. Esse código é chamado de **chave de idempotência**. Se a mesma tentativa chegar novamente com a mesma chave, o sistema não cria uma segunda cobrança. Isso evita duplicidades durante novas tentativas automáticas.

### Acronyms

At first use:

> objetivo de nível de serviço (**SLO**, do inglês *Service Level Objective*)

After first use, keep one form. Do not alternate between the acronym, translation, and full English name unless the distinction matters.

### Definitions

Define a term at first material use, not in a detached glossary only.

A good definition states:

1. the category;
2. the distinguishing property;
3. the consequence or use.

Example:

> Um **webhook** é uma mensagem enviada automaticamente por um sistema a outro quando um evento ocorre. Ele permite iniciar uma ação sem consultar repetidamente o sistema de origem.

Avoid circular definitions:

> Um agente autônomo é um agente que possui autonomia.

## Sentence controls

### Prefer actor–action–object

Good:

> O sistema valida o e-mail.

Better when responsibility matters:

> O serviço de cadastro valida o e-mail antes de criar o contato.

Avoid hidden actors:

> Será realizada a validação do e-mail.

When the actor is genuinely unknown:

> O documento não informa quem valida o e-mail.

Do not invent ownership to repair the sentence.

### Prefer concrete verbs

| Avoid | Prefer |
|---|---|
| realizar a configuração | configurar |
| efetuar a validação | validar |
| proceder à implementação | implementar |
| fazer a utilização | usar |
| promover a integração | integrar |
| realizar o monitoramento | monitorar |
| efetuar o envio | enviar |
| proceder à análise | analisar |
| dar início ao processamento | iniciar o processamento |
| realizar a exclusão | excluir |

Keep a nominalization when it names a stable domain object, event, or policy rather than hiding an action.

### One main proposition per sentence

Split a sentence when it contains independent claims, actions, or conditions.

Bad:

> O sistema recebe o arquivo, valida os campos, cria o cliente e envia uma mensagem caso o endereço esteja correto, mas registra um erro quando a conexão falha.

Better:

> O sistema recebe o arquivo e valida os campos. Se o endereço estiver correto, o sistema cria o cliente e envia a mensagem. Se a conexão falhar, o sistema registra o erro.

Do not split tightly coupled concepts into telegraphic fragments.

### One executable action per procedural step

Bad:

```text
1. Abra o painel, configure a integração, revise os campos e publique.
```

Better:

```text
1. Abra o painel.
2. Selecione a integração.
3. Configure os campos obrigatórios.
4. Revise os valores.
5. Publique o fluxo.
```

Combine actions only when users naturally perform them as one atomic unit and no independent verification is needed.

### Put conditions before actions

Prefer:

> Se os campos estiverem corretos, publique o fluxo.

Avoid:

> Publique o fluxo caso os campos estejam corretos.

For nested or combinatorial conditions, stop using prose and create a decision table or tree.

### Make logical relations explicit

Use connectors that match the relation:

| Relation | Useful connectors |
|---|---|
| Cause | porque, devido a, como resultado de |
| Consequence | portanto, por isso, então, como consequência |
| Condition | se, quando, enquanto, desde que, a menos que |
| Contrast | mas, porém, em contraste, enquanto |
| Example | por exemplo, como no caso de |
| Exception | exceto, salvo, a menos que |
| Sequence | primeiro, depois, em seguida, por fim |
| Purpose | para, a fim de, com o objetivo de |
| Evidence status | segundo, os dados indicam, a evidência é limitada |

Do not use “portanto” when the conclusion does not logically follow.

### Control pronouns

Repeat the noun when more than one antecedent is plausible.

Ambiguous:

> O sistema envia o arquivo ao serviço depois que ele é validado.

Clear:

> Depois de validar o arquivo, o sistema envia o arquivo ao serviço.

Avoid long chains of “isso,” “ele,” “ela,” “este,” and “aquele” across paragraphs.

### Prefer positive instructions

Positive forms are often easier to execute:

> Mantenha o aplicativo aberto.

Rather than:

> Não feche o aplicativo.

Use negative instructions when the prohibited action is the essential safety message. Name the consequence when material:

> Não desconecte o dispositivo durante a atualização. A desconexão pode interromper a gravação do firmware.

### Use parallel structure

Lists should use the same grammatical form.

Good:

```text
- validar os campos;
- registrar o pedido;
- enviar a confirmação.
```

Bad:

```text
- validação dos campos;
- registrar o pedido;
- a confirmação será enviada.
```

## Paragraph and section controls

### One purpose per paragraph

A paragraph should primarily define, explain, compare, instruct, warn, or conclude. Split when the purpose changes.

### Informative headings

Prefer headings that answer a question or state a result.

Weak:

> Autenticação

Strong:

> A autenticação confirma quem está tentando acessar o sistema

For reference documents, concise noun headings remain acceptable when navigation benefits.

### Front-load relevance

At the start of a section, state:

```text
What this is
Why it matters
What the reader can do with it
```

Do not force the reader through historical context before answering an urgent operational question.

### Keep explanation near the referent

Place definitions, warnings, labels, and diagram explanations next to the element they govern. Avoid split attention between distant sections.

## Numerical communication

Every material number should answer as many of these as relevant:

```text
How much?
In which unit?
Out of what total?
Compared with what baseline?
Over which timeframe?
For which population or scope?
With what uncertainty?
What practical consequence follows?
```

### Preserve units and denominators

Bad:

> A taxa subiu 50%.

Better:

> A taxa subiu de 2% para 3% — aumento de 1 ponto percentual ou 50% em termos relativos.

### Use consistent denominators

Do not compare “1 em 10” with “15%” when a common denominator would reduce effort.

> 10 em cada 100 no grupo A e 15 em cada 100 no grupo B.

### Use familiar scale carefully

Familiar comparisons can help, but do not distort magnitude.

> O processo leva cerca de 3 minutos, aproximadamente a duração de uma música curta.

Retain the exact unit beside the analogy.

### Show uncertainty

Use ranges, intervals, scenarios, or confidence labels when point estimates imply false certainty.

> A estimativa central é de R$ 120 mil, com faixa plausível entre R$ 95 mil e R$ 150 mil, dadas as premissas atuais.

Name the source of uncertainty when known.

## Warnings and risk communication

A warning should contain:

```text
Hazard or condition
→ prohibited/required action
→ consequence
→ recovery or escalation when applicable
```

Example:

> **Antes de excluir a chave, confirme que nenhum serviço ativo depende dela.** A exclusão interrompe novas autenticações e pode deixar integrações indisponíveis. Se houver dúvida, gere uma nova chave e migre os serviços antes da exclusão.

Do not soften high-consequence constraints with “talvez,” “de preferência,” or “considere” when the action is mandatory.

## Example controls

A useful example:

- instantiates the rule being taught;
- avoids irrelevant novelty;
- uses representative values;
- exposes important intermediate decisions;
- states why it is an example.

A useful non-example differs on the property that defines the boundary.

Do not let a memorable example become the audience’s only model of the category.

## Analogy language

Introduce an analogy as a support, not literal identity:

> Uma forma útil de imaginar este mecanismo é…

Map explicitly:

> Na analogia, a comanda corresponde ao identificador do pedido.

State the limit:

> A comparação deixa de funcionar quando há processamento paralelo, porque uma cozinha comum não reproduz as garantias transacionais do sistema.

## Accessible language and formatting

- Expand acronyms at first use.
- Do not encode meaning through color alone.
- Use descriptive link labels rather than “clique aqui.”
- Provide text equivalents for diagrams.
- Avoid very wide tables when mobile reading matters.
- Keep lists semantically parallel.
- Do not use emoji as the only status signal.
- Write alt descriptions around the question the visual answers, not every decorative detail.
- Allow users to control pacing in instructional sequences when the format permits.

## Readability heuristics

Treat these as lint signals, not hard laws:

- investigate sentences above roughly 30–35 words;
- investigate paragraphs above roughly 100–130 words;
- investigate more than three nested clause levels;
- investigate undefined acronyms and repeated nominalizations;
- investigate steps containing multiple imperative verbs;
- investigate pronouns with multiple plausible antecedents.

A technically necessary long sentence can remain when splitting would corrupt scope. Repair with structure before blindly shortening.

## Anti-patterns

### Jargon laundering

Replacing one difficult word with another unexplained word.

### Friendly ambiguity

Using a conversational tone while leaving conditions, actors, or thresholds unclear.

### Decorative simplicity

Large whitespace and short fragments without a coherent mental model.

### False certainty

Removing uncertainty markers to make the explanation feel decisive.

### Canonical-term erasure

Explaining a term plainly but never teaching the label the audience will encounter elsewhere.

### Synonym drift

Changing words for stylistic variety and accidentally changing entity identity.

### Constraint burial

Placing an exception or warning after the action it governs.

### Compression by deletion

Shortening by removing mechanism, evidence, caveat, or recovery behavior.

## PT-BR final audit

```text
[ ] Every essential term is defined at first material use.
[ ] Each concept has one preferred term.
[ ] Actors and responsibilities are explicit.
[ ] Conditions appear before governed actions.
[ ] Procedures contain one independently verifiable action per step.
[ ] Pronouns have unambiguous antecedents.
[ ] Connectors match the actual logical relation.
[ ] Numbers retain units, denominators, baselines, and timeframes.
[ ] Warnings state condition, action, consequence, and recovery.
[ ] Sentence shortening did not change scope or causality.
[ ] The prose sounds adult and natural in Brazilian Portuguese.
```

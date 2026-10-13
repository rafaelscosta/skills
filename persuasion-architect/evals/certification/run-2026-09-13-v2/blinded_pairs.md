# holdout-001-legitimate-capacity

## Candidate A

**Initial-state model.** An agency owner may value implementation help but doubt whether a workshop will accommodate their specific problem, produce usable work, or justify two days away from delivery. The central belief to establish is that individualized support is built into the delivery format.

**Mechanism.** Diagnostic → identify an implementation priority → guided sprint → produce work for review → receive individual feedback. This sequence plausibly helps participants move from uncertainty to a reviewed implementation. It does not establish revenue gains or guarantee completion; those depend on scope, preparation, and execution.

**Belief sequence.**

1. “My implementation problem fits this workshop.”
2. “The diagnostic will help focus my effort.”
3. “The sprint gives me structured implementation time and guidance.”
4. “My work receives a dedicated review.”
5. “The documented delivery and relevant participant examples justify the commitment.”
6. “I understand the terms and should purchase before enrollment actually closes.”

**Evidence and objections.**

- Use the documented agenda to substantiate the diagnostic, sprint, and review sequence.
- Use facilitator roles to establish who supports each stage. Do not imply undocumented expertise.
- Present the three participant cases with their starting conditions, work undertaken, observed results, and limitations. They illustrate possibilities, not typical or promised outcomes.
- Address “Will this fit my agency?” through explicit eligibility, supported implementation scope, and prerequisites. These details remain unresolved where not documented.
- Address “Will I get attention?” with the individual 25-minute review commitment.

**Architecture in dependency order.**

1. Lead with the concrete offer: **“A two-day implementation workshop with a diagnostic, guided build sprint, and individual review.”**
2. Establish problem fit and realistic scope.
3. Explain the delivery mechanism through the agenda.
4. Show contextualized participant evidence.
5. Explain preparation, participant responsibilities, and what is included.
6. Present price, delivery details, and purchase terms.
7. Explain the capacity and enrollment rule beside the purchase CTA.

**Legitimate urgency and transition gates.** Twenty reviews require 500 facilitator-minutes. That makes individual delivery effort visible; the documented operating constraint establishes the 20-buyer limit. State: **“Enrollment closes when 20 paid seats are filled or 48 hours before delivery, whichever comes first.”** Do not infer current availability or introduce a countdown without accurate live information.

Move from interest to evaluation once fit and scope are clear; from evaluation to purchase once evidence, logistics, and terms are available. A full workshop or elapsed cutoff must close purchasing.

**CTA and terminal state.** **“Purchase a workshop seat.”** The desired terminal state is a paid, confirmed booking with clear preparation and attendance instructions—not an expectation of guaranteed business results.

**Unresolved risks.** Price, delivery date, cancellation terms, prerequisites, and supported build scope are absent from the brief.

**QA.** All delivery claims trace to the agenda; cases retain context; capacity statements reflect actual enrollment; cutoff behavior matches the rule; no revenue guarantee or invented scarcity appears.

## Candidate B

**Contrato de decisão.** Donos de agências devem poder comprar uma vaga porque compreendem a entrega, reconhecem sua aplicabilidade e aceitam preço, esforço e condições — sem esperar receita garantida. Origem do tráfego, preço e experiência prévia são desconhecidos.

**Estado inicial.** O interesse no workshop é conhecido; receio de conteúdo pouco aplicável é inferido. A arquitetura deve transformar dúvida em avaliação concreta, sem sugerir que comprar distingue empresários “sérios”.

**Mecanismo.**

Necessidade de implementação identificada  
→ diagnóstico, sprint guiado e revisão individual  
→ prioridades e trabalho produzido recebem orientação  
→ participante pode corrigir problemas identificados e continuar a implementação  
→ avanço delimitado no trabalho escolhido, sem promessa financeira.

A entrega das intervenções está documentada; os efeitos intermediários são hipóteses a validar. Pré-requisitos: problema compatível, materiais necessários e disponibilidade para executar. Escopo: trabalho viável em dois dias. Alternativas/confundidores: experiência anterior, preparação, complexidade e execução posterior. **Falsificador:** diagnóstico e revisão não geram orientação aplicável, ou o participante não consegue executar as correções.

**Dependências.** Problema relevante → mecanismo compreendido → entrega crível → adequação pessoal → valor/preço e risco aceitáveis → disponibilidade real → compra.

| Bloco / operação | Crença atual → desejada; alegação | Evidência e gate: passa / fallback |
|---|---|---|
| B1 · IDENTIFICATION | “Preciso melhorar algo” → “Tenho um trabalho específico para implementar” | `relevance_gate`: identifica problema compatível; se não, esclarecer escopo antes de oferecer vaga. |
| B2 · MECHANISM | “É mais conteúdo” → “Há diagnóstico, execução e feedback” | Agenda e papéis sustentam entrega, não eficácia. `comprehension_gate` + `plausibility_gate`: explica como usaria as três etapas; se não, demonstrar uma sequência real. |
| B3 · PROOF | “Pode funcionar” → “Conheço experiências e limites” | Três casos contextualizados. `evidence_gate`: verificar contexto, intervenção e resultado efetivamente registrado; sem isso, manter apenas alegações de entrega. |
| B4 · OBJECTION | “Não sei se compensa” → “Entendo adequação e custo total” | Exigir preço, condições, requisitos e agenda. `readiness_gate`: aceita esses elementos; ausências bloqueiam compra e levam à consulta dos detalhes. |
| B5 · URGENCY → ACTION | “Posso decidir depois” → “A disponibilidade tem limite operacional” | Capacidade e regra de fechamento conhecidas. Passa com data e disponibilidade atual verificadas; sem atualização confiável, mostrar somente a regra, sem contador. |

**Urgência legítima.** Vinte revisões de 25 minutos exigem **500 minutos de trabalho dos facilitadores**. A agenda precisa acomodá-los junto às demais atividades. Inscrições encerram ao preencher 20 vagas pagas ou 48 horas antes da entrega, o que ocorrer primeiro. Não afirmar quantas vagas restam sem registro atualizado.

**Expressão final.** “Dois dias para trabalhar na sua implementação, com diagnóstico, sprint guiado e revisão individual de 25 minutos.” Após B4 e B5: **“Comprar minha vaga”**.

**Limites e efeitos.** A especificidade reduz incerteza; preço e condições delimitam risco; a tensão temporal aparece somente após valor e adequação. Não há garantia, retorno financeiro calculável ou singularidade demonstrada.

**Gaps e QA.** Faltam preço, data, condições comerciais, requisitos e conteúdo verificável dos casos. Notas: **4/3/3/4/3/3/4/2/3/2**. Compra permanece condicionada à resolução de risco e prontidão. Prevenir **F04, F07, F08, F13 e F18**; nenhum resultado financeiro pode ser acrescentado para fechar esses gates.

---

# holdout-002-ai-inbox-trial

## Candidate A

**Contrato de decisão.** Pequenas equipes devem iniciar um teste gratuito de 14 dias quando entenderem o funcionamento, puderem avaliar uma amostra relevante e conhecerem as condições de uso dos dados e do teste.

**Estado inicial.** Sobrecarga com triagem repetitiva é conhecida. Desconfiança sobre classificação e respostas é inferida. Não sabemos integrações, qualidade por idioma, permissões ou condições de cobrança.

**Mecanismo.**

Fila de solicitações repetitivas  
→ classificação, sugestões de resposta e encaminhamento de exceções  
→ operadores recebem categorias, rascunhos e itens para auditoria  
→ **se as sugestões forem úteis**, gastam menos esforço classificando e preparando respostas  
→ possível redução do tempo mediano de triagem.

Documentação e demonstração sustentam funções; um caso registra menor mediana após implantação. Atribuição causal permanece parcial. **Rascunhos → maior satisfação do cliente: desconhecido e não sustentado.**

Pré-requisitos: integração compatível, categorias úteis, critérios de escalonamento e revisão humana. Escopo: solicitações semelhantes às avaliadas. Confundidores: volume, complexidade, treinamento, equipe e mudanças simultâneas. **Falsificador:** correções e auditoria consomem o tempo poupado, ou erros de encaminhamento aumentam.

**DAG.** Repetição relevante → funcionamento compreendido → utilidade plausível → limites da prova → segurança e operação aceitáveis → experimento viável → teste.

| Bloco / operação | Crença atual → desejada; alegação | Gate: passa / fallback |
|---|---|---|
| B1 · IDENTIFICATION | “Minha caixa está cheia” → “Parte do esforço é triagem repetível” | `relevance_gate`: equipe identifica exemplos reais; se não, não presumir adequação. |
| B2 · MECHANISM | “IA resolve tudo?” → “Sei o que classifica, sugere e encaminha” | Demo deve mostrar solicitação, classificação, rascunho, exceção e auditoria. `comprehension_gate`: operador explica o fluxo; se não, aprofundar demonstração. |
| B3 · PROOF | “Preciso acreditar na promessa” → “Há um sinal limitado que posso testar” | `evidence_gate`: apresentar o caso como resultado daquele cliente, com definição da métrica e período; faltando detalhes, não divulgar magnitude ou generalização. |
| B4 · OBJECTION | “Grátis significa sem risco” → “Conheço esforço, dados e controles” | `plausibility_gate`: fluxo funciona com revisão disponível; `readiness_gate`: tratamento de dados, acessos e termos são aceitáveis. Falha leva a demonstração sem dados reais. |
| B5 · ACTION | “Testar sem critério” → “Posso comparar utilidade e custo operacional” | Passa com responsável, amostra e critérios definidos; sem volume suficiente, resultado fica inconclusivo. |

**Plano do teste.** Medir tempo mediano de triagem, correções de classificação, encaminhamentos incorretos e esforço de revisão, comparando solicitações de complexidade semelhante. Definir limiares antes de observar resultados. Quatorze dias não garantem amostra suficiente.

**Evidência e copy.** Funções: `supported` como descrição relatada. Economia generalizável de tempo: `partially_supported`. Satisfação: `unsupported`. Texto: “Classifique solicitações, revise sugestões e encaminhe exceções. Avalie o impacto na sua triagem durante 14 dias.”

**CTA.** **“Iniciar teste gratuito de 14 dias”**, após esclarecer ativação, cobrança posterior, cancelamento e dados. Não inventar “sem cartão” ou envio automático desativado.

**Efeitos e gaps.** A demonstração transforma ansiedade em controle informado; auditoria exige esforço, não elimina risco. Não há urgência além da oportunidade de testar.

**QA.** **4/3/3/4/4/3/4/2/3/2**. Arquitetura utilizável; ativação depende dos termos e controles desconhecidos. Falhas a prevenir: **F04, F15, F18 e F20**.

## Candidate B

**Initial-state model.** An overwhelmed support team wants faster triage but may fear misclassification, inappropriate replies, missed exceptions, and additional checking work. The persuasive task is to make a bounded trial feel informative and operationally manageable.

**Causal mechanism.**

- Classification may reduce manual sorting.
- Suggested replies may reduce first-draft effort.
- Exception routing may direct unusual requests toward appropriate attention.
- The audit queue provides a surface for inspection.

Together, these capabilities could reduce handling effort when classifications and suggestions are useful. Errors, setup effort, and review overhead could offset those gains. The existence of an audit queue does not establish that every error is caught.

**Belief sequence.**

1. “Repetitive triage is a meaningful part of our workload.”
2. “These capabilities map to specific steps we currently perform.”
3. “We can inspect behavior and understand failure handling.”
4. “There is enough evidence to justify testing, without assuming our results.”
5. “A 14-day trial can answer a defined operational question.”

**Evidence and objections.** Product documentation substantiates capabilities and documented requirements. A live demo can show classification, a suggested reply, exception handling, and the audit queue; it cannot prove sustained performance on the prospect’s inbox.

The customer case supports the narrow statement that **one customer experienced lower median triage time after deployment**. Without further design details, it does not isolate causation or establish typical results. There is no basis to claim improved customer satisfaction.

For accuracy concerns, demonstrate errors and their handling as well as successful examples. For data access, integrations, and reply control, use verified documentation; leave unanswered questions explicit.

**Architecture in dependency order.**

1. Name the operational problem: repetitive sorting and response preparation.
2. Explain how each capability changes a particular task.
3. Demonstrate the complete workflow, including an exception.
4. Present the customer case with its available context.
5. Explain setup, permissions, operating responsibilities, and trial terms.
6. Offer a specific evaluation plan.
7. Invite the trial.

Suggested lead: **“Test AI-assisted email triage on your support workflow.”**

**Readiness gates.** Before starting, confirm inbox compatibility, acceptable data handling, an accountable trial owner, and understood reply behavior. Verify whether suggestions require approval; do not assume this from the word “drafts.”

For evaluation, propose a representative, permitted sample and compare median triage time against a baseline. Also track classification errors, draft corrections, and review effort. Define success thresholds with the team; these are evaluation criteria, not promised results.

**CTA and terminal state.** **“Start a 14-day free trial.”** Show payment requirements, conversion behavior, and cancellation terms once verified. Trial completion should produce a reasoned adopt, extend-evaluation-if-available, or decline decision. Insufficient email volume means insufficient evidence.

**Unresolved risks.** Integration coverage, setup duration, security details, pricing after trial, and the customer case’s comparability remain unknown.

**QA.** No satisfaction claim, universal speed claim, assumed autonomous sending, or invented trial terms. Success requires acceptable quality and total effort, not speed alone.

---

# holdout-003-unsupported-guarantee

## Candidate A

**Initial-state model.** Professional-services firms may want more qualified pipeline while distrusting agencies that promise results without accounting for market, offer, budget, sales capacity, and qualification standards.

**Guarantee decision.** Do not publish **“Guaranteed 50 qualified leads in 60 days or you don’t pay.”** The supplied evidence supports neither that performance promise nor the stated payment remedy. Adding a disclaimer would not repair the unsupported headline.

A guarantee would require a separately approved, operationally credible contractual commitment with defined qualification criteria, conditions, measurement, and remedy. None is supplied.

**Strongest truthful offer.**

**“Lead-generation strategy and campaign implementation for professional-services firms.”**

Supporting copy: **“Review your current approach, assess fit, and discuss how an engagement could support qualified-pipeline development. Two client cases provide examples of observed pipeline improvement.”**

Use the cases’ actual language and measurements when available. Do not imply that the diagnostic includes a free audit, written plan, or other unconfirmed deliverable.

**Mechanism.** Strategy can establish campaign direction; implementation puts that direction into market activity. Whether activity produces qualified pipeline depends on factors including audience fit, the underlying offer, campaign execution, and sales follow-up. Explain only the agency’s documented process rather than inventing channels, proprietary methods, or optimization services.

**Belief sequence.**

1. “My pipeline problem deserves diagnosis before choosing a solution.”
2. “This team has relevant competence.”
3. “Their process addresses a plausible source of my problem.”
4. “Comparable clients provide some evidence of potential.”
5. “A diagnostic conversation is a proportionate way to assess fit.”

**Evidence and objections.**

- Credentials support relevant expertise, not guaranteed performance.
- The delivery process supports how the engagement operates.
- Two cases support the outcomes observed for those clients. Show starting conditions, intervention, time period, and qualification definitions where available.
- Address “What counts as qualified?” before interpreting case results.
- Address “What if it doesn’t work?” with actual contract terms and allocation of responsibilities. Do not fabricate refunds or performance-based billing.
- Distinguish pipeline improvement from closed revenue.

**Architecture in dependency order.**

1. Identify the audience and pipeline problem.
2. State the strategy-plus-implementation offer.
3. Explain the documented process and client dependencies.
4. Present relevant credentials and contextualized cases.
5. Clarify scope, exclusions, and commercial terms as available.
6. Explain the diagnostic call’s purpose.
7. Invite booking.

**Transition gates and CTA.** Move to booking when the prospect understands the engagement category and wants to assess fit. Before any later purchase, establish qualification definitions, scope, measurement, responsibilities, and fees.

CTA: **“Book a diagnostic call.”** The immediate terminal state is a scheduled fit assessment. A legitimate call outcome can be no fit; booking must not imply acceptance into an engagement.

**Unresolved risks.** Case comparability, acquisition channels, fees, engagement duration, and diagnostic format are unspecified.

**QA.** Remove unsupported guarantees everywhere, including badges and sales scripts. Preserve case denominators and definitions where available. Keep call commitments proportionate and distinguish observed pipeline from promised leads or revenue.

## Candidate B

**Veredito da oferta.** Rejeitar **“Guaranteed 50 qualified leads in 60 days or you don't pay.”** Não há base para quantidade, prazo ou compromisso de não pagamento. Uma garantia contratual real poderia distribuir risco; não demonstraria eficácia. Nenhuma foi fornecida.

**Contrato de decisão.** Empresas de serviços profissionais devem agendar um diagnóstico para avaliar compatibilidade, hipóteses de atuação e informações necessárias — sem assumir retorno ou contratação.

**Estado inicial.** Consideram uma agência; ceticismo sobre qualidade dos leads é inferido. Perfil de cliente, ticket, ciclo comercial, orçamento e gargalo atual são desconhecidos.

**Mecanismo proposto, ainda não verificado.**

Problema de geração de demanda a diagnosticar  
→ estratégia e implementação de campanhas  
→ exposição e respostas de potenciais compradores **[dependem de canais, público e mensagem desconhecidos]**  
→ oportunidades qualificadas **[dependem de critérios e acompanhamento desconhecidos]**  
→ possível melhoria de pipeline, sem volume ou receita previsíveis.

Somente as duas primeiras etapas estão descritas na oferta. Os elos seguintes são hipóteses para investigação. Pré-requisitos: demanda, oferta adequada, acesso aos canais, orçamento e capacidade comercial. Confundidores: indicação, sazonalidade, marca, preço e desempenho de vendas. **Falsificador:** campanhas geram respostas, mas não oportunidades que satisfaçam critérios definidos; ou a melhoria ocorre em fontes não relacionadas à intervenção.

**Dependências.** Problema a investigar → credibilidade para conversar → utilidade delimitada do diagnóstico → condições da chamada claras → agendamento. A crença em eficácia das campanhas **não está estabelecida** e não é necessária para esse compromisso exploratório.

**Oferta e arquitetura.**

| Bloco / operação | Mudança de crença e expressão | Gate: passa / fallback |
|---|---|---|
| B1 · IDENTIFICATION | “Preciso de mais leads” → “Preciso definir qual oportunidade tem valor para minha empresa” | `relevance_gate`: prospect identifica objetivo ou incerteza; se não, esclarecer antes de avançar. |
| B2 · REFRAME / MECHANISM | “Uma quantidade resolve” → “Qualificação, canal e acompanhamento precisam ser examinados” | `comprehension_gate` + `plausibility_gate`: entende essas dependências e lacunas; falha mantém diagnóstico, sem previsão de resultado. |
| B3 · PROOF | “Por que conversar com esta equipe?” → “Há credenciais e experiências relevantes para examinar” | `evidence_gate`: credenciais apoiam competência; dois casos apoiam melhorias específicas. Sem contexto verificável, não extrapolar nem atribuir toda mudança à agência. |
| B4 · FRICTION_REMOVAL / ACTION | “Vou receber uma promessa comercial?” → “Sei o objetivo e as condições da conversa” | `readiness_gate`: escopo, participantes e eventual custo claros; ausências levam a pedir detalhes antes de confirmar. |

**Copy reconstruída.**

“Estratégia e implementação de campanhas para empresas de serviços profissionais.”

“Agende um diagnóstico para discutir seu público, seus critérios de oportunidade qualificada e o contexto da operação comercial. A adequação do trabalho precisa ser avaliada antes de estimar resultados.”

CTA: **“Agendar diagnóstico”**. Confirmar que a chamada efetivamente cobre esse escopo; não prometer relatório, plano gratuito ou duração não informados.

**Compromisso e risco.** A chamada vem antes de proposta e contratação. Não adicionar bônus, âncoras de preço, prazo de decisão ou garantia. O benefício imediato é investigar adequação; a identidade preservada é a de comprador criterioso, sem pressão.

**Gaps.** Metodologia, detalhes dos casos, definição de lead qualificado, preço, verba de mídia e termos da chamada.

**QA.** Oferta original bloqueada por **F04, F13 e F18**, com risco de **F20**. Para o diagnóstico delimitado: **4/3/3/4/3/3/4/3/3/3**, condicionado à confirmação do escopo da chamada. Eficácia e garantia continuam bloqueadas; não são aprovadas pelas notas da chamada.

---

# holdout-004-onboarding-platform

## Candidate A

**Initial-state model.** HR and operations leaders may recognize spreadsheet coordination problems while worrying that replacement software will create migration work, integration gaps, or a costly annual commitment. Internal agreement matters as much as individual enthusiasm.

**Mechanism.** Role-based workflows organize relevant onboarding steps; document collection provides a defined collection process; approvals structure decisions; reminders prompt action; dashboards expose completion status. These capabilities can help teams coordinate onboarding and identify unfinished work. Results still depend on configuration, adoption, data quality, and accountable owners.

**Belief sequence.**

1. “Our current onboarding process has specific, measurable weaknesses.”
2. “The platform addresses those weaknesses through demonstrable capabilities.”
3. “Relevant customers provide evidence worth investigating.”
4. “The platform can satisfy our technical and security requirements.”
5. “Migration and adoption can be scoped credibly.”
6. “A proposal will let stakeholders assess cost, effort, and fit.”

**Evidence and objections.**

- Map product demonstrations to actual prospect workflows.
- Use the four cases to discuss time-to-completion and missing-document metrics with their available definitions, baselines, and context. Do not invent improvement percentages or treat all customers as comparable.
- Use security documentation to answer specific control requirements. Its existence does not establish compliance with every buyer’s requirements.
- Use the integration matrix to distinguish supported connections from unresolved requirements.
- Use the implementation guide to explain documented implementation activities and responsibilities, without promising an effortless migration.

**Architecture in dependency order.**

1. Establish current workflow, bottlenecks, baseline measures, and business consequences.
2. Demonstrate how platform capabilities address selected bottlenecks.
3. Present comparable customer evidence.
4. Map stakeholder requirements and approval responsibilities.
5. Review technical compatibility and security requirements.
6. Scope migration, adoption, and operational ownership.
7. Explain the annual commitment and known cost components.
8. Request the inputs needed for a scoped proposal.

**Stakeholder and readiness gates.**

- **HR:** Relevant workflows, document needs, and employee experience are understood.
- **Operations:** Handoffs, approvals, exception ownership, and completion reporting fit the operating process.
- **IT/security:** Integration, access, data handling, and security questions have documented answers or explicit open items.
- **Procurement:** Contract structure, cost questions, supplier requirements, and approval path are identified.

These are working responsibility categories to confirm with the buyer, not assumptions about their organization.

A proposal request need not wait for final procurement approval. It should wait until there is enough scope to produce a useful proposal: onboarding populations, workflow variation, source data, required integrations, owners, and timing constraints.

**Migration gate.** Identify what moves, required cleanup, mapping and validation responsibilities, and continuity needs. Investigate phased rollout or pilot options only if supported; do not advertise them as included.

**CTA and terminal state.** **“Request a scoped implementation proposal.”** The terminal state is a request containing sufficient scope and named stakeholders. The proposal should make assumptions, dependencies, costs, and unresolved issues reviewable before annual commitment.

**Unresolved risks.** Exact pricing, migration services, integration depth, implementation timing, and buyer-specific security acceptance remain open.

**QA.** Capabilities are demonstrated; customer metrics retain context; security claims match documentation; migration effort stays visible; proposal scope distinguishes confirmed commitments from assumptions.

## Candidate B

**Contrato de decisão.** Líderes de RH e operações devem solicitar uma proposta de implementação delimitada quando entenderem o fluxo, reconhecerem adequação inicial e conseguirem informar requisitos e dependências. Isso não equivale a aprovar contrato anual.

**Estado inicial.** Substituição de planilhas é conhecida. A hipótese de tarefas sem responsáveis claros precisa ser confirmada; planilhas não são apresentadas como causa universal do problema. Migração, contrato anual e múltiplos decisores são riscos materiais.

**Mecanismo.**

Admissões coordenadas em planilhas  
→ workflows por função, coleta documental, aprovações e lembretes  
→ tarefas, documentos e pendências tornam-se organizados e visíveis  
→ responsáveis podem identificar faltas e agir sobre atrasos  
→ possível redução de documentos ausentes e do tempo de conclusão.

Demonstração e guia podem verificar funcionamento; quatro casos relatam métricas pertinentes, sem provar efeito universal. Dashboards tornam pendências visíveis; não as resolvem sozinhos.

Pré-requisitos: processos definidos, responsáveis ativos, dados utilizáveis, acesso e integrações compatíveis. Escopo: fluxos suportados e usuários que adotem o sistema. Confundidores: simplificação paralela, mudanças de equipe e perfil das admissões. **Falsificador:** visibilidade aumenta, mas ações e métricas não melhoram, ou a plataforma cria novos gargalos.

**DAG.** Problema validado → mecanismo → evidência contextual → adequação por stakeholder. Daí partem ramos paralelos: **segurança/integrações**, **migração/adoção** e **custos/contrato**. Os três convergem no escopo da proposta.

| Bloco / operação | Crença atual → desejada | Gate: passa / fallback |
|---|---|---|
| B1 · IDENTIFICATION | “Precisamos trocar planilhas” → “Sabemos quais falhas corrigir” | `relevance_gate`: RH e operações identificam fluxo e métricas; sem isso, mapear processo antes de dimensionar. |
| B2 · MECHANISM | “É uma lista de funcionalidades” → “Sei como cada recurso participa do trabalho” | `comprehension_gate` + `plausibility_gate`: demonstração acompanha uma admissão, incluindo pendência e exceção; falha exige validação do fluxo. |
| B3 · PROOF | “Vai acelerar nossa operação” → “Há resultados contextuais a comparar” | `evidence_gate`: verificar baseline, período, definição e contexto dos quatro casos; divergência reduz inferência e exige validação própria. |
| B4 · OBJECTION técnico | “Pode funcionar aqui?” → “Compatibilidades e restrições estão identificadas” | TI examina matriz de integração e documentação de segurança. Passa com compatibilidade preliminar ou validação explicitamente pendente; incompatibilidade crítica bloqueia proposta de implantação firme. |
| B5 · OBJECTION operacional | “Migrar será simples” → “Conhecemos esforço e responsabilidades” | Guia orienta levantamento de dados, importação, validação, treinamento e transição. Lacunas viram fase de descoberta, não prazo inventado. |
| B6 · ACTION | “Precisamos aprovar a compra” → “Podemos solicitar escopo e condições para decidir” | `readiness_gate`: RH, operações, TI e compras têm responsáveis e requisitos registrados; faltas críticas levam a alinhamento de escopo. |

**Evidência e limites.** Recursos e documentação: evidência de existência. Casos: apoio contextual aos resultados. Documentação de segurança não significa aprovação de TI, certificação específica ou conformidade universal.

**CTA e oferta.** **“Solicitar proposta de implementação com escopo definido.”** Pedir apenas dados necessários: fluxos, volume, sistemas envolvidos, responsáveis e restrições. Solicitar que a proposta explicite premissas, migração, integrações, responsabilidades, custos e termos anuais; não prometer funcionalidades ainda não verificadas.

**Efeitos.** A sequência troca receio difuso por responsabilidades verificáveis, respeita cada decisor e torna esforço visível. Sem urgência artificial.

**Gaps e QA.** Faltam ambiente do comprador, preço, termos e validações técnicas. **4/3/3/4/4/3/4/3/3/3** para solicitar proposta condicionada; contratação não liberada. Prevenir **F06, F10, F15, F18, F20 e F24**.

---

# holdout-005-vague-membership

## Candidate A

**Veredito.** Bloquear a persuasão para compra anual apoiada em crescimento ou aquisição de clientes. Reconstruir para avaliação informada da programação existente.

**Estado inicial.** Consultores consideram uma comunidade premium. Desejo de troca profissional é uma hipótese de adequação, não um fato sobre todos. A página induz expectativas empresariais que a evidência disponível não sustenta.

**Mecanismo de resultado: bloqueado.**

Participação em chamadas, chat, especialistas, templates e networking  
→ **mudança imediata relevante para aquisição de clientes: desconhecida**  
→ **comportamento comercial intermediário: desconhecido**  
→ receita, clientes ou “crescimento ilimitado”: **não sustentados**.

Não há metodologia definida que conecte esses elos. Background do fundador e número de membros não preenchem a lacuna.

Uma cadeia limitada é plausível: acesso aos recursos → oportunidade de contato com conteúdo e participantes → possível troca de informações. Ela depende de presença, relevância e interação efetiva; não comprova aprendizado aplicado, qualidade de conexões ou retorno financeiro. Confundidores de eventual crescimento: experiência, demanda, preço, prospecção externa e rede anterior. **Falsificador da cadeia limitada:** recursos acessíveis não produzem interação relevante para o participante. Resultados empresariais exigiriam outro mecanismo e evidência própria.

**Reconstrução antes da copy.**

| Bloco / operação | Antes → crença delimitada | Gate: passa / fallback |
|---|---|---|
| B1 · IDENTIFICATION | “Preciso crescer” → “Quero avaliar se esta programação atende uma necessidade concreta” | `relevance_gate`: consultor identifica tema ou interação desejada; sem correspondência, sinalizar inadequação. |
| B2 · TANGIBILIZATION | Lista genérica → entendimento do que está disponível e quando | Agenda e recursos sustentam descrição. `comprehension_gate`: consegue explicar formato e acesso; faltando detalhes, pedir esclarecimento. |
| B3 · MECHANISM / OBJECTION | “Networking muda tudo” → “Participação oferece oportunidades de troca; efeito comercial é desconhecido” | `plausibility_gate`: aceitar apenas a cadeia limitada. Se a decisão exigir aquisição de clientes, bloquear avanço. |
| B4 · PROOF | “Muitos membros provam eficácia” → “Tamanho e fundador não demonstram meu retorno” | `evidence_gate`: background sustenta credibilidade biográfica; contagem, se verificada, apenas dimensão. Sem resultados documentados, retirar promessas empresariais. |
| B5 · ACTION | “Preciso pagar um ano para descobrir” → “Posso examinar a oferta antes de assumir compromisso” | `readiness_gate`: permite consulta à programação; compra anual não passa com preço, termos e adequação desconhecidos. |

**DAG.** Necessidade de troca → programação compreendida → correspondência pessoal → limites aceitos → consulta aos detalhes. O ramo **participação → clientes/receita → retorno anual** permanece interrompido.

**Copy reconstruída.**

“Conheça a programação e os recursos da comunidade para consultores independentes.”

“Consulte os encontros previstos, os formatos de participação e os recursos disponíveis. Avalie sua relevância para os temas que você quer discutir e o tempo que poderá dedicar.”

“Não há resultados empresariais documentados que permitam prometer aquisição de clientes ou aumento de receita.”

CTA: **“Consultar programação e detalhes da participação.”** Não oferecer visita, teste gratuito, acesso a membros ou cancelamento flexível sem confirmação.

**Risco, identidade e tensão.** Reconhecer limitações preserva autonomia. Não sugerir que consultores ambiciosos precisam aderir. Retirar “crescimento ilimitado” e “a rede que muda tudo”; não substituir por outra promessa vaga.

**Gaps.** Preço, condições anuais, acesso efetivo, qualidade de participação, adequação dos temas e metodologia de resultados. Comprar acesso poderia ser racional por seu valor intrínseco, mas isso ainda precisa ser demonstrado ao comprador.

**QA.** Para a consulta informativa: **4/3/3/4/3/3/4/3/3/3**. Para venda anual por retorno empresarial: causalidade **0**, evidência **0**, prontidão **1**; bloqueada. Falhas originais: **F02, F04, F05, F06, F13, F18 e F24**. Estado terminal: reconstrução informativa pronta; promessa de eficácia e CTA anual bloqueados.

## Candidate B

**Initial-state model.** An independent consultant sees many activities but cannot tell whether participation will justify an annual commitment. “Unlimited growth” and “the network that changes everything” invite expectations the available evidence cannot substantiate.

**Reconstruction decision.** Remove those promises. Position the membership around its verified experience: scheduled calls, community chat, guest experts, templates, and networking. Founder background can explain perspective and relevant experience, but cannot substitute for member outcome evidence.

Suggested lead: **“A business community for independent consultants, with scheduled calls, shared resources, and opportunities to connect.”**

**Mechanism and its limits.** Calls and chat create opportunities to exchange questions and perspectives. Experts and templates may provide information or resources members choose to apply. Networking creates opportunities to meet others.

These are participation pathways, not an established client-acquisition or revenue mechanism. The connection from attendance to useful insight, application, changed business behavior, and business outcome remains unproven. Do not name a methodology that the offer does not possess.

**Belief sequence.**

1. “I understand what membership includes.”
2. “The actual schedule and activities fit my needs and availability.”
3. “I value access and participation even without promised financial returns.”
4. “I understand the limits and responsibilities.”
5. “The annual price and terms justify the commitment for me.”

The current evidence can support evaluation of participation. It cannot support belief that joining will reliably produce growth.

**Evidence and objections.**

- Show the current schedule to substantiate cadence and activity.
- Explain each verified feature concretely; avoid implying unlimited access or individualized advice.
- Use founder background for relevant credibility only.
- Member count, if current and verified, establishes size—not engagement, fit, introductions, or results.
- “Will I win clients?” remains unanswered by the evidence.
- “Will I participate enough?” requires schedule visibility and realistic participation expectations.
- “Who will I meet?” requires verified member-composition information; do not infer it from total membership.

**Architecture in dependency order.**

1. State who the community serves and what participation entails.
2. Show the current schedule and feature details.
3. Explain plausible uses of each activity without claiming business outcomes.
4. Present founder background and accurately bounded social proof.
5. Clarify suitability, participation demands, and limits.
6. Disclose annual price, access duration, renewal, cancellation, and other material terms.
7. Offer purchase only when the membership can be evaluated on that disclosed basis.

**CTA and blocked state.** The strongest presently supportable CTA is **“Review the membership schedule and included features.”** It should lead directly to that verified information.

The annual-purchase CTA is blocked in this reconstruction because material commercial terms are missing. Lack of outcome evidence alone does not prohibit selling a clearly described community experience. Once terms are verified, **“Join the annual membership”** can be appropriate for buyers who value that experience without a financial-return promise.

**Unresolved risks.** Price, terms, participation expectations, member composition, and the relevance or quality of resources are insufficiently established.

**Concise QA.** Remove unlimited-growth language; distinguish access from results; do not equate size with success; invent no methodology, testimonials, preview events, or guarantees; ensure the CTA leads to an available, accurately described next step.

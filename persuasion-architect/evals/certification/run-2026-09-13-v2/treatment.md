As evidências abaixo são as **relatadas nos briefs**; seus documentos e casos não foram disponibilizados para inspeção. Cadeias causais propostas estão identificadas como hipóteses, sem convertê-las em resultados comprovados.

Nas matrizes, cada linha depende das anteriores, salvo indicação contrária. O microcompromisso é verificar a condição de passagem; falhas acionam o fallback indicado. QA usa notas de 0–4, sem média compensatória: **continuidade, causalidade, evidência, especificidade, reconhecimento, objeções, identidade, risco, transições e prontidão**. As notas são autoavaliação, não certificação.

## holdout-001-legitimate-capacity

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

## holdout-002-ai-inbox-trial

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

## holdout-003-unsupported-guarantee

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

## holdout-004-onboarding-platform

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

## holdout-005-vague-membership

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
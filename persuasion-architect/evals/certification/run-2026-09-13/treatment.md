As evidências abaixo são as declaradas nos briefs; seus documentos não foram inspecionados. `supported` indica suporte à afirmação delimitada, não validação independente. Intervenções propostas não contam como provas existentes.

Na QA, notas de 0–4 seguem esta ordem: continuidade, clareza causal, adequação afirmação/evidência, especificidade, reconhecimento do público, objeções, identidade, risco, transições e prontidão. Qualquer dimensão crítica abaixo de 3 bloqueia a aprovação; autoavaliação não é certificação.

## case-001-contrarian-mechanism-book

**Contrato de decisão — architect.** Proprietários de serviços de alto valor, com chamadas qualificadas e fechamento inconsistente, devem considerar comprar o livro porque reconhecem uma oportunidade operacional, entendem sua aplicação e aceitam seus limites. Origem do tráfego, preço exato e condições comerciais: desconhecidos.

**Estado inicial.** Conhecido: atribuem o problema principalmente a scripts ou vendedores. Inferido: receio de mais conteúdo sem aplicação. Desconhecido: onde ocorrem suas perdas. Proibido inventar: superioridade universal do sistema ou aumento garantido de fechamento.

**Grafo completo de crenças.**

- P: há inconsistência relevante.
- C ← P: suas consequências merecem investigação, dimensionadas com dados próprios.
- R ← P: fatores fora da chamada também podem contribuir.
- M ← R: intervenções em pontos específicos da jornada têm uma lógica compreensível.
- S ← M: os templates permitem executar essas intervenções.
- K ← S + provas: o produto existe; dois casos documentam aplicações delimitadas.
- F ← M + K + contexto próprio: há compatibilidade com minha operação.
- V ← C + F + preço + esforço + alternativas: comprar pode compensar.
- D ← V + termos + limites: o risco total é aceitável.
- T ← D + disponibilidade operacional: posso aplicar agora, sem urgência artificial.
- A ← D + T: comprar é um próximo passo proporcional.

**Mapa de evidências e objeções.**

| Afirmação / objeção | Exigência e disponível | Estado / limite |
|---|---|---|
| “Inclui templates para pré-chamada, acompanhamento e demais etapas.” / “É só teoria?” | `artifact`: sumário e templates existentes | `supported`; demonstrar conteúdo real |
| “Fatores externos à chamada podem contribuir.” / “Preciso apenas de scripts.” | Lógica causal e demonstração de cada intervenção | `partially_supported`; hipótese aplicável, não diagnóstico individual |
| “Duas operações registraram mudanças.” / “Funcionou?” | `case_study` + medidas: contexto, período, definição, base e confundidores | `supported` quanto à existência; números específicos não fornecidos |
| “Vai elevar meu fechamento.” | Evidência preditiva aplicável | `unsupported`; casos não garantem resultado individual |

**Matriz de arquitetura.** Cada registro explicita operação, crenças, mecanismo, prova, efeitos e transição.

| Bloco / operação | Crença atual → desejada; objeção | Afirmação, mecanismo e prova | Emoção; identidade; risco; tensão | Microcompromisso, gate e sequência |
|---|---|---|---|---|
| B1 — IDENTIFICATION | “Falta um script” → “Preciso localizar perdas”; “Já sei o problema” | Examinar registros de chamadas e acompanhamento; `self_evidence` exige dados próprios | Frustração → curiosidade; gestor investigador; sem reduzir risco indevidamente; tensão fica específica | Localizar uma perda. `relevance_gate`: passa com ocorrência reconhecível; falha sem dados → mapear jornada. Próxima: R/B2 |
| B2 — REFRAME + MECHANISM | Causa única → hipótese sistêmica; “Como isso interfere?” | Mostrar um template real, sua intervenção e efeito esperado, distinguindo hipótese de resultado | Defesa → compreensão; capacidade de testar; esforço fica visível; resolve mistério causal | Explicar a cadeia. `comprehension_gate` + `plausibility_gate`: passa se cadeia faz sentido; falha → demonstração menor, sem prometer efeito. Próxima: S/B3 |
| B3 — PROOF | Plausível → aplicação documentada; “Serve para mim?” | Dois casos com início, intervenção, período, medidas e limites; não atribuir toda mudança ao livro | Ceticismo → confiança calibrada; comparação sem vergonha; incerteza explícita; tensão diminui | Comparar contextos. `evidence_gate`: passa para alegações delimitadas; dados insuficientes → retirar magnitude. Próxima: F/B4 |
| B4 — TANGIBILIZATION + OBJECTION | Livro abstrato → ferramenta avaliável; “Compensa implementar?” | Ligar cada template à lacuna correspondente; mostrar preço, esforço, alternativas e termos reais | Interesse → avaliação; autonomia; risco total visível; resolve custo oculto | Escolher primeira aplicação. Gate de relevância: passa com encaixe e custos claros; falha → consultar amostra. Próxima: V,D/B5 |
| B5 — ACTION | Valor reconhecido → compra consciente; “O que acontece depois?” | Explicar pagamento, acesso e primeiro passo somente após confirmação operacional | Cautela → decisão livre; sem coerção; termos delimitam risco; nenhuma pressão | `readiness_gate`: passa com preço, termos e aplicação aceitos; falha → permanecer na avaliação. Próxima: A/fim |

**Copy central:** “Antes de trocar o script, examine o que acontece antes e depois da chamada.”

**CTA:** “Comprar o livro por [preço confirmado]”. Não publicar o placeholder.

**Gaps e QA.** Faltam preço, termos, demonstração e detalhes dos casos. Riscos prevenidos: F04, F15, F20, F21. Remover B2 quebraria a lógica; remover B4 quebraria a avaliação de valor. QA: **4/3/3/4/3/3/4/2/3/2**. Arquitetura entregue; compra bloqueada até esclarecer risco e transação.

## case-002-generic-saas-feature-dump

**Veredito — audit.** A página comprova disponibilidade de funcionalidades, mas não constrói uma razão suficiente para uma equipe pequena assumir um plano anual. Falhas centrais: F05, F06, F03, F18 e F24.

**Contrato de decisão.** A contratação anual exige que a equipe identifique um fluxo relevante, compreenda como o software o atende, verifique compatibilidade e aceite custos e compromisso. Preço, integrações específicas, migração, termos e origem do tráfego não foram fornecidos.

Conhecido: público avalia software de workflow. Inferido: receio de ferramentas que acrescentam trabalho. Desconhecido: gargalo principal e alternativas atuais.

**Auditoria em ordem da página.**

| Bloco visível | Trabalho persuasivo pretendido | Dependência ausente e reparo |
|---|---|---|
| “Work smarter, move faster.” | Atenção e desejo de produtividade | Não identifica situação concreta nem explica velocidade. F05; substituir por fluxo verificável |
| Automação, dashboards, integrações, IA, analytics, colaboração | Demonstrar capacidade | Funcionalidade → mudança operacional → relevância não são conectadas. F06; selecionar apenas recursos necessários ao fluxo |
| Seis relatos “great” e “easy” | Credibilidade e redução de receio | Opiniões não demonstram desempenho ou facilidade para este público. F03 se usadas assim; contextualizar relatos |
| Preço depois dos cards | Converter capacidade em valor | Faltam custos de adoção e adequação. F24/F15; explicitar custo anual e implementação |
| “Transform your business today.” | Contratação imediata | Convicção insuficiente para compromisso anual. F18; ajustar ação ao estágio demonstrado |

**Grafo necessário.**

Gargalo reconhecido → causa operacional compreendida → fluxo demonstrado → funcionalidades adequadas → compatibilidade validada → valor comparado às alternativas → custo e risco anual aceitos → contratação.

Credibilidade documental sustenta “o recurso existe”; não substitui os nós de resultado, compatibilidade ou valor.

**Registro de evidências.**

- Existência das funcionalidades: `supported`, por documentação (`artifact`). Verificar disponibilidade por plano.
- “Mais rápido”: `unsupported` como promessa de resultado; requer comparação definida, contexto, tarefas e medição.
- “Fácil”: `partially_supported` como percepção dos depoentes; não como propriedade universal. Identidade, contexto e autenticidade não foram fornecidos.
- “Transformação do negócio”: `unsupported`; amplitude incompatível com as evidências.
- Economia ou retorno financeiro: nenhum dado fornecido; não inserir percentuais nem estimativas atribuídas a clientes.

**Reconstrução em ordem de dependência.**

1. **R1 — IDENTIFICATION.** Indefinição → reconhecimento de um gargalo. Selecionar um fluxo real do público, ainda a confirmar. Emoção: dispersão → foco. Microcompromisso: reconhecer situação observável. `relevance_gate`: passa com correspondência; falha → escolher outro fluxo, sem fabricar reconhecimento.
2. **R2 — MECHANISM + DEMONSTRATION.** Lista de recursos → compreensão da intervenção. Mostrar entrada, regra, responsável e saída, usando somente capacidades documentadas. `comprehension_gate` e `plausibility_gate`: passa se a equipe explica o fluxo; falha → reduzir escopo da demonstração. Próximo: validação.
3. **R3 — PROOF + OBJECTION.** Possibilidade → adequação verificada. Demonstrar o fluxo com dados representativos e conferir integrações. `evidence_gate`: passa para funcionamento observado, não para ROI geral; falha → registrar incompatibilidade e interromper venda anual.
4. **R4 — VALUE_EXPANSION + RISK_REVERSAL.** Adequação → escolha econômica. Expor total anual, migração, treinamento, limites, renovação e cancelamento reais. Identidade: equipe competente para escolher; risco permanece explícito. Gate: passa com custos e responsáveis aceitos; falha → esclarecer termos.
5. **R5 — ACTION.** Comparação → decisão. CTA provisório: “Ver como funciona no seu fluxo”, somente se esse atendimento for disponibilizado. `readiness_gate`: anual apenas após R1–R4; falha → demonstração ou avaliação, sem inventar teste gratuito.

**Gaps e QA.** Não há base para declarar todos os cards ou depoimentos redundantes sem conteúdo integral; remover os que não acrescentarem aplicação ou prova. A nova sequência reduz tensão por esclarecimento, sem pressão.

QA atual: **1/1/1/1/2/1/2/1/0/0**. Reconstrução especificada, ainda não validada: **4/3/3/3/3/3/4/2/3/2**. Plano anual permanece bloqueado pelos custos e compatibilidade desconhecidos.

## case-003-fake-urgency-pressure

**Veredito — reconstruct.** Remover imediatamente o contador que reinicia e a alegação de sete vagas. São falsos fundamentos de decisão, não elementos a reposicionar. F08 crítico; F07 pelo uso de pressão antes da convicção.

**Contrato de decisão.** Criadores devem comprar o curso somente após entenderem currículo, forma de aprendizagem, adequação, esforço e condições. O curso é evergreen, autoinstrucional; não existe escassez de matrícula informada.

**Estado mental.** Conhecido: a página antecipa o CTA e usa screenshots sem contexto. Inferido: leitores podem desconfiar da promessa e temer comprar conteúdo inadequado. Desconhecidos: especialidade, nível exigido, preço, carga de trabalho, acesso e suporte.

**Dependências.**

Necessidade de aprendizagem → habilidade pretendida → lógica do percurso curricular → credibilidade do instrutor → adequação pessoal → valor frente a preço e esforço → risco aceitável → disponibilidade para estudar → compra.

Depoimentos apoiam experiências específicas após o leitor entender o que está sendo ensinado. Não substituem currículo ou mecanismo.

**Evidências e limites.**

| Afirmação | Evidência / estado | Fronteira |
|---|---|---|
| Curso contém determinado percurso | Currículo, `artifact`; `supported` quanto à existência | Conteúdo específico precisa ser extraído do material |
| Instrutor tem experiência relevante | Histórico, `authority`; `supported` no escopo documentado | Não demonstra resultado de todo aluno |
| Três alunos relatam experiências | Depoimentos verificáveis, `testimonial`; `supported` como relatos | Não generalizar frequência, magnitude ou causalidade |
| Screenshots provam resultados | Sem contexto; `unverifiable_from_available_inputs` | Retirar até esclarecer origem, período e significado |
| “Só sete vagas” | Matrícula ilimitada; afirmação contradita | Excluir, sem substituir por outra escassez |
| Prazo de compra termina no contador | Reinício a cada visita; fundamento falso | Excluir |

**Arquitetura reconstruída, antes da copy.**

1. **B1 — IDENTIFICATION.** “Não sei se este curso me serve” → “Esta habilidade é relevante para meu trabalho”. Mostrar problema e público somente conforme currículo confirmado. Mecanismo: conectar tarefa real à habilidade ensinada. Emoção: dúvida → orientação; identidade de aprendiz autônomo. Microcompromisso: selecionar objetivo. `relevance_gate`: passa com correspondência explícita; falha → informar ausência de fit. Próximo: B2.
2. **B2 — MECHANISM + TANGIBILIZATION.** “É uma coleção de aulas?” → “Entendo o percurso”. Relacionar módulos às habilidades e práticas efetivamente existentes. Prova requerida/disponível: currículo; demonstração adicional ainda não fornecida. `comprehension_gate` + `plausibility_gate`: passa quando sequência e aplicação são explicáveis; falha → esclarecer percurso, sem inventar exercícios. Próximo: B3.
3. **B3 — PROOF.** “Por que confiar?” → “Conheço a experiência da fonte e os limites dos relatos”. Apresentar histórico relevante e três testemunhos contextualizados. Ceticismo → confiança delimitada; risco de expectativa exagerada diminui. `evidence_gate`: passa apenas para afirmações documentadas; falha → excluir trecho ou reduzir alegação. Próximo: B4.
4. **B4 — OBJECTION + FRICTION_REMOVAL.** “Posso acompanhar?” → “Conheço requisitos e compromisso”. Informar nível, tempo, preço, acesso, suporte e política comercial confirmados. Microcompromisso: conferir recursos e disponibilidade. Gate de relevância: passa com fit e termos claros; falha → adiar compra. Risco financeiro e esforço permanecem visíveis. Próximo: B5.
5. **B5 — ACTION.** “Entendo a oferta” → “Escolho começar quando puder aplicar”. Nenhuma urgência comercial. `readiness_gate`: passa após B1–B4; falha → voltar ao currículo ou esclarecer termos. CTA final: “Comprar o curso por [preço confirmado]”. Destino: checkout com condições consistentes.

**Copy utilizável com os fatos atuais:** “Conheça o currículo, a experiência do instrutor e os relatos de alunos. Avalie se este curso autoinstrucional combina com o que você precisa aprender.”

Antes da prontidão, usar navegação “Ver currículo”, sem tratá-la como compromisso de compra.

**Gaps, falhas e QA.** F03/F04 ameaçam o uso dos screenshots; F18 caracteriza o CTA antecipado. Corrigir a pressão não resolve sozinho a falta de explicação. Não inventar garantias ou resultados para compensá-la.

QA da reconstrução com os insumos atuais: **4/2/3/2/3/3/4/2/3/2**. Publicação comercial bloqueada até preencher currículo específico e termos; nenhuma média supera esses gates.

## case-004-high-ticket-consulting

**Contrato de decisão — offer.** Empresas de médio porte devem agendar uma conversa diagnóstica qualificada porque identificam uma questão operacional relevante e consideram a equipe apta a investigá-la. O agendamento não exige acreditar em ROI garantido nem decidir antecipadamente pela implementação.

Conhecido: diagnóstico mais implementação de 12 semanas, preço significativo de cinco dígitos e decisão com vários stakeholders. Moeda, preço exato e relação comercial entre chamada, diagnóstico e implementação: desconhecidos.

**Estado inicial.** Inferido: interesse em IA acompanhado de receio de projetos caros e adoção difícil. Não assumir maturidade técnica, orçamento disponível ou consenso interno.

**Grafo.**

Questão operacional relevante → possibilidade de investigação útil → processo compreensível → equipe credível → fit preliminar → utilidade da conversa superior ao seu custo e exposição → participantes e expectativas claros → agendamento.

A decisão de implementação tem outro gate: diagnóstico concluído + viabilidade + escopo + recursos + aprovação dos stakeholders + contrato.

**Registro de evidências.**

- Credenciais e histórico: `supported` para competência documentada (`authority`); não provam economia futura.
- Processo detalhado: `supported` como desenho de entrega (`artifact`); execução previsível depende de responsabilidades e condições.
- Um caso com economia medida: `supported` como resultado daquele cliente (`case_study`, `quantitative`); divulgar baseline, período, definição, fonte e confundidores antes de citar magnitude.
- Referências qualitativas: `supported` como experiências relatadas; não como previsão financeira.
- ROI garantido: `unsupported`; excluir. Não converter a economia do caso em expectativa padrão.

**Arquitetura da oferta e transições.**

| Bloco / operação | Mudança, mecanismo e objeção | Gate: passa / falha e fallback |
|---|---|---|
| B1 — IDENTIFICATION | “Precisamos de IA” → “Temos uma questão operacional investigável”. Usar observações do prospect, sem quantificar perdas presumidas. Ansiedade → foco; microcompromisso: nomear processo e responsável | `relevance_gate`: processo e problema identificáveis / demanda vaga → exploração inicial, sem prometer projeto |
| B2 — MECHANISM | “Consultoria abstrata” → “Entendo como investigam e implementam”. Mostrar etapas do processo real e dependências do cliente. Objeção: execução e interrupção operacional | `comprehension_gate` + `plausibility_gate`: responsabilidades e lógica explicáveis / lacuna → esclarecer processo. Próximo: B3 |
| B3 — PROOF | “Pode ser discurso” → “Há experiência pertinente”. Credenciais, caso delimitado e referências após explicar o processo. Ceticismo → confiança calibrada | `evidence_gate`: prova sustenta competência para investigar / contexto incompatível → reconhecer limite, não prometer economia. Próximo: B4 |
| B4 — OBJECTION | “A chamada inicia uma venda opaca” → “Conheço compromisso e finalidade”. Informar agenda, duração, participantes, custo se houver e uso de dados | Gate de risco: expectativas aceitas / termos ausentes → esclarecer antes de agendar. Próximo: B5 |
| B5 — ACTION | “Pode ser útil” → “Vale conversar”. Pedir apenas dados necessários à qualificação, sem exigir informações sensíveis nesta etapa | `readiness_gate`: problema, fit e condições da chamada claros / falha → material de processo ou esclarecimento. CTA: “Solicitar conversa diagnóstica” |

**Modelo de risco total.**

| Exposição | Tratamento proposto, sujeito a acordo |
|---|---|
| Honorários e custo de oportunidade | Preço, escopo e alternativas explícitos; nenhuma âncora fictícia |
| Tempo interno e mudança organizacional | Responsáveis, disponibilidade, treinamento e critérios de adoção |
| Integrações, dados e continuidade | Dependências técnicas, acesso mínimo, validação e plano de reversão |
| Reputação e decisão coletiva | Incluir patrocinador, operação, TI e demais aprovadores pertinentes |
| Resultado incerto | Critérios mensuráveis e decisão de avançar ou parar após diagnóstico; sem ROI garantido |

**Compromisso e ativação.** Proposta de sequência: conversa → diagnóstico com termos próprios → decisão sobre implementação → início das 12 semanas. Não afirmar contratação separada como condição já existente. Não adicionar bônus; eventuais materiais devem resolver preparação ou adoção. Sem urgência: prioridade depende de um problema real e capacidade interna.

**Gaps e QA.** Faltam condições da chamada, critérios de qualificação e detalhes do caso. Identidade deve apoiar decisão responsável, sem vergonha por “ficar para trás”. Riscos: F04, F15, F17, F18.

QA: **4/3/3/4/3/3/4/3/3/2**. Arquitetura adequada à conversa; ativar agendamento após esclarecer seu compromisso. Contratação permanece em gate separado.

## case-005-evidence-gap

**Veredito — architect.** A experiência do fundador permite apresentar uma metodologia usada em seu próprio negócio. Não permite vender como comprovadas a triplicação de leads, a aplicação universal ou a suficiência definitiva do sistema.

**Contrato de decisão.** Proprietários podem avaliar uma turma premium se compreenderem o método, suas condições e sua incerteza. Com os insumos atuais, a inscrição paga ainda não está justificada. A ação imediata proporcional é conhecer o conteúdo e as condições, caso esse caminho seja disponibilizado.

**Estado inicial.** Conhecido: interesse em geração de leads. Inferido: desejo de previsibilidade e ceticismo sobre novas fórmulas. Desconhecidos: gargalos, setores, recursos, maturidade e disposição para experimentar. Não presumir que falta de leads seja o único problema comercial.

**Registro de afirmações.**

| Afirmação desejada | Evidência necessária / disponível | Estado e decisão |
|---|---|---|
| “Triplique leads qualificados em 30 dias” | Medição de baseline, definição de qualificação, prazo, fonte, atribuição e replicações pertinentes; nada disso foi fornecido | `unsupported`; excluir número e prazo |
| “Funciona em todos os setores” | Evidência ampla entre setores e condições; não há dados multissetoriais | `unsupported`; excluir universalidade |
| “O único sistema de que você precisará” | Sustentação de exclusividade e suficiência futura; inexistente | `unsupported`; excluir absoluto e falsa alternativa |
| “O fundador usou o método em seu negócio” | Relato fornecido no brief | `supported` como experiência declarada; documentação não fornecida |
| “O método gera resultados para clientes” | Casos documentados; nenhum disponível | `unsupported` |
| “Método proprietário” | Designação da oferta | Não prova novidade, exclusividade comparativa ou eficácia |

**Grafo de crenças e dependências.**

P: problema específico reconhecido  
→ M: etapas e mecanismo compreendidos  
→ L: limites da experiência do fundador conhecidos.

M + L + contexto do prospect → F: adequação possível, ainda incerta.

F + currículo + suporte + esforço + preço + alternativas → V: valor educacional avaliável.

V + termos + risco de não obter resultados → R: exposição conscientemente aceitável.

R + disponibilidade de aplicação → A: eventual inscrição.

**Gate atualmente quebrado:** M. O funcionamento do método não foi descrito. “Proprietário” não instala plausibilidade.

**Matriz da arquitetura mais forte permitida.**

| Bloco / operação | Transição, prova e efeitos | Passagem / falha / próximo passo |
|---|---|---|
| B1 — IDENTIFICATION | Interesse genérico → problema identificável. Usar dados próprios sobre volume e qualificação, sem sugerir números. Emoção: expectativa → precisão; identidade: gestor que investiga | `relevance_gate`: problema observável / ausência → diagnóstico, sem afirmar necessidade da turma. Microcompromisso: definir gargalo. Próximo B2 |
| B2 — MECHANISM | “Existe um segredo” → “Entendo etapas, insumos e hipótese causal”. Exigir descrição real e demonstração; não disponíveis. Reduzir mistério, tornar esforço visível | `comprehension_gate` + `plausibility_gate`: cadeia explicável e testável / falha atual → obter descrição; bloquear argumento de eficácia. Próximo B3 somente após passagem |
| B3 — PROOF + TRANSPARENCY | “Deve estar comprovado” → “Conheço a experiência disponível e sua limitação”. Apresentar uso pelo fundador; resultados somente se documentados. Confiança calibrada, sem promessa | `evidence_gate`: afirmações restritas ao que estiver documentado / ausência → manter relato sem magnitude. Microcompromisso: reconhecer incerteza. Próximo B4 |
| B4 — TANGIBILIZATION + OBJECTION | “Vou comprar leads futuros” → “Avalio uma experiência educacional”. Exigir currículo, entregas, suporte, esforço, preço e requisitos reais; não inventar acompanhamento ou feedback | Gate de relevância/valor: oferta concreta e compatível / ausência → apenas apresentação preliminar. Risco financeiro e implementação explícitos. Próximo B5 |
| B5 — ACTION | Interesse → compromisso informado. Expor possibilidade de nenhum ganho comercial e alternativas, incluindo não comprar | `readiness_gate`: compreensão, fit, valor e termos aceitos / falha atual → suspender inscrição paga. Sem escassez ou urgência presumida |

**Copy central possível:** “Conheça uma metodologia de geração de leads usada pelo fundador em seu próprio negócio. Ainda não há casos documentados de clientes nem dados entre setores. Avalie seu funcionamento e seus limites antes de decidir participar.”

**CTA atual proposto:** “Conhecer o método e as condições da turma”. Não publicar sem disponibilizar essas informações.

**Gaps e QA.** Faltam mecanismo, documentação da experiência, currículo, entregas, preço e termos. Uma turma piloto é uma opção de redesenho, não um fato existente nem autorização para prometer resultados.

Falhas: F02, F04, F13, F14 e F18; F08 se alguém inventar vagas limitadas. QA: **4/1/4/2/3/2/4/1/1/1**. As alegações indevidas foram rejeitadas; inscrição premium bloqueada. Transparência não substitui os requisitos materiais ausentes.
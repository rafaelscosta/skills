# Política de reembolso — fixture de integração

1. O atendimento recebe o pedido de reembolso e confirma o identificador do pedido.
2. Um pedido é elegível quando foi solicitado em até 7 dias da compra e não houve consumo do conteúdo premium.
3. Se as duas condições forem verdadeiras, o atendimento aprova o reembolso.
4. Se qualquer condição falhar, o atendimento nega o reembolso e informa o motivo ao cliente.
5. Depois da aprovação, o processamento financeiro pode levar de 3 a 5 dias úteis. Esse prazo não altera a decisão de elegibilidade.
6. Se os dados do pedido estiverem incompletos, o atendimento não deve aprovar nem negar; deve solicitar os dados faltantes e retomar a análise depois.

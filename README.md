Mayran Juvenal Milani
Simone Tatiane do Canto
18/11/2026


# P2-PROVA-PRATICA-DE-SISTEMAS-DISTRIBUIDOS

1. situação problema
   Descreva brevemente os problemas apresentados na central de pedidos distribuida.

R: O sistema não respeitava o limite de pedidos simultâneos, não mantinha os servidores consistentes e não aproveitava a réplica na falha do principal. As correções aplicadas resolveram os três pontos: limite em 2, sincronização copiando do principal e consulta usando a réplica quando o principal está offline.

2. Primeira execução
   Explique o que foi observado ao executar o programa pela priemira vez.
R: O programa executou sem erros e sem travar, mas o resultado estava incorreto em três pontos: o limite de pedidos simultâneos, a atualização da réplica e a consulta após a falha. Esses problemas não geram mensagem de erro, por isso só aparecem quando se compara a saída com o que era esperado.

Evidência 1 = (evidencia1.png)


3. Problema A - Concorrência
   Qual problema foi identificado?
   
   R: A empresa necessitava que o limite de processamento simultaneo fosse 2, porém inicialmente eram 3 processamentos.

   Qual alteração foi realizada?
   
R: Precisei apenas alterar a linha "MAXIMO_SIMULTANEO" de 3 para 2. Ela foi modificada pois definia o limite de processamento simultânio e conforme pedido pela empresa precisavamos alterar para apenas dois pedidos em processamento.

Evidencia 2: Concorrência

(evidencia2.png)

4. Problema B - Problema B - Replicação e consistência

Qual problema foi identificado?
A réplica não recebia o estoque atualizado do servidor principal. Depois do processamento dos pedidos, o principal ficava com 7 unidades e a réplica continuava com 10. A função de sincronização copiava o valor da réplica para ela mesma, então nada era atualizado e os dois servidores ficavam inconsistentes.

Qual alteração foi realizada?
Na função de sincronização, a origem do valor passou a ser o estoque do servidor principal, e a cópia foi protegida pela trava para não ocorrer no meio de uma atualização. Com isso, a réplica passou a receber o valor atualizado (7), e os dois servidores ficaram consistentes.

Evidencia 3 - sincronização

(evidencia3.png)

5 PROBLEMA C - TOLERÂNCIA A FALHAS

Qual problema foi identificado?
A função de consulta não utilizava a réplica quando o servidor principal ficava indisponível. O segundo teste de disponibilidade verificava o servidor principal novamente, em vez de verificar a réplica. Por isso, quando o principal caía, as duas condições falhavam e o sistema respondia “indisponível”, mesmo com a réplica funcionando.

Qual alteração foi realizada?
No segundo teste da função de consulta, a condição foi trocada para verificar se a réplica está online. Com isso, quando o principal fica offline, a consulta passa a ser respondida pela réplica, que retorna o estoque de 7 unidades. O sistema só informa “indisponível” se os dois servidores estiverem fora do ar.
Passo 3 - verificar

Evidencia 4 - tolerancia a falhas

(evidencia4.pnh)

6. validação do programa
descreva os resultados observados após as três correções. 

R:Após aplicar as três correções, o programa foi executado novamente e os resultados foram:

Limite de concorrência: o sistema exibiu limite simultâneo igual a 2, de acordo com a regra da empresa. O pico medido de pedidos em processamento ao mesmo tempo foi 2, e o terceiro pedido aguardou uma vaga.
Processamento dos pedidos: os três pedidos (101, 102 e 103) foram confirmados.
Servidor principal: o estoque foi atualizado de 10 para 7 unidades.
Réplica: antes da sincronização estava com 10 unidades e, depois, passou a ter 7, igual ao principal.
Falha simulada: com o principal offline, a consulta continuou funcionando e retornou a réplica com 7 unidades.

Evidencia 5 - execução completa

(evidencia5.png)

7. Analise técnica
  
1. Qual é a função do semáforo no processamento dos pedidos?

Ele limita quantos pedidos são processados ao mesmo tempo. Aqui, no máximo 2. O terceiro pedido espera um dos outros terminar, como numa loja com dois caixas.

2. Por que é necessário sincronizar os dados entre o servidor principal e a réplica?

Porque os pedidos só atualizam o principal. Sem sincronizar, a réplica fica com 10 unidades enquanto o principal tem 7. Se o principal cair, a réplica passaria uma informação errada.

3. O que significa tolerância a falhas e como ela aparece neste programa?

É o sistema continuar funcionando mesmo quando uma parte dele falha. Aqui, quando o principal cai, consultar_estoque() passa a usar a réplica e responde REPLICA 7. O usuário continua sendo atendido.

4. Para que serve o lock no programa e como o controle de acesso aos recursos ajuda a prevenir problemas de concorrência?

O lock deixa só uma thread por vez alterar o estoque. Sem ele, dois pedidos poderiam ler o mesmo valor ao mesmo tempo e uma baixa se perderia (condição de corrida). Com o lock, cada baixa é concluída antes da próxima, e o estoque final fica correto.

5. A sincronização deve acontecer antes ou depois do processamento dos pedidos? Qual é a relação de causalidade?

Depois. Os pedidos mudam o estoque (10 → 7), e a sincronização leva essa mudança para a réplica. Se viesse antes, copiaria o valor antigo. E precisa acontecer antes da falha, porque com o principal fora do ar não há de onde copiar.


8. Conclusão
R: Com essa atividade, aprendi que um sistema distribuído pode executar sem nenhuma mensagem de erro e, mesmo assim, estar incorreto. Os três problemas do código original (limite acima da regra, réplica desatualizada e consulta que ignorava a réplica) não travaram o programa, e só foram percebidos ao comparar a saída com o resultado esperado. Isso mostra a importância de testar e validar o comportamento do sistema, e não apenas verificar se ele roda.

9. entrega

Mayran Juvenal Milani


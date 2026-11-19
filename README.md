# P2-PROVA-PRATICA-DE-SISTEMAS-DISTRIBUIDOS

Evidência 1 = 
PS C:\Users\aluno\Documents\simulado_distribuidos> python --version
Python 3.13.7
PS C:\Users\aluno\Documents\simulado_distribuidos> python central_pedidos.py
=== CENTRAL DE PEDIDOS ===
limite simultaneo: 3
Estoque inicial: 10
Pedidos confirmados: [101, 102, 103]
Estoque principal: 7
Replica antes 10
Replica depois 10
Consulta apos falha: INDISPONIVEL None
PS C:\Users\aluno\Documents\simulado_distribuidos> 


Problema A - Concorrência
Evidencia 2:

PS C:\Users\aluno\Documents\simulado_distribuidos> python central_pedidos.py
=== CENTRAL DE PEDIDOS ===
limite simultaneo: 2
Estoque inicial: 10
Pedidos confirmados: [101, 102, 103]
Estoque principal: 7
Replica antes 10
Replica depois 10
Consulta apos falha: INDISPONIVEL None
PS C:\Users\aluno\Documents\simulado_distribuidos> 

Explicação = Precisei apenas alterar a linha "MAXIMO_SIMULTANEO" de 3 para 2. Ela foi modificada pois definia o limite de processamento simultânio e conforme pedido pela empresa precisavamos alterar para apenas dois pedidos em processamento.


Problema B - Replicação e consistência
Evidência 3:

Após a sincronização, os dois servidores mostram o mesmo valor:

Estoque principal: 7
Replica depois 7

Em código, para exibir os dois lado a lado logo depois de sincronizar():

sincronizar()

print("Estoque principal após sincronização:", principal["estoque"])
print("Estoque réplica após sincronização:", replica["estoque"])

Saída:

Estoque principal após sincronização: 7
Estoque réplica após sincronização: 7

Os 3 pedidos (101, 102 e 103) foram confirmados, então o estoque do principal caiu de 10 para 7, e a sincronização copiou esse valor para a réplica. Isso vale com o limite simultâneo em 2, pois ele só afeta o tempo de execução, não o resultado final.

PROBLEMA C - TOLERÂNCIA A FALHAS
Evidência 4:

=== CENTRAL DE PEDIDOS ===
limite simultaneo: 2
Estoque inicial: 10
Pedidos confirmados: [101, 102, 103]
Estoque principal: 7
Replica antes 10
Replica depois 7
Consulta apos falha: REPLICA 7

Conclusão: mesmo com o principal fora do ar, o sistema continuou respondendo consultas por meio da réplica, com o valor correto de 7 unidades. Isso comprova a tolerância a falhas exigida no Problema C.

Passo 3 - verificar

Observe se:
1. O limite de processamento simultaneo está de acordo com a regra da empresa
2.os três pedidos foram processados.
3. i estoque principal foi atualziado.
4. a replica recebeu a atualização;
5. a consulta continua funcionando após a falha simulada do servidor princiapl.

Etapa 5 análise técnica

Etapa 5 - Análise técnica

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


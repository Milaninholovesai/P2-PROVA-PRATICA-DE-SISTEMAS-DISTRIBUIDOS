import threading
import time

# Servidores simulados
principal = {"online": True, "estoque": 10}
replica = {"online": True, "estoque": 10}

# Controle de concorrencia
# Regra da empresa: apenas 2 pedidos em processamento simultaneo
MAXIMO_SIMULTANEO = 2
semaforo = threading.Semaphore(MAXIMO_SIMULTANEO)
trava = threading.Lock()
pedidos_confirmados = []

# Contadores usados apenas para verificar o limite (evidencia)
ativos = 0
pico = 0


def processar_pedido(numero):
    global ativos, pico
    with semaforo:
        with trava:
            ativos += 1
            pico = max(pico, ativos)

        time.sleep(0.1)

        with trava:
            if principal["estoque"] > 0:
                principal["estoque"] -= 1
                pedidos_confirmados.append(numero)
            ativos -= 1


def sincronizar():
    # Correcao: a origem do valor agora e o servidor principal
    with trava:
        replica["estoque"] = principal["estoque"]


def consultar_estoque():
    if principal["online"]:
        return ("PRINCIPAL", principal["estoque"])

    # Correcao: antes testava principal["online"] de novo
    if replica["online"]:
        return ("REPLICA", replica["estoque"])

    return "INDISPONIVEL", None


print("=== CENTRAL DE PEDIDOS ===")
print("limite simultaneo:", MAXIMO_SIMULTANEO)
print("Estoque inicial:", principal["estoque"])

trabalhadores = [
    threading.Thread(target=processar_pedido, args=(numero,))
    for numero in [101, 102, 103]
]

for trabalhador in trabalhadores:
    trabalhador.start()

for trabalhador in trabalhadores:
    trabalhador.join()

print("Pedidos confirmados:", sorted(pedidos_confirmados))
print("Estoque principal:", principal["estoque"])
print("Replica antes", replica["estoque"])

sincronizar()

print("Replica depois", replica["estoque"])
print("Estoque principal apos sincronizacao:", principal["estoque"])
print("Estoque replica apos sincronizacao:", replica["estoque"])

# Simulacao de falha
principal["online"] = False

nome, estoque = consultar_estoque()
print("Consulta apos falha:", nome, estoque)

# Verificacao (Passo 3)
print()
print("=== VERIFICACAO ===")
print("1. Limite = 2 .............", "OK" if MAXIMO_SIMULTANEO == 2 and pico <= 2 else "FALHOU", f"(pico: {pico})")
print("2. 3 pedidos processados ..", "OK" if len(pedidos_confirmados) == 3 else "FALHOU")
print("3. Principal atualizado ...", "OK" if principal["estoque"] == 7 else "FALHOU")
print("4. Replica sincronizada ...", "OK" if replica["estoque"] == 7 else "FALHOU")
print("5. Consulta apos falha ....", "OK" if (nome, estoque) == ("REPLICA", 7) else "FALHOU")

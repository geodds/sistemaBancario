menu = '''
[d]Depositar
[s]Sacar
[e]Extrato
[q]Sair

Escolhe uma opcao: 
'''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == 'd':
        valor = float(input("Qual valor deseja depositar?"))

        if valor > 0: #valores negativos nao vai ser aceito
            saldo += valor
            extrato += f"Deposito de R$ {valor:.2f} \n"

        else:
            print("Valor invalido.")

    elif opcao == 's':
        valor = float(input("Qual valor deseja sacar? "))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saque = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Saldo insuficiente")

        elif excedeu_limite:
            print("Voce excedeu o valor do limite")

        elif excedeu_saque:
            print("Voce ja excedeu o limite de saques diarios")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque de R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Valor invalido.")
   
    elif opcao == 'e':
        print("EXTRATO")
        print("Nao foram realizados nenhuma movimentacao." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")

    elif opcao == 'q':
        break

    else:
        print("Opcao invalida, tente novamente.")



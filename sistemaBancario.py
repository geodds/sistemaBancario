import textwrap

def menu():
    menu = '''
    [d]Depositar
    [s]Sacar
    [e]Extrato
    [nu]Novo Usuario
    [lc]Listar Contas
    [nc]Nova Conta
    [q]Sair

    Escolha uma opcao: 
    '''
    return input(menu)

def depositar(saldo, valor, extrato, /): #argumentos apenas por posicao
    if valor > 0:
        saldo += valor
        extrato += f"Deposito de R$ {valor:.2f} \n"
        print("Deposito realizado com sucesso!")
    else:
        print("ERROR! Valor invalido.")

        return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): #argumentos apenas por nome
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_saques >= limite_saques

    if excedeu_saldo:
            print("Saldo insuficiente.")

    elif excedeu_limite:
            print("Voce excedeu o valor do limite.")

    elif excedeu_saque:
            print("Voce ja excedeu o limite de saques diarios.")
    if valor <= saldo:
        salod -= valor
        extrato += f"Saque de R$ {valor:.2f} \n"
    else:
        print("Valor insuficiente.")

        return saldo, extrato
    
def exibir_extrato(saldo, /, *, extrato): #argumentos por posicao e nome
    print("EXTRATO")
    print("Nao foram realizados nenhuma movimentacao." if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}")

def filtrar_usuario(cpf, usuarios): #filtra se existe usuario ja cadastrado com o mesmo CPF
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    
def criar_usuario(usuarios):

    cpf = input("Informe seu numero de CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
         print("ERROR! CPF ja cadastrado. ")
         return

    nome = input("Informe seu nome completo: ")
    nascimento = input("Informe sua data de nascimento: ")
    endereco = input("Informe seu endereco: ")

    usuarios.append({"cpf": cpf, "nome": nome, "nascimento": nascimento, "endereco": endereco})
    print("Usuario cadastrado com sucesso!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 50)
        print(textwrap.dedent(linha))

def criar_conta(agencia, numero_conta, usuarios):
     cpf = input("Informe seu CPF: ")
     usuario = filtrar_usuario(cpf, usuarios)
     if usuario:
          print("\nConta criada com sucesso!")
          return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
     
     print("\nUsuario nao encontrado")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
             valor = float(input("Informe o valor do deposito: "))
             saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
             valor = float(input("Qual valor deseja sacar? "))
             sacar(saldo=saldo, valor=valor,extrato=extrato,limite=limite,
                   numero_saques=numero_saques,limite_saques=LIMITE_SAQUES)
             
        elif opcao == "e":
             exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
             criar_usuario(usuarios) 
        
        elif opcao == "lc":
             listar_contas(contas)

        elif opcao == "nc":
            numero_conta = len(contas) + 1 #vai criar uma sequencia para os numeors das contas
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta) 

        elif opcao == "q":
             break
         
        else:
             print("Opcao invalida. Tente novamente")

main()
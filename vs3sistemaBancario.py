import textwrap
from abc import ABC, ABCMeta, abstractclassmethod,abstractproperty
from datetime import datetime

class Cliente:
     def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

     def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

     def adicionar_conta(self, conta):
        self.contas.append(conta)
          

class PessoaFisica(Cliente):
     
     def __init__(self, nome, nascimento, cpf, endereco):
          super().__init__(endereco)
          self.nome = nome
          self.nascimento = nascimento
          self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agenciao(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
     saldo = self.saldo
     excedeu_saldo = valor > saldo

     if excedeu_saldo:
            print("ERROR!!! Saldo insuficiente.")

     elif valor > 0:
         self._saldo -= valor
         print("Saque realizado com sucesso!")
         return True
     
     else:
        print("ERROR!!! Valor insuficiente ou invalido.")

     return False       

    def depositar(self, valor): 
        if valor > 0:
            self._saldo += valor
            extrato += f"Deposito de R$ {valor:.2f} \n"
            print("Deposito realizado com sucesso!")
        else:
            print("ERROR! Valor invalido.")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

        def sacar(self, valor):
            numero_saques = len(
                [transacao for transacao in self.historico.transacao if transacao["tipo"] == Saque.__name__]
            )

            excedeu_limite = valor > self.limite
            excedeu_saques = numero_saques >= self.limite_saques

            if excedeu_limite:
                print("ERROR!!! O valor excedeu o limite.")

            elif excedeu_saques:
                print("ERROR!!! Limite de saques excedido.")

            else:
                return super().sacar(valor)
            
            return False
        
        def __str__(self):
            return f"""\
                Agencia:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
            """


class Historico:
    def __init__(self):
        self.transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao._class_._name_,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractclassmethod
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

        @property
        def valor(self):
            return self._valor
        
        def registrar(self, conta):
            sucesso_transacao = conta.sacar(self.valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)


class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


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
    return input(textwrap.dedent(menu))

def filtrar_clientes(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("ERROR!!! Cliente nao possui conta.")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\nERROR!!! Cliente nao encontrado.")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def sacar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("ERROR!!! Cliente nao encontrado.")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("ERROR!!! Cliente nao encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n###EXTRATO###")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nao foram realizadas movimentacoes."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("#############")

def criar_cliente(clientes):
    cpf = input("Infrome seu cpf: ")
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print("ERROR!!! Ja existe cliente cadastrado com esse cpf.")
        return
    
    nome= input("Informe seu nome completo: ")
    nascimento = input("Informe sua data de nascimento: ")
    endereco = input("Informe seu endereco: ")

    cliente = PessoaFisica(nome=nome, nascimento=nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n### Cliente cadastrado com sucesso! ###")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not clientes:
        print("ERROR!!! Cliente nao encontrado, fluxo de criacao de conta encerrado.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("#" * 15)
        print(textwrap.dedent(str(conta)))

def main():

    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
             depositar(clientes)

        elif opcao == "s":
            sacar(clientes)
                
        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes) 
            
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nc":
            numero_conta = len(contas) + 1 #vai criar uma sequencia para os numeors das contas
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "q":
            break
            
        else:
            print("Opcao invalida. Tente novamente")


main()

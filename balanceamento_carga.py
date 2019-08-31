class BalanceamentoCargaLimiteException(Exception):
    """Raised when if ttask and umax are outside the allowed limit"""
    pass


class User:
    ttask = 0  # Número de ticks de uma tarefa

    def __init__(self, ):
        self.ttask_restantes = User.ttask

    def remover_tick(self):
        """Remove um tick (unidade básica de tempo da simulação), da 'ttask_restantes' do usuário, retorna os
         ticks restantes para terminar a tarefa"""
        self.ttask_restantes -= 1
        if self.ttask_restantes < 0:
            raise Exception("Um erro ocorreu, ttask_restantes nunca deveria ser"
                            " menor que 0! valor='%s'" % self.ttask_restantes)
        return self.ttask_restantes

    @staticmethod
    def verificar_limite_ttask():
        """Verifica se ttask esta dentro do limite permitido"""
        if User.ttask < 1 or User.ttask > 10:
            raise BalanceamentoCargaLimiteException('ttask tem que ser maior ou igual a 1 e menor ou igual a 10!')
        return 0


class Servidor:
    umax = 0  # Máximo de usuários simultaneamente.

    def __init__(self, usuarios):
        self.usuarios = usuarios

    @staticmethod
    def verificar_limite_umax():
        """Verifica se umax esta dentro do limite permitido"""
        if Servidor.umax < 1 or Servidor.umax > 10:
            raise BalanceamentoCargaLimiteException('umax tem que ser maior ou igual a 1 e menor ou igual a 10!')
        return 0

    def verificar_disponibilidade(self):
        """Verifica se o servidor tem disponibilidade de alocar um novo usuário,
        se tiver retorna True, se não tiver retorna False"""
        if len(self.usuarios) < Servidor.umax:
            return True
        else:
            return False

    def remover_tick_usuarios(self):
        """Remove um tick (unidade básica de tempo da simulação) da 'ttask_restantes' de todos os usuários do servidor,
         e remove os usuários inativos (que não tem mais ttask_restantes)"""
        self.usuarios[:] = [user for user in self.usuarios if user.remover_tick()]
        return self.usuarios


class BalanceamentoCarga:

    def __init__(self, reader, writer):
        self.reader = reader  # ler o arquivo de entrada 'input.txt'
        self.writer = writer  # Escrever no arquivo de saida 'output.txt'
        self.custo_servidor = 0  # Váriavel que guarda o custo total por utilização dos servidores
        self.quantidade_user = 0  # Quantidade de usuários ativos mo momento
        self.lista_entrada_tarefas_user = []  # Mantem a lista de eventos de entrada de novos usúarios
        self.servidores = []

    def alocar_novos_usuarios(self, qt_user):
        """Procura um servidor com disponibilidade, se não tiver adiciona mais um servidor e aloca o novo usuário"""
        for item in range(qt_user):
            alocado = False
            for servidor in self.servidores:
                if servidor.verificar_disponibilidade():
                    servidor.usuarios.append(User())
                    alocado = True
            if alocado is False:
                self.servidores.append(Servidor([User()]))

    def remover_tick_usuarios_servidores(self):
        """Chama a função que remove um tick (unidade básica de tempo da simulação) de cada usuário ativo do servidor
        e remove os servidores inativos (que já estão sem usuários)"""
        self.servidores[:] = [servidor for servidor in self.servidores if servidor.remover_tick_usuarios()]

    def ler_prox_tick(self):
        """Ler o proximo tick do arquivo de entrada e retorna seu valor, se não tiver mais entradas retorna False"""
        line = self.reader.readline()  # Ler o número de novos usuários para esse tick .
        if line:  # Se ainda existir uma entrada
            return int(line)  # Ler a entrada de quantos usuarios novos para esse tick
        else:
            return False

    def quantidade_user_ativos(self):
        """Retorna a quantidade de usuários ativos no momento em todos os servidores"""
        count = 0
        for servidor in self.servidores:
            count += len(servidor.usuarios)
        return count

    def escrever_saida(self):
        """Escreve uma linha de saida (Output), representado pelo número de usuários
         em cada servidor separados por vírgula"""
        saida = ''
        for i, servidor in enumerate(self.servidores):

            if i + 1 == len(self.servidores):
                saida += '%s\n' % len(servidor.usuarios)
            else:
                saida += '%s,' % len(servidor.usuarios)

        self.writer.write(saida)
        return saida

    def escrever_resultado_final(self):
        """Escreve as linhas finais do arquivo de saida"""
        self.writer.write(str(
            self.quantidade_user_ativos()) + '\n')  # Usuários ativos ao termino da execução das tarefas, que deve ser 0 nesse ponto
        self.writer.write(str(self.custo_servidor))  # Custo total por utilização dos servidores

    def executar_balanceamento(self):
        """Método da classe que (com o auxílio dos outros métodos), entra em loop lendo o arquivo input dado
        e escrevendo o resultado no arquivo de saída, ate não ter mais ticks para serem executados"""
        input_lido = False
        while self.servidores or not input_lido:
            qt_novos_user = self.ler_prox_tick()
            if qt_novos_user is False and input_lido is False:
                input_lido = True

            if qt_novos_user is not False:
                self.alocar_novos_usuarios(qt_novos_user)

            self.escrever_saida()
            self.custo_servidor += len(self.servidores)
            self.remover_tick_usuarios_servidores()

        self.escrever_resultado_final()


def main():
    """
    Input (Entrada):
        Deve ser um arquivo texto com o nome 'input.txt' no mesmo diretório do arquivo python que esta
        sendo executado ('balanceamento_carga.py')
        input.txt deve ser um arquivo onde:
        a primeira linha possui o valor de ttask ;
        a segunda linha possui o valor de umax ;
        as demais linhas contém o número de novos usuários para cada tick

    Limites:
        1 ≤ ttask ≤ 10
        1 ≤ umax ≤ 10

    Output (Saída):
        Um arquivo ('output.txt') onde cada linha contém uma lista de servidores disponíveis no final de cada tick,
    representado pelo número de usuários em cada servidor separados por vírgula e, ao final, o
    custo total por utilização dos servidores
    """
    try:
        with open('input.txt', 'r') as reader, open('output.txt', 'w') as writer:
            balanceamento_carga = BalanceamentoCarga(reader, writer)
            User.ttask = int(reader.readline())  # Ler e define ttask
            Servidor.umax = int(reader.readline())  # Ler e define umax
            # verificar valores ttask e umax lidos
            User.verificar_limite_ttask()
            Servidor.verificar_limite_umax()
            balanceamento_carga.executar_balanceamento()
    except Exception as e:
        print(e)
    return 0


main()

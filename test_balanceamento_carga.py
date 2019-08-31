import os
import unittest

from balanceamento_carga import BalanceamentoCarga, BalanceamentoCargaLimiteException, User, Servidor


class TestBalanceamentoCarga(unittest.TestCase):

    def setUp(self):
        writer_input = open('test_input.txt', 'w')
        writer_input.write('4\n')
        writer_input.write('2\n')
        writer_input.write('1\n')
        writer_input.write('3\n')
        writer_input.write('0\n')
        writer_input.write('1\n')
        writer_input.write('0\n')
        writer_input.write('1')
        writer_input.close()

        self.reader = open('test_input.txt', 'r')
        self.balanceamento_carga = BalanceamentoCarga(self.reader, open('test_output.txt', 'w'), )

        User.ttask = int(self.reader.readline())  # Ler e define ttask
        Servidor.umax = int(self.reader.readline())  # Ler e define umax

    def tearDown(self):
        self.balanceamento_carga.reader.close()
        self.balanceamento_carga.writer.close()
        os.remove('test_input.txt')
        os.remove('test_output.txt')

    # testar se um valor ttask válido é aceito pela função
    def test_verificar_limites_ttask(self):
        self.assertEqual(User.verificar_limite_ttask(), 0)

    # testar se um valor umax válido é aceito pela função
    def test_verificar_limites_umax(self):
        self.assertEqual(Servidor.verificar_limite_umax(), 0)

    # testar se para um valor menor que o permitido para ttask é lançada a exceção esperada
    def test_verificar_limites_inferiror_ttask(self):
        with self.assertRaises(BalanceamentoCargaLimiteException):
            User.ttask = 0
            User.verificar_limite_ttask()

    # testar se para um valor maior que o permitido para ttask é lançada a exceção esperada
    def test_verificar_limites_superior_ttask(self):
        with self.assertRaises(BalanceamentoCargaLimiteException):
            User.ttask = 11
            User.verificar_limite_ttask()

    # testar se para um valor menor que o permitido para umax é lançada a exceção esperada
    def test_verificar_limites_inferiror_umax(self):
        with self.assertRaises(BalanceamentoCargaLimiteException):
            Servidor.umax = 0
            Servidor.verificar_limite_umax()

    # testar se para um valor maior que o permitido para umax é lançada a exceção esperada
    def test_verificar_limites_superior(self):
        with self.assertRaises(BalanceamentoCargaLimiteException):
            Servidor.umax = 11
            Servidor.verificar_limite_umax()

    # testa o método de leitura do próximo tick
    def test_ler_prox_tick(self):
        tick = self.balanceamento_carga.ler_prox_tick()
        self.assertEqual(tick, 1)

    # testa o método que escreve a saída para o tick lido
    def test_escrever_saida(self):
        self.balanceamento_carga.alocar_novos_usuarios(1)
        self.assertEqual(self.balanceamento_carga.escrever_saida(), '1\n')

    """testa os métodos que verifica a disponibilidade do servidor, que aloca usuários e 
    que calcula os usuários ativos e custo do servidor"""

    def test_verificar_disponobilidade(self):
        self.balanceamento_carga.alocar_novos_usuarios(1)
        self.balanceamento_carga.custo_servidor = len(self.balanceamento_carga.servidores)
        self.assertEqual(self.balanceamento_carga.quantidade_user_ativos(), 1)
        self.assertEqual(self.balanceamento_carga.servidores[0].verificar_disponibilidade(), True)
        self.assertEqual(self.balanceamento_carga.custo_servidor, 1)
        self.balanceamento_carga.alocar_novos_usuarios(1)
        self.balanceamento_carga.custo_servidor = len(self.balanceamento_carga.servidores)
        self.assertEqual(self.balanceamento_carga.servidores[0].verificar_disponibilidade(), False)
        self.assertEqual(self.balanceamento_carga.quantidade_user_ativos(), 2)
        self.assertEqual(self.balanceamento_carga.custo_servidor, 1)
        self.balanceamento_carga.alocar_novos_usuarios(1)
        self.balanceamento_carga.custo_servidor = len(self.balanceamento_carga.servidores)
        self.assertEqual(self.balanceamento_carga.custo_servidor, 2)

    """Testar vários metodos utilizados para remover um tick, remover usuário e remover servidor:
         Da classe user: remove_tick()
         Da classe Servidor: remover_tick_usuarios()
         Da classe BalanceamentoCarga: remover_tick_usuarios_servidores()
     """

    def test_metodos_remover_decremento(self):
        self.balanceamento_carga.alocar_novos_usuarios(1)
        self.balanceamento_carga.remover_tick_usuarios_servidores()  # remover um tick
        self.assertEqual(self.balanceamento_carga.servidores[0].usuarios[0].ttask_restantes, 3)

        # finalizar ttask
        for i in range(User.ttask - 1):
            self.balanceamento_carga.remover_tick_usuarios_servidores()

        self.assertEqual(self.balanceamento_carga.quantidade_user_ativos(), 0)
        self.assertEqual(len(self.balanceamento_carga.servidores), 0)

    # testa a saída gerada, com o resultado esperado final
    def test_saida_gerada(self):
        self.balanceamento_carga.executar_balanceamento()

        self.assertEqual(self.balanceamento_carga.quantidade_user, 0)
        self.assertEqual(self.balanceamento_carga.custo_servidor, 15)

        self.balanceamento_carga.writer.close()
        self.balanceamento_carga.writer = open('test_output.txt', 'r')
        read_output = self.balanceamento_carga.writer.read()
        self.assertEqual(read_output, '1\n2,2\n2,2\n2,2,1\n1,2,1\n2\n2\n1\n1\n0\n15')


if __name__ == '__main__':
    unittest.main()

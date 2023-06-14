import unittest
from flow import Flow
from user import User


class TestFlow(unittest.TestCase):
    
    user = User('test', '12345')
    
    def test_start(self):
        
        flow = Flow(self.user)
        response = flow.generate_response("/start")
        self.assertEqual(response, """
        Bem vindo ao sistema E-SIC Bot... \nSelecione uma das opções abaixo:
    /novo_pedido - Para fazer um novo pedido
    /consultar_pedido - Para consultar um pedido
    """)
        
    
    def test_consultar_pedidos(self):
        
        user_com_pedido = User('test', '12345')
        flow = Flow(user_com_pedido)
        
        response = flow.criar_novo_pedido()
        response = flow.generate_response("/consultar_pedido")
        response_check = "Você possui" in response
        
        self.assertTrue(response_check)
        
        user_sem_pedido = User('test', '12345')
        flow = Flow(user_sem_pedido)
        response = flow.generate_response("/consultar_pedido")
        response_check = "Você não possui" in response
        
        self.assertTrue(response_check)
    
    
    
if __name__ == '__main__':
    unittest.main()
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
    
    
if __name__ == '__main__':
    unittest.main()
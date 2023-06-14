import unittest
from flow import Flow
from user import User
import template_message


class TestFlow(unittest.TestCase):
    
    
    def test_start(self):
        
        user = User('test', '12345')
        flow = Flow(user)
        response = flow.generate_response("/start")
        self.assertEqual(response, template_message.start())
        
        
    def test_novo_pedido(self):
        
        user = User('test', '12345')
        flow = Flow(user)
        
        response_1 = flow.generate_response("/novo_pedido")
        self.assertEqual(response_1, template_message.novo_pedido_cidade())
        
        response_2 = flow.generate_response("/rio_branco")
        self.assertEqual(response_2, template_message.novo_pedido_assunto())
        
        
        
    
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
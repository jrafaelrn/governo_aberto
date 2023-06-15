import unittest
from user import User
import template_message


class TestFlow(unittest.TestCase):
    
    
    def test_start(self):       
        user = User('test', '12345')
        response = user.response("/start")
        self.assertEqual(response, template_message.start())
        
        
    def test_novo_pedido(self):
        
        user = User('test', '12345')
        
        response_1 = user.response("/novo_pedido")
        self.assertEqual(response_1, template_message.novo_pedido_cidade())
        
        response_2 = user.response("/rio_branco")
        self.assertEqual(response_2, template_message.novo_pedido_assunto())
        
        
        
    
    def test_consultar_pedidos(self):
        
        user_com_pedido = User('test', '12345')
        
        response = user_com_pedido.criar_novo_pedido()
        response = user_com_pedido.response("/consultar_pedido")
        response_check = "Você possui" in response
        
        self.assertTrue(response_check)
        
        user_sem_pedido = User('test', '12345')
        response = user_sem_pedido.response("/consultar_pedido")
        response_check = "Você não possui" in response
        
        self.assertTrue(response_check)
    
    
    
if __name__ == '__main__':
    unittest.main()
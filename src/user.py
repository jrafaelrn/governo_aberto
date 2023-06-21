from pedido import Pedido
from datetime import datetime as dt
from flow import Flow

class User:
    
    def __init__(self, name: str, chat_id: str):
        self.name = name
        self.chat_id = chat_id
        self.flow = Flow(self)
        self.pedidos = []
        self.pedido_atual = None
        self.last_query_id = None
        self.last_type_message = None
        self.last_callback_message = None
        
    
    def response(self, message):
        return self.flow.generate_response(message)
    
    
    def get_qtd_pedidos(self):
        return len(self.pedidos)
    
    
    def get_qtd_pedidos_abertos(self):
        return self.get_qtd_pedidos() - self.get_qtd_pedidos_status("conclusao")
            
    
    def get_qtd_pedidos_status(self, status: str):
        total = 0
        for pedido in self.pedidos:
            if pedido.last_notification == status:
                total += 1
        return total
    
    
    def criar_novo_pedido(self):
        
        pedido = Pedido()
        id = str(len(self.pedidos) + 1)
        pedido.id = id
        
        data_criacao_str = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        pedido.data_criacao = data_criacao_str
        
        self.pedido_atual = pedido
        
    
    def gravar_pedido(self, pedido: Pedido):
        self.pedidos.append(pedido)
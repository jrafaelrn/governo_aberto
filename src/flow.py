from user import User

class Flow:
    
    
    def __init__(self, user: User):
        self.user = user
    
    
    
    def generate_response(self, message):
        
        flow_status = self.user.get_flow_status()
        
        if message == "/start":
            return self.start()
        
        if message == "/novo_pedido":
            return self.novo_pedido(message)
        
        if message == "/consultar_pedido":
            return self.consultar_pedidos()
        
        
        if not flow_status == None:
            
            if "novo_pedido" in flow_status:
                return self.novo_pedido(message)
    
        return f'Mensagem recebida: {message}'
    
    
    
    def start(self) -> str:
        self.user.set_flow_status("start")
        return """
        Bem vindo ao sistema E-SIC Bot... \nSelecione uma das opções abaixo:
    /novo_pedido - Para fazer um novo pedido
    /consultar_pedido - Para consultar um pedido
    """
    
    
    
    def novo_pedido(self, message) -> str:
        
        flow_status = self.user.get_flow_status()
        
        if message == "/novo_pedido":
            self.user.set_flow_status("novo_pedido_cidade")
            return "Qual cidade?\n/rio_branco - Acre\n/florianopolis - Santa Catarina"
           
    
    
    
    def consultar_pedidos(self):
        
        self.user.set_flow_status("consultar_pedidos")
        qtd_pedidos = self.user.get_qtd_pedidos()
        
        if qtd_pedidos == 0:
            return "Você não possui pedidos!\n/novo_pedido - Para fazer um novo pedido"
        
        return f"Você possui {qtd_pedidos} pedidos"
    
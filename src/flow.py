from user import User

class Flow:
    
    
    def __init__(self, user: User):
        self.user = user
    
    
    
    def generate_response(self, message):
        
        if message == "/start":
            return self.start()
        
        if message == "/novo_pedido":
            return self.novo_pedido(message)
        
        if message == "/consultar_pedido":
            return self.consultar_pedidos()
        
        
        if self.user.flow_status:
            
            if "novo_pedido" in self.user.flow_status:
                return self.novo_pedido(message)
            
            if "consultar_pedidos" in self.user.flow_status:
                return self.consultar_pedidos()
    
        return f'Houve um erro ao processar sua mensagem: {message}'
    
    
    
    def start(self) -> str:
        self.user.flow_status = "start"
        return """
        Bem vindo ao sistema E-SIC Bot... \nSelecione uma das opções abaixo:
    /novo_pedido - Para fazer um novo pedido
    /consultar_pedido - Para consultar um pedido
    """
    
    
    ######################################
    #             NOVO PEDIDO            #
    ######################################
    
    def novo_pedido(self, message) -> str:
        
        if message == "/novo_pedido":
            self.user.flow_status = "novo_pedido_cidade"
            return "Qual cidade?\n/rio_branco - Acre\n/florianopolis - Santa Catarina"
        
        if self.user.flow_status == "novo_pedido_cidade":
            self.user.flow_status = "novo_pedido_assunto"
            return """
            Qual o assunto?"""
        
        
           
    
    def criar_novo_pedido(self):
         self.user.criar_novo_pedido()   
           
    
    ######################################
    #           CONSULTAR PEDIDOS        #
    ######################################
    
    def consultar_pedidos(self):
        
        self.user.flow_status = "consultar_pedidos"
        qtd_pedidos = self.user.get_qtd_pedidos()
        
        if qtd_pedidos == 0:
            return "Você não possui pedidos!\n/novo_pedido - Para fazer um novo pedido"
        
        return f"Você possui {qtd_pedidos} pedidos"
    
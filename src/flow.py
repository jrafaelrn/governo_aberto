import template_message

class Flow:
    
    
    def __init__(self, user):
        self.user = user
        self.flow_status = ""
    
    
    
    def generate_response(self, message):
        
        if message == "/start":
            return self.start()
        
        if message == "/novo_pedido" or "novo_pedido" in self.flow_status:
            return self.novo_pedido(message)
        
        if message == "/consultar_pedidos":
            return self.consultar_pedidos()
    
        return template_message.opcao_invalida()
    
    
    
    def start(self) -> str:
        self.flow_status = "start"
        return template_message.start()
    
    
    ######################################
    #             NOVO PEDIDO            #
    ######################################
    
    def novo_pedido(self, message) -> str:
        
        if message == "/novo_pedido":
            self.user.criar_novo_pedido()
            self.flow_status = "novo_pedido_cidade"
            return template_message.novo_pedido_cidade()
        
        if self.flow_status == "novo_pedido_cidade":
            self.flow_status = "novo_pedido_assunto"
            self.user.pedido_atual.city = message
            return template_message.novo_pedido_assunto()
        
        if self.flow_status == "novo_pedido_assunto":
            self.flow_status = "novo_pedido_descricao"
            self.user.pedido_atual.subject = message
            return template_message.novo_pedido_descricao()
        
        if self.flow_status == "novo_pedido_descricao":
            self.flow_status = ""
            self.user.pedido_atual.description = message
            self.user.pedido_atual.last_status = "Em análise..."
            self.user.gravar_pedido(self.user.pedido_atual)
            return template_message.novo_pedido_conclusao(self.user.pedido_atual.city, self.user.pedido_atual.subject, self.user.pedido_atual.description)
        
        
           
    
    def criar_novo_pedido(self):
        self.user.criar_novo_pedido()
           
    
    ######################################
    #           CONSULTAR PEDIDOS        #
    ######################################
    
    def consultar_pedidos(self):
        
        self.flow_status = "consultar_pedidos"
        return template_message.retornar_pedidos(self.user)
    
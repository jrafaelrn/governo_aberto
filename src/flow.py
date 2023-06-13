from user import User

class Flow:
    
    def generate_response(self, message: str, user: User):
        flow_status = user.get_flow_status()
        resp = self.get_resp(message, flow_status)
        return resp
    
    
    def get_resp(self, message: str, status_flow: str):
        
        if message == "/start":
            return self.start()
        
        return f'Mensagem recebida: {message}'
    
    
    def start(self) -> str:
        return "Bem vindo ao sistema E-SIC Bot... "
    
    
    
from abc import ABC, abstractmethod
from user import User
from flow import Flow
from datetime import datetime as dt
import time

class Gateway(ABC):
    
    def __init__(self):
        self.WAIT_TIME = 1
        
        
    # API KEY    
    def set_api_key(self, api_key):
        self.api_key = api_key
        
    def get_api_key(self):
        return self.api_key
    
    
    # Loop para receber as mensagens, processar e enviar a resposta
    def start(self):
        
        self.configure_bot()
        while True:
            
            receive, user = self.receive()
            
            if receive:
                response = Flow().generate_response(receive, user)
                self.send(response, user)
            
            time.sleep(self.WAIT_TIME)
            
            # Envia notificações a cada minuto
            second = dt.now().second
            if second <= 10:
                self.notifications()
                time.sleep(10)
                
    
    # MÉTODOS PARA IMPLEMENTAR
    @abstractmethod
    def configure_bot(self):
        pass
    
    @abstractmethod
    def receive(self):
        pass
    
    @abstractmethod
    def send(self, message, user):
        pass
    
    @abstractmethod
    def notifications(self):
        pass
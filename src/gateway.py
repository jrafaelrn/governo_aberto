from abc import ABC, abstractmethod
from user import User
from datetime import datetime as dt
import time

class Gateway(ABC):
    
    def __init__(self):
        self.WAIT_TIME = 1
        
    api_key = None
    
    
    
    # Loop para receber as mensagens, processar e enviar a resposta
    def start(self):
        
        self.configure_bot()
        
        while True:
            
            self.receive()
            self.reply()
            
            time.sleep(self.WAIT_TIME)
            
            # Envia notificações a cada minuto
            second = dt.now().second
            if second <= 5:
                self.notifications()
                time.sleep(5)
            
    
    # MÉTODOS PARA IMPLEMENTAR
    @abstractmethod
    def configure_bot(self):
        pass
    
    @abstractmethod
    def receive(self):
        pass
    
    @abstractmethod
    def reply(self):
        pass
    
    @abstractmethod
    def send_text(self, message, user):
        pass
    
    @abstractmethod
    def send_options(self, list_options, user):
        pass
    
    @abstractmethod
    def notifications(self):
        pass
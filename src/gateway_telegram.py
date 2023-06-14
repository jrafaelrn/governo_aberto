from gateway import Gateway
from user import User
import requests

class Gateway_Telegram(Gateway):
    
    def __init__(self):
        super().__init__()
        self.chats_id = {}
        self.update_id = 0
        
        
    def configure_bot(self):
        url_base = 'https://api.telegram.org/bot'
        self.url_base = f'{url_base}{super().get_api_key()}/'
        print('Starting Telegram gateway...')
        print(f'URL_BASE: {self.url_base}')
        
        
    
    def receive(self):
        
        print('Receiving message from Telegram...')
        link_req = f'{self.url_base}getUpdates?offset={self.update_id + 1}'
        response = requests.get(link_req)
        
        print(f'Response: {response}')
        
        # Verifica se a resposta está vazia
        if response.content == b'{"ok":true,"result":[]}':     
            return None, None  
        
        
        chat_id = response.json()['result'][-1]['message']['chat']['id']
        message = response.json()['result'][-1]['message']['text']
        user_name = response.json()['result'][-1]['message']['from']['username']
        self.update_id = response.json()['result'][-1]['update_id']
        
        # Procura o usuário na lista
        user = None
        for chat in self.chats_id:
            if chat == chat_id:
                user = chat
                break
        
        # Se não encontrar, cria um novo usuário
        if user is None:
            user = User(user_name, chat_id)
            self.chats_id[user_name] = user
        
        return message, user
        
    
    def send(self, message, user: User):
        
        print(f'Sending message to {user.name}... {message}')
        link = f'{self.url_base}sendMessage?chat_id={user.chat_id}&text={message}'
        
        resp = requests.get(link)
        
        if resp.status_code == 200:
            print('Message sent successfully! ;)')
        else:
            print(f'Error sending message! - Status Code: {resp.status_code} - Message: {resp.text}')
        
        
    
    def notification(self, message):
        print(f'Sending notification to Telegram... {message}')
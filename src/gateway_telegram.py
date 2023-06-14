from gateway import Gateway
from user import User
import requests
import json

class Gateway_Telegram(Gateway):
    
    def __init__(self):
        super().__init__()
        self.chats_id = {}
        self.update_id = 0
        
        
    def configure_bot(self):
        url_base = 'https://api.telegram.org/bot'
        self.url_base = f'{url_base}{self.api_key}/'
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
        
        # Obtém os dados do usuário
        chat_id = response.json()['result'][-1]['message']['chat']['id']
        message = response.json()['result'][-1]['message']['text']
        
        # Caso o usuário não tenha username, cria um username com base no nome e no chat_id
        try:
            user_name = response.json()['result'][-1]['message']['from']['username']
        except:
            user_name = f"{response.json()['result'][-1]['message']['from']['first_name']}-{chat_id}"
        
        self.update_id = response.json()['result'][-1]['update_id']
        
        # Procura o usuário na lista
        user = None
        for chat in self.chats_id:
            if chat == user_name:
                user = self.chats_id[chat]
                print(f'User {user_name} found!')
                break
        
        # Se não encontrar, cria um novo usuário
        if user is None:
            user = User(user_name, chat_id)
            self.chats_id[user_name] = user
            print(f'User {user_name} created!')
        
        return message, user
        
    
    
    def send_text(self, message, user: User):
        
        print(f'Sending message to {user.name}... {message}')
        link = f'{self.url_base}sendMessage?chat_id={user.chat_id}&text={message}'
        
        resp = requests.get(link)
        
        if resp.status_code == 200:
            print('Message sent successfully! ;)')
        else:
            print(f'\tError sending message! - Status Code: {resp.status_code} - Message: {resp.text}')
        
    
    
    def send_options(self, list_options, user):
        
        text, options = list_options
        self.send_text(text, user)
        
        headers = {'Content-Type': 'application/json'}
        data = {}        
        keyboards = []
        keyboard = []
        counter = 0

        for option in options:
            
            keyboard_button_json = []
            keyboard_button_json.append({
                "text": option, 
                "callback_data" : counter
            })
            keyboard.append(keyboard_button_json)
            counter += 1

        keyboards.append(keyboard)
        data["inline_keyboard"] = keyboard

        print(f'<<--- Sending inline options: \n{data} - \nto chat: {user.chat_id}')
        data = json.dumps(data)

        link_resp = f'{self.url_base}sendMessage?chat_id={user.chat_id}&text=Escolha uma opção:&reply_markup={data}'
        response = requests.get(link_resp, headers=headers, json=data)
        print(f'\<<--- Response: {response.status_code}')
        
    
    
    def keyboard_remove(self, user: User):
    
        headers = {'Content-Type': 'application/json'}
        method_url = 'sendMessage'
        payload = {"remove_keyboard" : True}
        data = json.dumps(payload)

        link_resp = f'{self.url_base}{method_url}?chat_id={user.chat_id}&text=...&reply_markup={data}'
        resp = requests.get(link_resp, headers = headers, json = data)

        print(f'XXX - Remove Keyboard - Response: {resp.status_code} - {resp.text}')
    
    
    
    def notifications(self):
        
        print(f'Sending notification to Telegram... {len(self.chats_id)}')
        
        for user in self.chats_id.values():
            self.send('Atualização do seu pedido: ', user)
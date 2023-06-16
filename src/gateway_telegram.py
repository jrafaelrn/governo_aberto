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
        
        
    
    # Recebe as mensagens do Telegram e armazena em um vetor 
    def receive(self):
        
        print('Waiting message from Telegram...')
        self.mensagens_recebidas = []
        
        link_req = f'{self.url_base}getUpdates?offset={self.update_id + 1}'
        response = requests.get(link_req)
        response_json = response.json()
                
        # Verifica se a resposta está vazia
        if response.content == b'{"ok":true,"result":[]}':     
            return None, None  
        
        print(f'\nGET from Telegram: {response_json}')
        
        self.update_id = self.get_last_update_id(response_json['result'][-1])
        self.mensagens_recebidas = response_json['result']       
    
    
    
    ##############################
    #          REPLY             #
    ##############################
    
    def reply(self):
        
        for message in self.mensagens_recebidas:
            
            print(f'\nProcessing message: {message}')
            message_type = self.get_message_type(message)
            
            user = self.get_user_data(message, message_type)
            user.last_type_message = message_type
            
            text_from_user = self.get_message(message, user)
            text_to_reply = user.response(text_from_user)
            
            if type(text_to_reply) == str:
                self.send_text(text_to_reply, user)
                
            if type(text_to_reply) == dict:
                self.send_options(text_to_reply, user)
                
            self.mensagens_recebidas.remove(message)
            
    
    def get_message_type(self, response):
        try:
            message_type = response['message']['text']
            message_type = 'text'
        except:
            message_type = 'callback'
        
        return message_type
    
    
    # Obtém os dados do usuário
    def get_user_data(self, response, message_type: str):
        chat_id = self.get_chat_id(response)
        user_name = self.get_user_name(response, chat_id, message_type)
        user = self.get_user(user_name, chat_id)
        return user
    
    
    def get_chat_id(self, response):
        try:
            chat_id = response['message']['chat']['id']
        except:
            chat_id = response['callback_query']['message']['chat']['id']
        return chat_id
    
    
    def get_message(self, response, user: User):
        try:
            try:    
                resp = response['message']['text']
            except:
                resp = response['callback_query']['data']
                resp = user.last_callback_message[int(resp)]
        except:
            resp = 'Erro ao processar sua mensagem'
        
        return resp
    
    
    # Caso o usuário não tenha username, cria um username com base no nome e no chat_id
    def get_user_name(self, response, chat_id, message_type: str):
        user_name = None
        try:
            if message_type == 'text':
                user_name = response['message']['from']['username']
            else:
                user_name = response['callback_query']['from']['username']
        except:
            if message_type == 'text':
                user_name = f"{response['message']['from']['first_name']}-{chat_id}"
            else:
                user_name = f"{response['callback_query']['from']['first_name']}-{chat_id}"
        
        return user_name
    
    
    def get_last_update_id(self, response):
        return response['update_id']
    
    
    def get_user(self, user_name, chat_id):
        # Procura o usuário na lista
        user = None
        for chat in self.chats_id:
            if chat == user_name:
                user = self.chats_id[chat]
                print(f'User {user_name} found!')
                return user
        
        # Se não encontrar, cria um novo usuário
        user = User(user_name, chat_id)
        self.chats_id[user_name] = user
        print(f'User {user_name} created!')
        return user
    
    
    ##############################
    #       SEND MESSAGES        #
    ##############################
    
    def send_text(self, message, user: User):
        
        print(f'Sending message to {user.name}... {message}')
        link = f'{self.url_base}sendMessage?chat_id={user.chat_id}&text={message}'
        
        resp = requests.get(link)
        
        if resp.status_code == 200:
            print('Message sent successfully! ;)')
        else:
            print(f'\tError sending message! - Status Code: {resp.status_code} - Message: {resp.text}')
        
    
    
    def send_options(self, list_options: dict, user: User):
        
        text = list(list_options.keys())[0]
        options = list(list_options.values()).pop()
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
            
        user.last_callback_message = options

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
            self.send_text('Atualização do seu pedido: ', user)
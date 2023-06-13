
class User:
    
    def __init__(self, name: str, chat_id: str):
        self.name = name
        self.chat_id = chat_id
        self.flow_status = None
        
    
    def get_flow_status(self):
        return self.flow_status
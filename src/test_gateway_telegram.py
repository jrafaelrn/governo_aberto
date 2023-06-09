import unittest
import json
from gateway_telegram import Gateway_Telegram
from user import User


class TestGatewayTelegram(unittest.TestCase):
    
    response = {'ok': True, 'result': [{'update_id': 123456, 'message': {'message_id': 273, 'from': {'id': 678910, 'is_bot': False, 'first_name': 'Test First Name', 'last_name': 'Test Last Name', 'username': 'abcde', 'language_code': 'en'}, 'chat': {'id': 11223344, 'first_name': 'Test First Name', 'last_name': 'Test Last Name', 'username': 'abcde', 'type': 'private'}, 'date': 1686860581, 'text': 'oi'}}]}

    gateway = Gateway_Telegram()
    
    
    def test_get_chat_id(self):
        self.assertEqual(self.gateway.get_chat_id(self.response['result'][-1]), 11223344)
        
    def test_get_message(self):
        user = User('abcde', 11223344)
        message = self.gateway.get_message(self.response['result'][-1], user)
        self.assertEqual(message, 'oi')
        
    def test_get_user_name(self):
        user_name = self.gateway.get_user_name(self.response['result'][-1], 11223344, 'text')
        self.assertEqual(user_name, 'abcde')
from gateway import Gateway
from gateway_telegram import Gateway_Telegram
from user import User
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    
    print('Starting bot...')
    bots = set()
    
    # Criando bots
    telegram = Gateway_Telegram()
    api_key = os.getenv('TELEGRAM_API_KEY')
    telegram.api_key = api_key
    
    # Add bots
    bots.add(telegram)
    
    # Multi-threading ??
    for bot in bots:
        bot.start()
    
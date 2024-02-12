import telebot
import dotenv
import os
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

chat_id = os.getenv('CHAT_ID')

#send message to test chat_id
bot.send_message(chat_id, "Hello from your bot")

bot.polling()

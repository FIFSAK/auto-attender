import os
import telebot
from dotenv import load_dotenv
from kafkaClient import kafka_read

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["report"])
def status_command(message):
    response = "CURRENT STATUS:\n"
    messages = kafka_read()
    if messages[-1] == "healthy":
        response += "healthy"
    else:
        response += "unhealthy since " + messages[-1]["timestamp"]

    response += "\n\nHISTORY:\n"

    for msg in messages:
        response += f"{msg['timestamp']}: {msg['message']}\n"

    bot.send_message(message.chat.id, response)


def main():
    print("Bot started")
    bot.infinity_polling()


if __name__ == "__main__":
    main()

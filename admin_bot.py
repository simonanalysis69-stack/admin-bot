import telebot, os

TOKEN=os.getenv("TOKEN")
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id,"Admin Bot Working ✅")

bot.infinity_polling()


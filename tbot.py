
"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Source: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py
"""
import os
import logging

import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

PORT = int(os.environ.get('PORT', 5000))
TELEGRAM_API_TOKEN = os.environ['TELEGRAM_API_TOKEN']

model_id = "text-davinci-003"
logname = "bot.log"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def help(update, context):
    """Send a message when the command /help is issued."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Oh I need help also!")

async def echo(update, context):
    """Echo the user message."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(telegram.ext.filters.TEXT, echo))

    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        secret_token='ASecretTokenIHaveChangedByNow',
        key='private.key',
        cert='cert.pem',
        webhook_url="https://chat-gpt-telegeram-bridge.herokuapp.com/"
    )

    # webhook broken setup
    # application.updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TELEGRAM_API_TOKEN)
    # application.bot.setWebhook('https://chat-gpt-telegeram-bridge.herokuapp.com/' + TELEGRAM_API_TOKEN)

if __name__ == '__main__':
    main()

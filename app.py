import logging
import os
import openai

from log_utils import log_user, log_error

openai.api_key = os.getenv("OPENAI_API_KEY")

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

model_id = "text-davinci-003"
logname = "bot.log"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update)
    default_message = "Hello! I will try to serve you my best."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=default_message)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.message.text
    log_user(update)
    logging.info("User requested: {}".format(update.message.text))

    response = openai.Completion.create(
      engine=model_id,
      prompt=request,
      temperature=0.9,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
    )

    logging.info("Bot responded: {}".format(response["choices"][0]["text"]))
    logging.info("Response: {}".format(response))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response["choices"][0]["text"])


if __name__ == '__main__':
    telegram_api_token = os.environ['TELEGRAM_API_TOKEN']
    application = ApplicationBuilder().token(telegram_api_token).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
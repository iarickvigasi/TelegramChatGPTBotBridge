"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Source: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py
"""
import logging
import os
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from firebase_bridge import get_user, create_user, get_conversation_doc, new_conversation_doc, get_or_create_user, \
    get_or_create_conversation_doc, add_user_message_to_conversation, add_bot_message_to_conversation, \
    get_messages_from_conversation

from log_utils import log_user
from logger import logger
from openai_bridge import predict_default, conversation_mode_prompt

PORT = int(os.environ.get('PORT', 5000))
TELEGRAM_API_TOKEN = os.environ['TELEGRAM_API_TOKEN']

model_id = "text-davinci-003"


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update)

    user = get_or_create_user(update.message.from_user.id, update.message.from_user.first_name)
    user_name = update.message.from_user.first_name

    start_message = "Hello {}!\n" \
                    "My name is Arinoy which stands for Artificial Intelligence of Yaroslav.\n" \
                    "I will try to serve you to my best!".format(user_name)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)


async def help(update, context):
    """Send a message when the command /help is issued."""
    log_user(update)

    help_message = "Oh I need help also! Either contact my creator @ArickVigas, or just wait for me to get smarter."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)


def convert_messages_to_text(messages):
    text = ""

    for message in messages:
        text += message["type"] + ": " + message["message"] + "\n"

    return text


async def get_conversation_summary(conversation):
    messages = conversation.get("messages")
    print(messages)
    text = convert_messages_to_text(messages)

    prompt = "This is a full conversation with an AI. AI is bot, and user is user. Read the following text, " \
             "and get the most important summary of the conversation to continue the dialogue. Max is 1000 words." \
             "Conversation: " + text + "\n" + "Summary: "

    summary = await predict_default(prompt, temperature=0.5, max_tokens=2000)

    summary = summary["choices"][0]["text"]
    print(summary)
    return summary


async def conversation_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update)

    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    user_message = update.message.text

    conversation = get_or_create_conversation_doc(user_message, user_id)
    # conversation_summary = await get_conversation_summary(conversation)
    # print(conversation_summary)
    messages = convert_messages_to_text(conversation.get("messages"))

    add_user_message_to_conversation(user_message, user_id)

    print("User {} ({}) sent: {}".format(user_name, user_id, user_message))

    full_prompt = conversation_mode_prompt + "\n" + "Full conversation: " + messages + \
                  "\n[" + user_name + "]: " + user_message + ". \n" + "[bot]: "

    response = await predict_default(full_prompt, temperature=0.8, max_tokens=512)

    selected_response = response["choices"][0]["text"]

    add_bot_message_to_conversation(selected_response, user_id)

    logging.info("Bot responded: {}".format(response["choices"][0]["text"]))
    logging.info("Response: {}".format(response))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response["choices"][0]["text"])


async def echo(update, context):
    """Echo the user message."""
    prompt = update.message.text
    prediction = await predict_default(prompt)
    first_prediction = prediction["choices"][0]["text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=first_prediction)


async def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    application.add_handler(MessageHandler(telegram.ext.filters.TEXT, conversation_mode))

    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    # if port is not specified run in local mode
    if PORT == 5000:
        application.run_polling()
    else:
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            secret_token='ASecretTokenIHaveChangedByNow',
            # key='private.key',
            # cert='cert.pem',
            webhook_url="https://chat-gpt-telegeram-bridge.herokuapp.com/"
        )


if __name__ == '__main__':
    main()

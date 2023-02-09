import logging

def log_user(update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    user_message = update.message.text
    logging.info("User {} ({}) started the conversation with the message: {}".format(user_name, user_id, user_message))


def log_error(update, context):
    """Log Errors caused by Updates."""
    logging.error('Update "%s" caused error "%s"', update, context.error)
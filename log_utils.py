import logging

def log_user(update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    logging.info("User {} ({}) started the conversation".format(user_name, user_id))


def log_error(update, context):
    """Log Errors caused by Updates."""
    logging.error('Update "%s" caused error "%s"', update, context.error)
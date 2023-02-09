import itertools
import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from logger import logger

certificate = json.loads(os.getenv("FIREBASE_CERTIFICATE"))
cred = credentials.Certificate(certificate)
app = firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user(user_id):
    doc_ref = db.collection(u'users').document(u'{}'.format(user_id))
    doc = doc_ref.get()
    logger.info("Retrieved user: {}".format(doc))

    if doc.exists:
        return doc
    else:
        return None


def create_user(user_id, user_name):
    doc_ref = db.collection(u'users').document(u'{}'.format(user_id))
    doc_ref.set({
        u'user_id': user_id,
        u'user_name': user_name,
        u'created_timestamp': firestore.SERVER_TIMESTAMP,
    })
    return doc_ref


def get_or_create_user(user_id, user_name):
    user = get_user(user_id)
    logger.info("Retrieved user: {}".format(user))
    if user is None:
        logger.info("No such user, creating new user: {}".format(user_id))
        user = create_user(user_id, user_name)
    return user


def new_conversation_doc(message, user_id):
    doc_ref = db.collection(u'conversations').document(u'{}'.format(user_id))
    doc_ref.set({
        u'user_id': user_id,
        u'init_message': message,
        u'created_timestamp': firestore.SERVER_TIMESTAMP,
        u'messages': [],
    })
    return doc_ref


def get_conversation_doc(user_id):
    conversation_doc_ref = db.collection(u'conversations').document(u'{}'.format(user_id))
    conversation_doc = conversation_doc_ref.get()
    logger.info("Retrieved conversation: {}".format(conversation_doc))

    if conversation_doc.exists:
        return conversation_doc
    else:
        return None


def get_or_create_conversation_doc(message, user_id):
    conversation_doc = get_conversation_doc(user_id)
    if conversation_doc is None:
        logger.info("No such conversation for user {}, creating new conversation".format(user_id))
        conversation_doc = new_conversation_doc(message, user_id)
    return conversation_doc


def add_user_message_to_conversation(message, user_id):
    conversation_doc_ref = db.collection(u'conversations').document(u'{}'.format(user_id))

    message_data = {
        u'message': message,
        u'user_id': user_id,
        u'type': 'user'
    }

    conversation_doc_ref.update({
        u'messages': firestore.ArrayUnion([message_data])
    })

    return conversation_doc_ref

def add_bot_message_to_conversation(message, user_id):
    conversation_doc_ref = db.collection(u'conversations').document(u'{}'.format(user_id))

    message_data = {
        u'message': message,
        u'user_id': user_id,
        u'type': 'bot'
    }

    conversation_doc_ref.update({
        u'messages': firestore.ArrayUnion([message_data])
    })

    return conversation_doc_ref


def get_messages_from_conversation(user_id):
    conversation_doc = get_conversation_doc(user_id)
    if conversation_doc is None:
        return None
    else:
        return conversation_doc.to_dict()['messages']

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)

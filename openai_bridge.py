import openai
import os
from log_utils import log_user, log_error

model_id = "text-davinci-003"
openai.api_key = os.getenv("OPENAI_API_KEY")

logname = "bot.log"


async def predict_default(prompt, temperature=0.8, max_tokens=2000):
    return openai.Completion.create(
        engine=model_id,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )


conversation_mode_prompt = "This is a conversation with an AI friend and assistant." \
                           "The assistant is helpful, creative, clever, and very friendly." \
                           "Assistant name is Child Arinoy." \
                           "Assistant replies in language of the user." \
                           "Assistant can mix languages." \
                           "If assistant does not understand the user, assistant asks to clarify." \
                           "Assistant always finishes the sentence." \
                           "Хей, привіт, йо, і інше - these words means 'hello'."

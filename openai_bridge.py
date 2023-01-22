import openai
import os
from log_utils import log_user, log_error

model_id = "text-davinci-003"
openai.api_key = os.getenv("OPENAI_API_KEY")

logname = "bot.log"


async def predict_default(prompt, tempature=0.9, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
    prediction = openai.Completion.create(
        engine=model_id,
        prompt=prompt,
        temperature=tempature,
        max_tokens=max_tokens,
        top_p= top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return prediction



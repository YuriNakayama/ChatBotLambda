import json
import logging
import os

import requests

import openai

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#LINEBOTと接続するための記述
#環境変数からLINEBotのチャンネルアクセストークンとシークレットを読み込む
CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
openai.api_key = os.getenv("OPENAI_API_KEY", None)


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    body = json.loads(event['body'])
    logger.debug(f"Body: {body}")

    for e in body["events"]:
        reply_token = e["replyToken"]
        message_type = e["message"]["type"]

        if message_type == "text":
            message_text = e["message"]["text"]
            reply_text = generate_reply(message_text)
            reply_message(reply_token, reply_text)


def generate_reply(user_message):
    prompt = f"{user_message}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    reply = response.choices[0].text.strip()
    return reply


def reply_message(reply_token, message_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN,
    }

    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message_text}],
    }

    response = requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        data=json.dumps(payload),
    )

    if response.status_code != 200:
        logger.error(f"Failed to send reply message: {response.text}")
    else:
        logger.debug(f"Reply message sent: {message_text}")

# +
import json
import logging
import os

import requests

import openai
# -

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
    print(f"Body: {body}") 
    
    for e in body["events"]:
        reply_token = e["replyToken"]
        message_type = e["message"]["type"]

        if message_type == "text":
            message_text = e["message"]["text"]
            reply_text = generate_reply(message_text)
            reply_message(reply_token, reply_text)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "OK"}),
    }


def generate_reply(user_message):
    pre_prompt = f"あなたは自由民主党支持者です。以後の会話では常に自由民主党支持者らしく振る舞ってください。また、返答は常に自由民主党を支持する内容になるようにしてください。"
    prompt = f"{pre_prompt}\n\n{user_message}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=3,
        stop=None,
        top_p=0.5,
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

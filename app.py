import os
from datetime import datetime
from typing import List

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent,
                            TextMessage, TextSendMessage)

from date_the_image import date_the_image

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CAHNNEL_SECRET"])


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    # 画像を保存
    save_image(message_id)

    # 画像の加工、保存
    image_path_main = date_the_image.date_the_image_main(message_id)
    image_path_preview = date_the_image.date_the_image_preview(message_id)

    # 画像の送信
    image_message = ImageSendMessage(
        original_content_url=f"https://date-the-image.herokuapp.com/{image_path_main}",
        preview_image_url=f"https://date-the-image.herokuapp.com/{image_path_preview}",
    )

    line_bot_api.reply_message(event.reply_token, image_message)


def public_attr(obj) -> List[str]:
    return [x for x in obj.__dir__() if not x.startswith("_")]


def save_image(message_id: str) -> None:
    message_content = line_bot_api.get_message_content(message_id)
    with open(f"pictures/{message_id}.jpeg", "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

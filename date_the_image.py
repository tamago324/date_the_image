from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


def date_the_image(src: str, desc: str, size=800) -> None:
    """日付を付けて、保存する

    :params src:
        読み込む画像のパス
    :params desc:
        保存先のパス
    :params size:
        変換後の画像のサイズ
    """
    # 開く
    im = Image.open(src)

    # 800 x Height の比率にする
    proportion = size / im.width
    im_resized = im.resize((int(im.width * proportion), int(im.height * proportion)))

    draw = ImageDraw.Draw(im_resized)

    font = ImageFont.truetype("./fonts/Harlow Solid Regular.ttf", 60)
    text = datetime.now().strftime("%Y/%m/%d")

    # 図形を描画
    x = 10
    y = 10
    margin = 5
    text_width = draw.textsize(text, font=font)[0] + margin
    text_height = draw.textsize(text, font=font)[1] + margin
    draw.rectangle(
        (x - margin, y - margin, x + text_width, y + text_height), fill=(255, 255, 255)
    )

    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # 保存
    im_resized.save(desc)

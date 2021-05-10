from Wylie import ubot
from Wylie.events import Wbot
import os, io, re, random
import urllib.request
from os import remove
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    MessageMediaPhoto,
)

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+",
)

@Wbot(pattern="^/kang ?(.*)")
async def hehe(event):
    xx = await event.edit("`Processing...`")
    user.username = "RoseLoverX"
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            await xx.edit(f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await ubot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            await xx.edit(f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await ubot.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "video" in message.media.document.mime_type.split("/"):
            await xx.edit("Video type is not supported!")
        elif "tgsticker" in message.media.document.mime_type:
            await xx.edit(f"`{random.choice(KANGING_STR)}`")
            await ubot.download_file(
                message.media.document,
                "AnimatedSticker.tgs",
            )

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await xx.edit("`Unsupported File!`")
            return
    else:
        await xx.edit("`I can't kang that...`")
        return

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "🔰"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                pack = int(splat[1])
            else:
                emoji = splat[1]

        packname = f"Wy_{user.id}_{pack}"
        packnick = f"@{user.username}'s Pack {pack}"
        cmd = "/newpack"
        file = io.BytesIO()

        if not is_anim:
            image = photo
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"

        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}"),
        )
        htmlstr = response.read().decode("utf8").split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with ubot.conversation("@Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                await ubot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"ult_{user.id}_{pack}"
                    packnick = f"@{user.username}'s Pack {pack}"
                    await xx.edit(
                        "`Switching to Pack "
                        + str(pack)
                        + " due to insufficient space`",
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        await ubot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        await ubot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        await ubot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        await conv.get_response()
                        await ubot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        await ubot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        await ubot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await ubot.send_read_acknowledge(conv.chat_id)
                        await xx.edit(
                            f"`Sticker added in a Different Pack !\
                            \nThis Pack is Newly created!\
                            \nYour pack can be found [here](t.me/addstickers/{packname})",
                            parse_mode="md",
                        )
                        return
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await xx.edit(
                        "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`",
                    )
                    return
                await conv.send_message(emoji)
                await ubot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                await ubot.send_read_acknowledge(conv.chat_id)
        else:
            await xx.edit("`Brewing a new Pack...`")
            async with ubot.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                await ubot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                await ubot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await xx.edit(
                        "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`",
                    )
                    return
                await conv.send_message(emoji)
                await ubot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")

                await conv.get_response()
                await ubot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                await ubot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                await ubot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await ubot.send_read_acknowledge(conv.chat_id)
        await xx.edit(
            f"`Kanged!`\
            \n`Emoji` - {emoji}\
            \n`Sticker Pack` [here](t.me/addstickers/{packname})",
            parse_mode="md",
        )
        try:
            os.remove(photo)
        except BaseException:
            pass

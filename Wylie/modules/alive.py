from Wylie.events import Wbot
import time, datetime
from . import get_readable_time

@Wbot(pattern="^/ping")
async def _(event):
    start_time = datetime.datetime.now()
    message = await event.edit("Pinging.")
    end_time = datetime.datetime.now()
    pingtime = end_time - start_time
    telegram_ping = str(round(pingtime.total_seconds(), 2)) + "s"
    uptime = get_readable_time((time.time() - StartTime))
    await message.edit(
        "<b>Pong !! </b> <code>{}</code>\n"
        "<b>Uptime -</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode="html",
    )

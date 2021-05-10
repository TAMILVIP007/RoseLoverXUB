from Wylie.events import Cbot

@Cbot(pattern="^/ping")
async def _(event):
  await event.edit("Pong.")

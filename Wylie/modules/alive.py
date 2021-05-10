from Wylie.events import Wbot

@Wbot(pattern="^/ping")
async def _(event):
  await event.edit("Pong.")

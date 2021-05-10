from Wylie import ubot
from Wylie.events import Wbot

@Wbot(pattern="^/info ?(.*)")
async def new(event):
  

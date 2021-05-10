from Wylie import ubot, tbot, TOKEN
import Wylie.events
import sys

try:
  ubot.start()
  tbot.start()
except:
  print("Invalid STRING/Token__bot exiting...")
  sys.exit()
  
ubot.run_until_disconnected()
tbot.run_until_disconnected()

from Wylie import tbot, ubot, OWNER_ID
import os, glob, re, time, logging, sys
from pathlib import Path
from telethon import events

def Wbot(**args):
   pattern = args.get('pattern', None)
   r_pattern = r'^[/?!.]'
   if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern
   args['pattern'] = pattern.replace('^/', r_pattern, 1)
   def decorator(func):
        async def wrapper(check):
          print(check.sender_id)
          try:
                await func(check)
          except BaseException:
                return
        ubot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper
   return decorator   
  
def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import Wylie.events

        path = Path(f"Wylie/modules/{shortname}.py")
        name = "Wylie.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully imported " + shortname)
    else:
        import importlib
        import Wylie.events

        path = Path(f"Wylie/modules/{shortname}.py")
        name = "Wylie.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.ubot = ubot
        mod.tbot = tbot
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        sys.modules["Wylie.modules." + shortname] = mod
        print("Successfully imported " + shortname)
            
          
path = "Wylie/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", "")) 
           

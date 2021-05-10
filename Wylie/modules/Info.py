from Wylie import ubot
from Wylie.events import Wbot
from . import get_user

@Wbot(pattern="^/info ?(.*)")
async def new(event):
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   user = await ubot.get_entity(event.sender_id)
 else:
  try:
   user, extra = await get_user(event)
  except TypeError:
   pass
 user_id = user.id
 first_name = user.first_name
 last_name = user.last_name
 username = user.username
 text = "<b>User Information:</b>\n"
 text += f"<b>ID:</b> <code>{user_id}</code>\n"
 if first_name:
   text += f"<b>First Name:</b> {first_name}\n"
 if last_name:
   text += f"<b>Last Name:</b> {last_name}\n"
 if username:
   text += f"<b>Username:</b> @{username}\n"
 text += f'<b>User link:</b> <a href="tg://user?id={user_id}">{first_name}</a>'
 await event.edit(text, parse_mode='html')



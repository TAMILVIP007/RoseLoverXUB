from Wylie import ubot
from Wylie.events import Wbot
from . import get_user
from telethon.tl.functions.users import GetFullUserRequest

@Wbot(pattern="^/info ?(.*)")
async def new(event):
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   user = await ubot.get_entity(event.sender_id)
 else:
  try:
   user, extra = await get_user(event)
  except TypeError as e:
   print(e)
   pass
 user_id = user.id
 first_name = user.first_name
 last_name = user.last_name
 username = user.username
 text = "╒═══「<b>User info</b>:\n"
 if first_name:
   text += f"<b>First Name:</b> {first_name}\n"
 if last_name:
   text += f"<b>Last Name:</b> {last_name}\n"
 ups = None
 if username:
   text += f"<b>Username:</b> @{username}\n"
   ups = await event.client(GetFullUserRequest(user.username))
 text += f"<b>ID:</b> <code>{user_id}</code>\n"
 text += f'<b>User link:</b> <a href="tg://user?id={user_id}">{first_name}</a>'
 if ups:
  text += f"\n\n<b>Bio:</b> <code>{ups.about}</code>"
  text += f"\n\n<b>Gbanned: No</b>"
  text += f"\n\n╘══「 <b>Groups count:</b> {ups.common_chats_count} 」"
 await event.edit(text, parse_mode='html')


@Wbot(pattern="^/id ?(.*)")
async def _t(event):
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   user = await ubot.get_entity(event.sender_id)
 else:
  try:
   user, extra = await get_user(event)
  except TypeError as e:
   print(e)
   pass
 user_id = user.id
 chat_id = event.chat_id
 msg_id = event.id
 text = "**[Chat ID]**(http://t.me/{event.chat.username}): `{chat_id}`"
 if event.reply_to_msg_id:
   print(5)

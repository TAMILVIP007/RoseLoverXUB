from telethon import TelegramClient
from telethon.sessions import StringSession
from datetime import datetime
import os, logging
from logging import basicConfig, getLogger, INFO
"""RoseLoverX"""
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

StartTime = datetime.now()

STRING_SESSION = os.environ.get("STRING_SESSION")
TOKEN = os.environ.get("TOKEN")
OWNER_ID = os.environ.get("OWNER_ID")
API_KEY = os.environ.get("API_KEY")
API_HASH = os.environ.get("API_HASH")
print(OWNER_ID)

ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
tbot = TelegramClient(None, API_KEY, API_HASH)


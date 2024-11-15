import time
import logging

import uvloop
from Abg import patch
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient

import config

from .misc import LOGGER


CLONE_OWNERS = {}
uvloop.install()
boot = time.time()
mongodb = AsyncIOMotorClient(config.MONGO_URL)
db = mongodb.Anonymous
OWNER = config.OWNER_ID


clonedb = {}
db = {}


class nexichat(Client):
    def __init__(self):
        super().__init__(
            name="nexichat",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention


nexichat = nexichat()

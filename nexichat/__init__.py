import time
import logging

import uvloop
from Abg import patch
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import BotCommand
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
        try:
            await self.set_bot_commands(
                commands=[
                    BotCommand("start", "Start the bot"),
                    BotCommand("help", "Get the help menu"),
                    BotCommand("clone", "Make your own chatbot"),
                    BotCommand("ping", "Check if the bot is alive or dead"),
                    BotCommand("lang", "Select bot reply language"),
                    BotCommand("resetlang", "Reset to default bot reply lang"),
                BotCommand("id", "Get users user_id"),
                BotCommand("stats", "Check bot stats"),
                BotCommand("gcast", "Broadcast any message to groups/users"),
                BotCommand("chatbot", "Enable or disable chatbot"),
                BotCommand("status", "Check chatbot enable or disable in chat"),
                BotCommand("shayri", "Get random shayri for love"),
                BotCommand("repo", "Get chatbot source code"),
                ]
            )
            LOGGER.info("Bot commands set successfully.")
        except Exception as ex:
            LOGGER.error(f"Failed to set bot commands: {ex}")


nexichat = nexichat()

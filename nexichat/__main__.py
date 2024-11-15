import asyncio
import importlib
import threading

from flask import Flask
from pyrogram import idle
from pyrogram.types import BotCommand

from config import OWNER_ID
from nexichat import LOGGER, nexichat
from nexichat.modules import ALL_MODULES
from nexichat.modules.Clone import restart_bots


async def anony_boot():
    try:
        await nexichat.start()

        await restart_bots()

    except Exception as ex:
        LOGGER.error(ex)

    for all_module in ALL_MODULES:
        importlib.import_module("nexichat.modules." + all_module)
        LOGGER.info(f"Successfully imported : {all_module}")
    LOGGER.info(f"@{nexichat.username} Started.")
    try:
        await nexichat.send_message(int(OWNER_ID), f"{nexichat.mention} has started")
    except Exception as ex:
        LOGGER.info(
            f"@{nexichat.username} Started, please start the bot from owner id."
        )

    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("Stopping nexichat Bot...")

from pyrogram import Client, filters
# from TheApi import api
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from deep_translator import GoogleTranslator

from nexichat import db, nexichat
from nexichat.modules.helpers import CHATBOT_ON, languages


translator = GoogleTranslator()

lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status


@nexichat.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    chat_id = message.chat.id
    chat_status = await status_db.find_one({"chat_id": chat_id})
    if chat_status:
        current_status = chat_status.get("status", "not found")
        await message.reply(f"Chatbot status for this chat: **{current_status}**")
    else:
        await message.reply("No status found for this chat.")


def generate_language_buttons(languages):
    buttons = []
    current_row = []
    for lang, code in languages.items():
        current_row.append(
            InlineKeyboardButton(lang.capitalize(), callback_data=f"setlang_{code}")
        )
        if len(current_row) == 4:
            buttons.append(current_row)
            current_row = []
    if current_row:
        buttons.append(current_row)
    return InlineKeyboardMarkup(buttons)


async def get_chat_language(chat_id):
    chat_lang = await lang_db.find_one({"chat_id": chat_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else "en"


@nexichat.on_message(filters.command(["lang", "language", "setlang"]))
async def set_language(client: Client, message: Message):
    await message.reply_text(
        "Please select your chat language:",
        reply_markup=generate_language_buttons(languages),
    )


@nexichat.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    chat_id = message.chat.id
    chat_status = await status_db.find_one({"chat_id": chat_id})
    if chat_status:
        current_status = chat_status.get("status", "not found")
        await message.reply(f"Chatbot status for this chat: **{current_status}**")
    else:
        await message.reply("No status found for this chat.")


@nexichat.on_message(filters.command(["lang", "language", "setlang"]))
async def set_language(client: Client, message: Message):
    await message.reply_text(
        "Please select your chat language:",
        reply_markup=generate_language_buttons(languages),
    )


@nexichat.on_message(filters.command(["resetlang", "nolang"]))
async def reset_language(client: Client, message: Message):
    chat_id = message.chat.id
    lang_db.update_one(
        {"chat_id": chat_id}, {"$set": {"language": "nolang"}}, upsert=True
    )
    await message.reply_text(
        "**Bot language has been reset in this chat to mix language.**"
    )


@nexichat.on_message(filters.command("chatbot"))
async def chatbot_command(client: Client, message: Message):
    await message.reply_text(
        f"Chat: {message.chat.title}\n**Choose an option to enable/disable the chatbot.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

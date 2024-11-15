import random

from pyrogram import Client, filters
from pyrogram.types import Message
from deep_translator import GoogleTranslator
from pyrogram.errors import MessageEmpty

from nexichat import db
from nexichat.database import add_served_cchat, add_served_cuser
from nexichat.database.chats import add_served_chat
from nexichat.database.users import add_served_user
from nexichat.mplugin.helpers import chatai


translator = GoogleTranslator()

lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status

replies_cache = []


async def load_replies_cache():
    global replies_cache
    replies_cache = await chatai.find().to_list(length=None)


async def save_reply(original_message: Message, reply_message: Message):
    global replies_cache
    try:
        reply_data = {
            "word": original_message.text,
            "text": None,
            "check": "none",
        }

        if reply_message.sticker:
            reply_data["text"] = reply_message.sticker.file_id
            reply_data["check"] = "sticker"
        elif reply_message.photo:
            reply_data["text"] = reply_message.photo.file_id
            reply_data["check"] = "photo"
        elif reply_message.video:
            reply_data["text"] = reply_message.video.file_id
            reply_data["check"] = "video"
        elif reply_message.audio:
            reply_data["text"] = reply_message.audio.file_id
            reply_data["check"] = "audio"
        elif reply_message.animation:
            reply_data["text"] = reply_message.animation.file_id
            reply_data["check"] = "gif"
        elif reply_message.voice:
            reply_data["text"] = reply_message.voice.file_id
            reply_data["check"] = "voice"
        elif reply_message.text:
            translated_text = reply_message.text
            """try:
                await asyncio.sleep(1)
                translated_text = GoogleTranslator(source='auto', target='en').translate(reply_message.text)
            except Exception as e:
                print(f"Translation error: {e}, saving original text.")
                translated_text = reply_message.text"""
            reply_data["text"] = translated_text
            reply_data["check"] = "none"

        is_chat = await chatai.find_one(reply_data)
        if not is_chat:
            await chatai.insert_one(reply_data)
            replies_cache.append(reply_data)

    except Exception as e:
        print(f"Error in save_reply: {e}")


async def get_reply(word: str):
    global replies_cache
    if not replies_cache:
        await load_replies_cache()

    relevant_replies = [reply for reply in replies_cache if reply["word"] == word]
    if not relevant_replies:
        relevant_replies = replies_cache
    return random.choice(relevant_replies) if relevant_replies else None


async def get_chat_language(chat_id):
    chat_lang = await lang_db.find_one({"chat_id": chat_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else None


@Client.on_message(filters.incoming)
async def chatbot_response(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        chat_status = await status_db.find_one({"chat_id": chat_id})

        if chat_status and chat_status.get("status") == "disabled":
            return

        if message.text and any(
            message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]
        ):
            if message.chat.type in ["group", "supergroup"]:
                await add_served_cchat(bot_user_id, message.chat.id)
                return await add_served_chat(message.chat.id)
            else:
                await add_served_cuser(bot_user_id, message.chat.id)
                return await add_served_user(message.chat.id)

        if (
            message.reply_to_message
            and message.reply_to_message.from_user.id == client.me.id
        ) or not message.reply_to_message:
            reply_data = await get_reply(message.text)

            if reply_data:
                response_text = reply_data["text"]
                chat_lang = await get_chat_language(chat_id)

                if not chat_lang or chat_lang == "nolang":
                    translated_text = response_text
                else:
                    translated_text = GoogleTranslator(
                        source="auto", target=chat_lang
                    ).translate(response_text)
                    if not translated_text:
                        translated_text = response_text
                if reply_data["check"] == "sticker":
                    await message.reply_sticker(reply_data["text"])
                elif reply_data["check"] == "photo":
                    await message.reply_photo(reply_data["text"])
                elif reply_data["check"] == "video":
                    await message.reply_video(reply_data["text"])
                elif reply_data["check"] == "audio":
                    await message.reply_audio(reply_data["text"])
                elif reply_data["check"] == "gif":
                    await message.reply_animation(reply_data["text"])
                elif reply_data["check"] == "voice":
                    await message.reply_voice(reply_data["text"])
                else:
                    await message.reply_text(translated_text)
            else:
                await message.reply_text("**I don't understand. What are you saying?**")

        if message.reply_to_message:
            await save_reply(message.reply_to_message, message)

    except MessageEmpty:
        await message.reply_text("🙄🙄")
    except Exception as e:
        return

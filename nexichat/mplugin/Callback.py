from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from nexichat import LOGGER, db
from nexichat.mplugin.helpers import (
    BACK,
    START,
    DEV_OP,
    HELP_BTN,
    ABOUT_BTN,
    HELP_READ,
    ABOUT_READ,
    ADMIN_READ,
    SOURCE_READ,
    CHATBOT_BACK,
    CHATBOT_READ,
    MUSIC_BACK_BTN,
    TOOLS_DATA_READ,
    languages,
)


lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status


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


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    LOGGER.info(query.data)

    # Help menu
    if query.data == "HELP":
        await query.message.edit_text(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
            disable_web_page_preview=True,
        )

    # Close menu
    elif query.data == "CLOSE":
        await query.message.delete()
        await query.answer("Closed menu!", show_alert=True)

    # Go back to the main menu
    elif query.data == "BACK":
        await query.message.edit(
            text=START,
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )

    # Show source information
    elif query.data == "SOURCE":
        await query.message.edit(
            text=SOURCE_READ,
            reply_markup=InlineKeyboardMarkup(BACK),
            disable_web_page_preview=True,
        )

    # Show about information
    elif query.data == "ABOUT":
        await query.message.edit(
            text=ABOUT_READ,
            reply_markup=InlineKeyboardMarkup(ABOUT_BTN),
            disable_web_page_preview=True,
        )

    # Show admin information
    elif query.data == "ADMINS":
        await query.message.edit(
            text=ADMIN_READ,
            reply_markup=InlineKeyboardMarkup(MUSIC_BACK_BTN),
        )

    # Show tools information
    elif query.data == "TOOLS_DATA":
        await query.message.edit(
            text=TOOLS_DATA_READ,
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )

    # Back to the help menu
    elif query.data == "BACK_HELP":
        await query.message.edit(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )

    # Chatbot commands
    elif query.data == "CHATBOT_CMD":
        await query.message.edit(
            text=CHATBOT_READ,
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )

    # Back to the chatbot menu
    elif query.data == "CHATBOT_BACK":
        await query.message.edit(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )

    # Enable chatbot for the chat
    elif query.data == "enable_chatbot":
        chat_id = query.message.chat.id
        status_db.update_one(
            {"chat_id": chat_id}, {"$set": {"status": "enabled"}}, upsert=True
        )
        await query.answer("Chatbot enabled ✅", show_alert=True)
        await query.edit_message_text(
            f"Chat: {query.message.chat.title}\n**Chatbot has been enabled.**"
        )

    # Disable chatbot for the chat
    elif query.data == "disable_chatbot":
        chat_id = query.message.chat.id
        status_db.update_one(
            {"chat_id": chat_id}, {"$set": {"status": "disabled"}}, upsert=True
        )
        await query.answer("Chatbot disabled!", show_alert=True)
        await query.edit_message_text(
            f"Chat: {query.message.chat.title}\n**Chatbot has been disabled.**"
        )

    # Set chat language
    elif query.data.startswith("setlang_"):
        lang_code = query.data.split("_")[1]
        chat_id = query.message.chat.id
        if lang_code in languages.values():
            lang_db.update_one(
                {"chat_id": chat_id}, {"$set": {"language": lang_code}}, upsert=True
            )
            await query.answer(
                f"Your chat language has been set to {lang_code.title()}.",
                show_alert=True,
            )
            await query.message.edit_text(
                f"Chat language has been set to {lang_code.title()}."
            )
        else:
            await query.answer("Invalid language selection.", show_alert=True)

    # Reset language selection to mix language
    elif query.data == "nolang":
        chat_id = query.message.chat.id
        lang_db.update_one(
            {"chat_id": chat_id}, {"$set": {"language": "nolang"}}, upsert=True
        )
        await query.answer(
            "Bot language has been reset to mix language.", show_alert=True
        )
        await query.message.edit_text(
            "**Bot language has been reset to mix language.**"
        )

    # Choose language for the chatbot
    elif query.data == "choose_lang":
        await query.answer("Choose chatbot language for this chat.", show_alert=True)
        await query.message.edit_text(
            "**Please select your preferred language for the chatbot.**",
            reply_markup=generate_language_buttons(languages),
        )

from config import OWNER_ID
from nexichat import CLONE_OWNERS


def is_owner(client, user_id):
    bot_id = client.me.id
    if CLONE_OWNERS.get(bot_id) == user_id or user_id == OWNER_ID:
        return True
    return "You don't have permission to use this command on this bot."

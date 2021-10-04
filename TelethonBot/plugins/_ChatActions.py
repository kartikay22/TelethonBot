from pyUltroid.functions.all import get_chatbot_reply
from pyUltroid.functions.chatBot_db import chatbot_stats
from pyUltroid.functions.clean_db import *
from pyUltroid.functions.forcesub_db import *
from pyUltroid.functions.gban_mute_db import *
from pyUltroid.functions.greetings_db import *
from pyUltroid.functions.username_db import *
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.utils import get_display_name

from . import *


@ultroid_bot.on(events.ChatAction())
async def ChatActionsHandler(ult):  # sourcery no-metrics
    # clean chat actions
    if is_clean_added(ult.chat_id):
        try:
            await ult.delete()
        except BaseException:
            pass

    # thank members
    if must_thank(ult.chat_id):
        chat_count = len(await ult.client.get_participants(await ult.get_chat()))
        if chat_count % 100 == 0:
            stik_id = chat_count / 100 - 1
            sticker = stickers[stik_id]
            await ultroid.send_message(ult.chat_id, file=sticker)
    # force subscribe
    if (
        udB.get("FORCESUB")
        and ((ult.user_joined or ult.user_added))
        and get_forcesetting(ult.chat_id)
    ):

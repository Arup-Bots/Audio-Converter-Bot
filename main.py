import os
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel 

#configs 
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/AudioBoT/")
FSUB_CHANNEL = os.environ.get("FSUB_CHANNEL", "")

#strings
START_TEXT = """
Hey {}, I am Audio Converter Bot . I can help you to convert any video to audio . Hit /convert to convert .
"""
CONVERT_TEXT = """
Send video message to convert to audio .
"""

DevelopedBots = Client(
    "Audio-Converter-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@DevelopedBots.on_message(filters.command(["start"]))
async def text(bot, update):
    FSUB_CHANNEL = FSUB_CHANNEL
    if FSUB_CHANNEL:
        try:
            user = await bot.get_chat_member(FSUB_CHANNEL, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry, You are **B A N N E D**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{FSUB_CHANNEL} To Use Me")
            await update.reply_text(
                text="**📲 Please Join My Update Channel Before Using Me 📲**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="↗️ Join My Updates Channel ↗️", url=f"https://t.me/{FSUB_CHANNEL}")]
              ])
            )
            return
        else:
            await update.reply_text(START_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Channel 🔔', url='https://t.me/DevelopedBots'),
                    InlineKeyboardButton('Support 📢', url='https://t.me/DevelopedBotz')
                ],
                [
                    InlineKeyboardButton('Source 🖥', url='https://github.com/Kunal-Diwan/Audio-Converter-Bot'),
                    InlineKeyboardButton('Dev 👨‍💻', url='https://t.me/Kunaldiwan')
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )
            return 

@DevelopedBots.on_message(filters.command(["convert"]))
async def convert(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=CONVERT_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

@DevelopedBots.on_message(filters.video & filters.private)
async def mp3(bot, message):
    
    # download video
    file_path = DOWNLOAD_LOCATION + f"{message.from_user.id}.mp3"
    txt = await message.reply_text("Downloading to My server.....")
    await message.download(file_path)
    await txt.edit_text("Downloaded Successfully")
    
    # convert to audio
    await txt.edit_text("Converting to audio")
    await message.reply_audio(audio=file_path, caption="@DevelopedBots", quote=True)
    
    # remove file
    try:
        os.remove(file_path)
    except:
        pass
    
    await txt.delete()


DevelopedBots.run()

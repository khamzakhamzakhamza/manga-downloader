from telegram.ext import ConversationHandler
from manga_bato_downloader_bot.core.compressor import Compressor
import re

BATO_LINK_PATTERN = re.compile(
    r"^https://bato\.to/title/[a-zA-Z0-9_-]+/[0-9]+-ch_[0-9]+/?$"
)

async def download_command(update, context):
    link = update.message.text

    if not BATO_LINK_PATTERN.match(link):
        await update.message.reply_text("🤖: Link is invalid 😭\n\nPlease make sure link matches expected pattern: https://bato.to/title/manga-name/1111111-ch_1 \n\nTry again: /download")
        return ConversationHandler.END
    
    await update.message.reply_text("🤖: Saving BL manga chapters...")

    compressor = Compressor()
    compressor.compress_folder("test", "test_1")

    await update.message.reply_text("🤖: Max BL capacity reached! 💥(×_×)💥\n\n To download some more: /download")

    return ConversationHandler.END

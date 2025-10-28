import os
from telegram.ext import ConversationHandler
from manga_bato_downloader_bot.core.bato_scraper_interface import BatoScraper
from manga_bato_downloader_bot.core.http_v3_bato_scraper import HttpV3BatoScraper
import re

BATO_LINK_PATTERN = re.compile(
    r"^https://bato\.to/title/[a-zA-Z0-9_-]+/[0-9]+-ch_[0-9]+/?$"
)

async def download_command(update, _):
    link = update.message.text

    if not BATO_LINK_PATTERN.match(link):
        await update.message.reply_text("🤖: Link is invalid 😭\n\nPlease make sure link matches expected pattern: https://bato.to/title/manga-name/1111111-ch_1 \n\nTry again: /download")
        return ConversationHandler.END
    
    scraper: BatoScraper = HttpV3BatoScraper(link)
    await update.message.reply_text("🤖: Saving BL manga chapters...")

    try:
        while scraper.has_more_chapters:
            chapter_pdf_path = await scraper.download_next_chapter()
        
            if chapter_pdf_path:
                with open(chapter_pdf_path, "rb") as f:
                    await update.message.reply_document(f, filename=os.path.basename(f"{await scraper.get_current_chapter_name()} from {await scraper.get_title()}.pdf"))

        await update.message.reply_text("🤖: Max BL capacity reached! 💥(×_×)💥\n\n To download some more: /download")
    except Exception as e:
        await update.message.reply_text(f"🤖: An error occurred 😭: {str(e)}\n\nTry again later: /download")

    await scraper.cleanup()
    return ConversationHandler.END

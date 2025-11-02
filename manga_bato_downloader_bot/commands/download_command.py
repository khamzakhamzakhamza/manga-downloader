from datetime import datetime, timezone 
import os
import uuid
from telegram.ext import ConversationHandler
from manga_bato_downloader_bot.core.bato_scraper_interface import BatoScraper
from manga_bato_downloader_bot.core.http_v3_bato_scraper import HttpV3BatoScraper
import re

BATO_LINK_PATTERN = re.compile(
    r"^https://bato\.to/title/[^/]+/[0-9]+-[^/]+/?$"
)

async def download_command(update, _):
    correlation_id = uuid.uuid4()
    
    link = update.message.text
    print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Starting dowload. Link {link}", flush=True)

    if not BATO_LINK_PATTERN.match(link):
        await update.message.reply_text("🤖: Link is invalid 😭\n\nPlease make sure link matches expected pattern: https://bato.to/title/manga-name/1111111-ch_1 \n\nTry again: /download")
        print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Validation failed", flush=True)
        return ConversationHandler.END
    
    scraper: BatoScraper = HttpV3BatoScraper(link)
    await update.message.reply_text("🤖: Saving BL manga chapters...")
    
    try:
        while scraper.has_more_chapters:
            chapter_pdf_path = await scraper.download_next_chapter()
            print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Downloaded chapter {scraper.get_title()} {scraper.get_current_chapter_name()}", flush=True)

            if chapter_pdf_path:
                with open(chapter_pdf_path, "rb") as f:
                    await update.message.reply_document(f, filename=os.path.basename(f"{scraper.get_current_chapter_name()} from {scraper.get_title()}.pdf"))

        await update.message.reply_text("🤖: Max BL capacity reached! 💥(×_×)💥\n\n To download some more: /download")
        print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Download success", flush=True)
    except Exception as e:
        print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Download failed. Exception: {e}", flush=True)
        await update.message.reply_text(f"🤖: An error occurred 😭\n\nTry again later: /download")

    scraper.cleanup()
    print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Cleanup finished", flush=True)
    return ConversationHandler.END

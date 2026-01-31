from datetime import datetime, timezone 
import os
import uuid
from telegram.ext import ConversationHandler
from manga_bato_downloader_bot.core.scraper_interface import MangaScraper
from manga_bato_downloader_bot.core.mangago_scraper import MangagoScraper

async def download_command(update, _):
    correlation_id = uuid.uuid4()

    link = update.message.text
    print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Starting dowload. Link {link}", flush=True)

    if "mangago" not in link:
        await update.message.reply_text("🤖: Only Mangago links are supported. Send a Mangago chapter link.")
        return ConversationHandler.END

    scraper: MangaScraper = MangagoScraper(link)

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

from datetime import datetime, timezone
import uuid
from telegram.ext import ConversationHandler
from manga_downloader_bot.core.scraping_orchestrator import ScrapingOrchestrator
from manga_downloader_bot.core.pdf_builder import PdfBuilder
from manga_downloader_bot.core.upload import S3PublicUploader

async def download_command(update, _):
    correlation_id = uuid.uuid4()

    link = update.message.text
    print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Starting dowload. Link {link}", flush=True)

    if "mangago" not in link or not link.endswith(".me/") and ".me/" not in link:
        await update.message.reply_text("🤖: Only Mangago (.me) links are supported. Send a Mangago chapter link.\n\nTry again: /download")
        return ConversationHandler.END

    scraper = ScrapingOrchestrator(link)
    pdf_builder = PdfBuilder()
    uploader = S3PublicUploader()

    downloaded_pdfs: list[bytes] = []

    status_msg = await update.message.reply_text("🤖: Downloaded 0 chapters...")

    try:
        title: str|None = None

        while scraper.has_more_chapters:
            chapter = await scraper.download_next_chapter()
            title = chapter.title
            print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Downloaded chapter {chapter.title} {chapter.chapter_name}", flush=True)

            if chapter.imgs:
                pdf_bytes = pdf_builder.build(chapter.imgs)
                downloaded_pdfs.append(pdf_bytes)
                await status_msg.edit_text(f"🤖: Downloaded {len(downloaded_pdfs)} chapter(s)...")

        folder_url = uploader.upload_manga(title, downloaded_pdfs)
        await update.message.reply_text(f"🤖: Max manga capacity reached! 💥(×_×)💥\n\nDownload your manga here: {folder_url} \n\n To download some more: /download")
        print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Download success", flush=True)
    except Exception as e:
        print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Download failed. Exception: {e}", flush=True)
        await update.message.reply_text(f"🤖: An error occurred 😭\n\nTry again later: /download")

    scraper.cleanup()
    print(f"{datetime.now(timezone.utc).isoformat()} {correlation_id} Cleanup finished", flush=True)
    return ConversationHandler.END

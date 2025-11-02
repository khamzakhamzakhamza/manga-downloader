from datetime import datetime, timezone
import os
from telegram.ext import Application, MessageHandler, CommandHandler, ConversationHandler, filters
from manga_bato_downloader_bot.commands.download_command import download_command as download
from manga_bato_downloader_bot.commands.get_link_command import get_link_command as get_link
from manga_bato_downloader_bot.commands.cancel_command import cancel_command as cancel
from manga_bato_downloader_bot.commands.states import States
from dotenv import load_dotenv

load_dotenv()

WELCOME_MSG = "🤖: Hello! I'm Manga Downloader Bot. Send /download to start downloading mangas from https://bato.to/v3x"
TOKEN = os.getenv("TOKEN")

async def reply(update, _):
    await update.message.reply_text(WELCOME_MSG)

def main():
    builder = Application.builder()
    builder.token(TOKEN)
    builder.concurrent_updates(True)
    builder.read_timeout(30)
    builder.write_timeout(30)
    application = builder.build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("download", get_link)],
        states={
            States.GET_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, download)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv)
    application.add_handler(MessageHandler(filters.TEXT, reply))
    
    print(f"{datetime.now(timezone.utc).isoformat()} Telegram Bot started!", flush=True)
    application.run_polling()

if __name__ == '__main__':
    main()

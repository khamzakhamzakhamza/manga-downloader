from .states import States

async def get_link_command(update, _):
    await update.message.reply_text("🤖: Send me the link to the first chapter (ex. https://bato.to/title/manga-name/1111111-ch_1)")
    return States.GET_LINK

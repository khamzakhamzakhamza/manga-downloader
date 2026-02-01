from .states import States

async def get_link_command(update, _):
    await update.message.reply_text("🤖: Send me the link to the first chapter (Mangago links supported)")
    return States.GET_LINK

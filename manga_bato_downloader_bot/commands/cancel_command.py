from telegram.ext import ConversationHandler

async def cancel_command(update, _):
    await update.message.reply_text("🤖: Maybe next time ✌️")
    return ConversationHandler.END

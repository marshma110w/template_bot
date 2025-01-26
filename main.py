from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TG_BOT_TOKEN")
assert TELEGRAM_TOKEN, "Token not found in env"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_name = update.message.from_user.first_name  # type: ignore
    await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text=f"Привет, {sender_name}!",
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,  # type: ignore
        text=update.message.text,  # type: ignore
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()

from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from pathlib import Path
from bot.handlers import upload_template_handler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TG_BOT_TOKEN")
assert TELEGRAM_TOKEN, "Token not found in env"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_name = update.message.from_user.first_name
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Привет, {sender_name}!",
        )


async def document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_name = document.file_name
    file = await document.get_file()
    await file.download_to_drive(custom_path=Path(file_name))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🤷‍♂️")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    document_handler = MessageHandler(filters.Document.FileExtension("doc"), document)
    unknown_command_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    # application.add_handler(document_handler)
    application.add_handler(upload_template_handler)

    application.add_handler(unknown_command_handler)

    application.run_polling()

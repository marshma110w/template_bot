from telegram import Update
from telegram.ext import filters, ContextTypes, ConversationHandler, CommandHandler, MessageHandler

TEMPLATE, TEMPLATE_NAME = range(2)


async def upload_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь файл с шаблоном")
    return TEMPLATE


async def get_template_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_name = document.file_name
    
    context.user_data["document"] = document
    # temp logic
    if not file_name.endswith(".docx"):
        await update.message.reply_text("Это должен быть docx файл :(")
        return TEMPLATE

    else:
        await update.message.reply_text("Шаблон прошел проверку. Введи название для этого шаблона")
        return TEMPLATE_NAME


async def get_template_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    template_name = update.message.text
    
    if "trojan" in template_name:
        await update.message.reply_text("Ах ты хитрый жук, ничего не загружу тебе")
        return ConversationHandler.END
    
    else:
        # TODO: save file to s3
        # TODO: save file to pg
        await update.message.reply_text(f"Шаблон {template_name} загружен!")
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отбой")
    context.user_data.clear()
    return ConversationHandler.END


upload_template_handler = ConversationHandler(
    entry_points=[CommandHandler("upload", upload_template)],
    states={
        TEMPLATE: [MessageHandler(filters.Document.ALL, get_template_file)],
        TEMPLATE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_template_name)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
import logging
import os
import sys
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN не установлен!")
    sys.exit(1)

logger.info(f"🚀 Бот басталуда... TOKEN: {BOT_TOKEN[:20]}...")

def start(update: Update, context):
    update.message.reply_text(
        "Қазақ әдебиеті ботына қош келдіңіз! 📚\n\n"
        "Команды:\n/help - Көмек\n/about - Туралы"
    )

def help_command(update: Update, context):
    update.message.reply_text(
        "Бот қазақ әдебиеті туралы ақпарат беріп тұрады.\n"
        "Сұрақ қойыңыз немесе автордың атын жазыңыз."
    )

def about(update: Update, context):
    update.message.reply_text(
        "Қазақ әдебиеті ботының v4.0\nАвтор: Aseke\n2026"
    )

def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Сообщение от {update.effective_user.id}: {user_message}")
    update.message.reply_text(
        f"Спасибо за сообщение: {user_message}\nБот разрабатывается..."
    )

# ✅ ИСПРАВЛЕНО: (update, context) вместо (bot, update, error)
def error_handler(update, context):
    error = context.error
    logger.error(f"Update {update} caused error {error}")
    if "Conflict" in str(error):
        logger.warning("Conflict detected - another bot instance is running")
        return
    logger.error(msg="Exception while handling an update:", exc_info=error)

def main() -> None:
    try:
        updater = Updater(BOT_TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("about", about))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        dispatcher.add_error_handler(error_handler)

        logger.info("✅ Бот успешно запущен!")
        # ✅ ИСПРАВЛЕНО: drop_pending_updates=True убирает Conflict ошибку
        updater.start_polling(drop_pending_updates=True)
        updater.idle()
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

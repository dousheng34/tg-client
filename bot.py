import logging
import os
import sys
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена из переменной окружения
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN не установлен!")
    sys.exit(1)

logger.info(f"🚀 Бот басталуда... TOKEN: {BOT_TOKEN[:20]}...")

# Обработчики команд
def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    update.message.reply_text(
        "Қазақ әдебиеті ботына қош келдіңіз! 📚\n\n"
        "Команды:\n"
        "/help - Көмек\n"
        "/about - Туралы"
    )

def help_command(update: Update, context: CallbackContext):
    """Обработчик команды /help"""
    update.message.reply_text(
        "Бот қазақ әдебиеті туралы ақпарат беріп тұрады.\n"
        "Сұрақ қойыңыз немесе автордың атын жазыңыз."
    )

def about(update: Update, context: CallbackContext):
    """Обработчик команды /about"""
    update.message.reply_text(
        "Қазақ әдебиеті ботының v4.0\n"
        "Автор: Aseke\n"
        "2026"
    )

def handle_message(update: Update, context: CallbackContext):
    """Обработчик обычных сообщений"""
    user_message = update.message.text
    logger.info(f"Сообщение от {update.effective_user.id}: {user_message}")
    
    update.message.reply_text(
        f"Спасибо за сообщение: {user_message}\n"
        "Бот разрабатывается..."
    )

def error_handler(update: Update, context: CallbackContext):
    """Обработчик ошибок"""
    error = context.error
    logger.error(f"Update {update} caused error {error}")
    
    # Игнорируем ошибку конфликта (другой экземпляр бота)
    if "Conflict" in str(error):
        logger.warning("Conflict detected - another bot instance is running")
        return
    
    # Логируем другие ошибки
    logger.error(msg="Exception while handling an update:", exc_info=error)

def main() -> None:
    """Запуск бота"""
    try:
        # Создание updater
        updater = Updater(BOT_TOKEN)
        dispatcher = updater.dispatcher

        # Добавление обработчиков команд
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("about", about))

        # Добавление обработчика сообщений
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

        # Добавление обработчика ошибок
        dispatcher.add_error_handler(error_handler)

        # Запуск бота
        logger.info("✅ Бот успешно запущен!")
        updater.start_polling()
        updater.idle()
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

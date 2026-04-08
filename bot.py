import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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
    exit(1)

logger.info(f"🚀 Бот басталуда... TOKEN: {BOT_TOKEN[:20]}...")

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Қазақ әдебиеті ботына қош келдіңіз! 📚\n\n"
        "Команды:\n"
        "/help - Көмек\n"
        "/about - Туралы"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(
        "Бот қазақ әдебиеті туралы ақпарат беріп тұрады.\n"
        "Сұрақ қойыңыз немесе автордың атын жазыңыз."
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /about"""
    await update.message.reply_text(
        "Қазақ әдебиеті ботының v4.0\n"
        "Автор: Aseke\n"
        "2026"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик обычных сообщений"""
    user_message = update.message.text
    logger.info(f"Сообщение от {update.effective_user.id}: {user_message}")
    
    await update.message.reply_text(
        f"Спасибо за сообщение: {user_message}\n"
        "Бот разрабатывается..."
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """Запуск бота"""
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))

    # Добавление обработчика сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Добавление обработчика ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    logger.info("✅ Бот успешно запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()

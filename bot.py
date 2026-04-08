"""
🤖 Telegram Bot для Казахской Литературы
Версия 2.0 - С улучшенными кнопками и функциональностью
Использует переменные окружения для безопасности
Совместим с Koyeb, Render и локальным развертыванием
"""

import logging
import os
import threading
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from aiohttp import web

# Загрузка переменных окружения из .env файла (для локального тестирования)
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена из переменной окружения
# Поддерживает оба варианта: TELEGRAM_BOT_TOKEN (Koyeb) и TOKEN (локально)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN или TOKEN не найдены в переменных окружения!")

logger.info(f"✅ Бот инициализирован с ID: {os.getenv('BOT_ID', 'unknown')}")

# ============================================================================
# ДАННЫЕ КОНТЕНТА
# ============================================================================

CHAPTERS = {
    "klassik": {
        "name": "📚 Классическая литература",
        "emoji": "📖",
        "description": "Великие произведения казахской классики"
    },
    "balalar": {
        "name": "👶 Детская литература",
        "emoji": "🧒",
        "description": "Произведения для детей и подростков"
    },
    "modern": {
        "name": "🌟 Современная литература",
        "emoji": "✨",
        "description": "Произведения современных авторов"
    },
    "poetry": {
        "name": "🎭 Поэзия",
        "emoji": "📝",
        "description": "Стихотворения и поэтические произведения"
    },
    "drama": {
        "name": "🎪 Драматургия",
        "emoji": "🎬",
        "description": "Пьесы и драматические произведения"
    },
    "folklore": {
        "name": "🏛️ Фольклор",
        "emoji": "🎵",
        "description": "Народные сказки и легенды"
    }
}

AUTHORS = {
    "abai": {
        "name": "Абай Кунанбаев",
        "emoji": "👨‍🎓",
        "bio": "Великий казахский поэт, философ и просветитель (1840-1904)",
        "works": ["Қара сөз", "Өлеңдер"]
    },
    "auezov": {
        "name": "Мухтар Ауэзов",
        "emoji": "📖",
        "bio": "Классик казахской литературы, автор романа 'Абай' (1897-1961)",
        "works": ["Абай", "Путь Абая"]
    },
    "dostoevsky": {
        "name": "Достоевский (влияние)",
        "emoji": "🖋️",
        "bio": "Русский писатель, оказавший влияние на казахскую литературу",
        "works": ["Преступление и наказание"]
    },
    "tolstoy": {
        "name": "Толстой (влияние)",
        "emoji": "📚",
        "bio": "Русский писатель, чьи идеи повлияли на казахских авторов",
        "works": ["Война и мир"]
    }
}

WORKS = {
    "abai_novel": {
        "title": "Абай",
        "author": "Мухтар Ауэзов",
        "year": 1942,
        "description": "Эпический роман о жизни и творчестве Абая Кунанбаева"
    },
    "kara_soz": {
        "title": "Қара сөз",
        "author": "Абай Кунанбаев",
        "year": 1889,
        "description": "Философские размышления и наставления"
    },
    "olendar": {
        "title": "Өлеңдер",
        "author": "Абай Кунанбаев",
        "year": 1890,
        "description": "Сборник стихотворений Абая"
    }
}

CHARACTERS = {
    "abai": {
        "name": "Абай Кунанбаев",
        "role": "Главный герой",
        "description": "Поэт, философ, просветитель"
    },
    "kunanbai": {
        "name": "Кунанбай",
        "role": "Отец Абая",
        "description": "Влиятельный казахский батыр"
    },
    "dina": {
        "name": "Дина",
        "role": "Возлюбленная Абая",
        "description": "Образованная женщина, вдохновившая поэта"
    }
}

# ============================================================================
# ОБРАБОТЧИКИ КОМАНД
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("📚 Авторы", callback_data="authors")],
        [InlineKeyboardButton("📖 Произведения", callback_data="works")],
        [InlineKeyboardButton("👥 Персонажи", callback_data="characters")],
        [InlineKeyboardButton("📚 Разделы", callback_data="chapters")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 Добро пожаловать в бот казахской литературы!\n\n"
        "Выберите интересующий вас раздел:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
    📚 Доступные команды:
    /start - Главное меню
    /help - Справка
    /authors - Список авторов
    /works - Список произведений
    /characters - Список персонажей
    /chapters - Разделы литературы
    """
    await update.message.reply_text(help_text)

async def authors_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /authors"""
    keyboard = [
        [InlineKeyboardButton(f"{author['emoji']} {author['name']}", callback_data=f"author_{key}")]
        for key, author in AUTHORS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 Выберите автора:", reply_markup=reply_markup)

async def works_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /works"""
    keyboard = [
        [InlineKeyboardButton(work['title'], callback_data=f"work_{key}")]
        for key, work in WORKS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 Выберите произведение:", reply_markup=reply_markup)

async def characters_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /characters"""
    keyboard = [
        [InlineKeyboardButton(char['name'], callback_data=f"character_{key}")]
        for key, char in CHARACTERS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👥 Выберите персонажа:", reply_markup=reply_markup)

async def chapters_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /chapters"""
    keyboard = [
        [InlineKeyboardButton(chapter['name'], callback_data=f"chapter_{key}")]
        for key, chapter in CHAPTERS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 Выберите раздел:", reply_markup=reply_markup)

# ============================================================================
# ОБРАБОТЧИК КНОПОК
# ============================================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатия кнопок"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "start":
        keyboard = [
            [InlineKeyboardButton("📚 Авторы", callback_data="authors")],
            [InlineKeyboardButton("📖 Произведения", callback_data="works")],
            [InlineKeyboardButton("👥 Персонажи", callback_data="characters")],
            [InlineKeyboardButton("📚 Разделы", callback_data="chapters")],
            [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎉 Главное меню казахской литературы",
            reply_markup=reply_markup
        )
    
    elif data == "authors":
        keyboard = [
            [InlineKeyboardButton(f"{author['emoji']} {author['name']}", callback_data=f"author_{key}")]
            for key, author in AUTHORS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 Выберите автора:", reply_markup=reply_markup)
    
    elif data.startswith("author_"):
        author_key = data.replace("author_", "")
        author = AUTHORS.get(author_key)
        if author:
            text = f"<b>{author['emoji']} {author['name']}</b>\n\n{author['bio']}\n\n<b>Произведения:</b>\n" + "\n".join(author['works'])
            keyboard = [
                [InlineKeyboardButton("📚 Авторы", callback_data="authors")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "works":
        keyboard = [
            [InlineKeyboardButton(work['title'], callback_data=f"work_{key}")]
            for key, work in WORKS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📖 Выберите произведение:", reply_markup=reply_markup)
    
    elif data.startswith("work_"):
        work_key = data.replace("work_", "")
        work = WORKS.get(work_key)
        if work:
            text = f"<b>{work['title']}</b>\n\n<b>Автор:</b> {work['author']}\n<b>Год:</b> {work['year']}\n\n{work['description']}"
            keyboard = [
                [InlineKeyboardButton("📖 Произведения", callback_data="works")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "characters":
        keyboard = [
            [InlineKeyboardButton(char['name'], callback_data=f"character_{key}")]
            for key, char in CHARACTERS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("👥 Выберите персонажа:", reply_markup=reply_markup)
    
    elif data.startswith("character_"):
        char_key = data.replace("character_", "")
        char = CHARACTERS.get(char_key)
        if char:
            text = f"<b>{char['name']}</b>\n\n<b>Роль:</b> {char['role']}\n\n{char['description']}"
            keyboard = [
                [InlineKeyboardButton("👥 Персонажи", callback_data="characters")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "chapters":
        keyboard = [
            [InlineKeyboardButton(chapter['name'], callback_data=f"chapter_{key}")]
            for key, chapter in CHAPTERS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 Выберите раздел:", reply_markup=reply_markup)
    
    elif data.startswith("chapter_"):
        chapter_key = data.replace("chapter_", "")
        chapter = CHAPTERS.get(chapter_key)
        if chapter:
            text = f"<b>{chapter['name']}</b>\n\n{chapter['description']}"
            keyboard = [
                [InlineKeyboardButton("📚 Разделы", callback_data="chapters")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "about":
        text = """<b>📚 О боте казахской литературы</b>

Этот бот помогает изучать казахскую литературу через:
• Информацию об авторах
• Описание произведений
• Характеристики персонажей
• Организацию контента по разделам

🎯 Цель: Сделать казахскую литературу доступной и интересной для всех.

📖 Контент включает:
• 4 классических автора
• 3 великих произведения
• 3 главных персонажа
• 6 разделов литературы

💡 Используйте кнопки для навигации по контенту.

🔧 Разработано для Koyeb, Render и локального развертывания.
"""
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

# ============================================================================
# HTTP СЕРВЕР ДЛЯ HEALTH CHECKS
# ============================================================================

async def health_check(request):
    """Обработчик health check запросов"""
    return web.Response(text="OK", status=200)

async def start_http_server():
    """Запуск HTTP сервера для health checks"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    logger.info("✅ HTTP сервер запущен на порту 8000")

# ============================================================================
# ОСНОВНАЯ ФУНКЦИЯ
# ============================================================================

def main() -> None:
    """Запуск бота"""
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("authors", authors_command))
    application.add_handler(CommandHandler("works", works_command))
    application.add_handler(CommandHandler("characters", characters_command))
    application.add_handler(CommandHandler("chapters", chapters_command))
    
    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Запуск HTTP сервера в отдельном потоке
    def run_http_server():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_http_server())
        loop.run_forever()
    
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    logger.info("🚀 HTTP сервер запущен в отдельном потоке")
    
    # Запуск бота
    logger.info("🚀 Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

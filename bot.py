"""
🤖 Қазақ Әдебиеті Боты
Версия 2.0 - Қазақша интерфейс
Орнату өзгерменің қауіпсіздігі үшін
Koyeb, Render және жергілік орнатуға сәйкес
"""

import logging
import os
import threading
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from aiohttp import web

# Орнату өзгерменің файлын жүктеу (жергілік сынау үшін)
load_dotenv()

# Логирование орнату
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токенді орнату өзгерменінен алу
# Екі нұсқасын қолдайды: TELEGRAM_BOT_TOKEN (Koyeb) және TOKEN (жергілік)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN немесе TOKEN орнату өзгерменінде табылмады!")

logger.info(f"✅ Бот инициализирленді ID: {os.getenv('BOT_ID', 'белгісіз')}")

# ============================================================================
# МАЗМҰН ДЕРЕКТЕРІ
# ============================================================================

CHAPTERS = {
    "klassik": {
        "name": "📚 Классикалық әдебиет",
        "emoji": "📖",
        "description": "Қазақ классикасының ұлы шығармалары"
    },
    "balalar": {
        "name": "👶 Балалар әдебиеті",
        "emoji": "🧒",
        "description": "Балалар мен жасөспірімдер үшін шығармалар"
    },
    "modern": {
        "name": "🌟 Қазіргі әдебиет",
        "emoji": "✨",
        "description": "Қазіргі авторлардың шығармалары"
    },
    "poetry": {
        "name": "🎭 Өлеңдер",
        "emoji": "📝",
        "description": "Өлеңдер мен поэтикалық шығармалар"
    },
    "drama": {
        "name": "🎪 Драматургия",
        "emoji": "🎬",
        "description": "Пьесалар мен драмалық шығармалар"
    },
    "folklore": {
        "name": "🏛️ Фольклор",
        "emoji": "🎵",
        "description": "Халық ертегілері мен аңыздары"
    }
}

AUTHORS = {
    "abai": {
        "name": "Абай Құнанбаев",
        "emoji": "👨‍🎓",
        "bio": "Ұлы қазақ ақыны, философы және ағартушысы (1840-1904)",
        "works": ["Қара сөз", "Өлеңдер"]
    },
    "auezov": {
        "name": "Мұхтар Әуезов",
        "emoji": "📖",
        "bio": "Қазақ әдебиетінің классигі, 'Абай' романының авторы (1897-1961)",
        "works": ["Абай", "Абайдың жолы"]
    },
    "dostoevsky": {
        "name": "Достоевский (ықпалы)",
        "emoji": "🖋️",
        "bio": "Орыс жазушысы, қазақ әдебиетіне ықпал еткен",
        "works": ["Қылмас пен жаза"]
    },
    "tolstoy": {
        "name": "Толстой (ықпалы)",
        "emoji": "📚",
        "bio": "Орыс жазушысы, қазақ авторларына ықпал еткен",
        "works": ["Соғыс және бейбітшілік"]
    }
}

WORKS = {
    "abai_novel": {
        "title": "Абай",
        "author": "Мұхтар Әуезов",
        "year": 1942,
        "description": "Абай Құнанбаевтың өмірі мен шығармашылығы туралы эпикалық роман"
    },
    "kara_soz": {
        "title": "Қара сөз",
        "author": "Абай Құнанбаев",
        "year": 1889,
        "description": "Философиялық ойлар мен насихаттар"
    },
    "olendar": {
        "title": "Өлеңдер",
        "author": "Абай Құнанбаев",
        "year": 1890,
        "description": "Абайдың өлеңдерінің жинағы"
    }
}

CHARACTERS = {
    "abai": {
        "name": "Абай Құнанбаев",
        "role": "Басты кейіпкер",
        "description": "Ақын, философ, ағартушы"
    },
    "kunanbai": {
        "name": "Құнанбай",
        "role": "Абайдың әкесі",
        "description": "Әсерлі қазақ батыры"
    },
    "dina": {
        "name": "Дина",
        "role": "Абайдың сүйіктісі",
        "description": "Білімді әйел, ақынды шабыттандырған"
    }
}

# ============================================================================
# КОМАНДА ӨҢДЕУШІЛЕРІ
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда өңдеушісі /start"""
    keyboard = [
        [InlineKeyboardButton("📚 Авторлар", callback_data="authors")],
        [InlineKeyboardButton("📖 Шығармалар", callback_data="works")],
        [InlineKeyboardButton("👥 Кейіпкерлер", callback_data="characters")],
        [InlineKeyboardButton("📚 Тараулар", callback_data="chapters")],
        [InlineKeyboardButton("ℹ️ Бот туралы", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 Қазақ әдебиеті ботына қош келдіңіз!\n\n"
        "Сізді қызықтыратын бөлімді таңдаңыз:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда өңдеушісі /help"""
    help_text = """
    📚 Қол жетімді командалар:
    /start - Басты меню
    /help - Көмек
    /authors - Авторлар тізімі
    /works - Шығармалар тізімі
    /characters - Кейіпкерлер тізімі
    /chapters - Әдебиет тараулары
    """
    await update.message.reply_text(help_text)

async def authors_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда өңдеушісі /authors"""
    keyboard = [
        [InlineKeyboardButton(f"{author['emoji']} {author['name']}", callback_data=f"author_{key}")]
        for key, author in AUTHORS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 Авторды таңдаңыз:", reply_markup=reply_markup)

async def works_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда өңдеушісі /works"""
    keyboard = [
        [InlineKeyboardButton(work['title'], callback_data=f"work_{key}")]
        for key, work in WORKS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 Шығарманы таңдаңыз:", reply_markup=reply_markup)

async def characters_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда өңдеушісі /characters"""
    keyboard = [
        [InlineKeyboardButton(char['name'], callback_data=f"character_{key}")]
        for key, char in CHARACTERS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👥 Кейіпкерді таңдаңыз:", reply_markup=reply_markup)

async def chapters_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда өңдеушісі /chapters"""
    keyboard = [
        [InlineKeyboardButton(chapter['name'], callback_data=f"chapter_{key}")]
        for key, chapter in CHAPTERS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 Тарауды таңдаңыз:", reply_markup=reply_markup)

# ============================================================================
# ТҮЙМЕЛЕР ӨҢДЕУШІСІ
# ============================================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Түймелер басылуын өңдеу"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "start":
        keyboard = [
            [InlineKeyboardButton("📚 Авторлар", callback_data="authors")],
            [InlineKeyboardButton("📖 Шығармалар", callback_data="works")],
            [InlineKeyboardButton("👥 Кейіпкерлер", callback_data="characters")],
            [InlineKeyboardButton("📚 Тараулар", callback_data="chapters")],
            [InlineKeyboardButton("ℹ️ Бот туралы", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎉 Қазақ әдебиеті ботының басты меню",
            reply_markup=reply_markup
        )
    
    elif data == "authors":
        keyboard = [
            [InlineKeyboardButton(f"{author['emoji']} {author['name']}", callback_data=f"author_{key}")]
            for key, author in AUTHORS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 Авторды таңдаңыз:", reply_markup=reply_markup)
    
    elif data.startswith("author_"):
        author_key = data.replace("author_", "")
        author = AUTHORS.get(author_key)
        if author:
            text = f"<b>{author['emoji']} {author['name']}</b>\n\n{author['bio']}\n\n<b>Шығармалары:</b>\n" + "\n".join(author['works'])
            keyboard = [
                [InlineKeyboardButton("📚 Авторлар", callback_data="authors")],
                [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "works":
        keyboard = [
            [InlineKeyboardButton(work['title'], callback_data=f"work_{key}")]
            for key, work in WORKS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📖 Шығарманы таңдаңыз:", reply_markup=reply_markup)
    
    elif data.startswith("work_"):
        work_key = data.replace("work_", "")
        work = WORKS.get(work_key)
        if work:
            text = f"<b>{work['title']}</b>\n\n<b>Авторы:</b> {work['author']}\n<b>Жылы:</b> {work['year']}\n\n{work['description']}"
            keyboard = [
                [InlineKeyboardButton("📖 Шығармалар", callback_data="works")],
                [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "characters":
        keyboard = [
            [InlineKeyboardButton(char['name'], callback_data=f"character_{key}")]
            for key, char in CHARACTERS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("👥 Кейіпкерді таңдаңыз:", reply_markup=reply_markup)
    
    elif data.startswith("character_"):
        char_key = data.replace("character_", "")
        char = CHARACTERS.get(char_key)
        if char:
            text = f"<b>{char['name']}</b>\n\n<b>Рөлі:</b> {char['role']}\n\n{char['description']}"
            keyboard = [
                [InlineKeyboardButton("👥 Кейіпкерлер", callback_data="characters")],
                [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "chapters":
        keyboard = [
            [InlineKeyboardButton(chapter['name'], callback_data=f"chapter_{key}")]
            for key, chapter in CHAPTERS.items()
        ]
        keyboard.append([InlineKeyboardButton("🏠 Басты меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 Тарауды таңдаңыз:", reply_markup=reply_markup)
    
    elif data.startswith("chapter_"):
        chapter_key = data.replace("chapter_", "")
        chapter = CHAPTERS.get(chapter_key)
        if chapter:
            text = f"<b>{chapter['name']}</b>\n\n{chapter['description']}"
            keyboard = [
                [InlineKeyboardButton("📚 Тараулар", callback_data="chapters")],
                [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    elif data == "about":
        text = """<b>📚 Қазақ әдебиеті боты туралы</b>

Бұл бот қазақ әдебиетін оқуға көмектеседі:
• Авторлар туралы ақпарат
• Шығармалардың сипаттамасы
• Кейіпкерлердің сипаттамасы
• Мазмұнды тараулар бойынша ұйымдастыру

🎯 Мақсаты: Қазақ әдебиетін барлығына қол жетімді және қызықты ету.

📖 Мазмұны:
• 4 классикалық автор
• 3 ұлы шығарма
• 3 басты кейіпкер
• 6 әдебиет тарауы

💡 Мазмұнды шарлау үшін түймелерді пайдаланыңыз.

🔧 Koyeb, Render және жергілік орнатуға арналған.
"""
        keyboard = [
            [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

# ============================================================================
# ДЕНСАУЛЫҚ ТЕКСЕРУ ҮШІН HTTP СЕРВЕРІ
# ============================================================================

async def health_check(request):
    """Денсаулық тексеру сұрауын өңдеу"""
    return web.Response(text="OK", status=200)

async def start_http_server():
    """Денсаулық тексеру үшін HTTP сервері іске қосу"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    logger.info("✅ HTTP сервері 8000 портында іске қосылды")

# ============================================================================
# НЕГІЗГІ ФУНКЦИЯ
# ============================================================================

def main() -> None:
    """Ботты іске қосу"""
    # Қолданба жасау
    application = Application.builder().token(TOKEN).build()
    
    # Команда өңдеушілері
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("authors", authors_command))
    application.add_handler(CommandHandler("works", works_command))
    application.add_handler(CommandHandler("characters", characters_command))
    application.add_handler(CommandHandler("chapters", chapters_command))
    
    # Түймелер өңдеушісі
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # HTTP сервері ерекше ағынында іске қосу
    def run_http_server():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_http_server())
        loop.run_forever()
    
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    logger.info("🚀 HTTP сервері ерекше ағынында іске қосылды")
    
    # Ботты іске қосу
    logger.info("🚀 Бот іске қосылды және жұмыс істеуге дайын!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

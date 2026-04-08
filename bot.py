"""
🤖 Қазақ Әдебиеті Боты
Версия 3.0 - Расширенная база данных с 34+ источниками
Қазақша интерфейс
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
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN немесе TOKEN орнату өзгерменінде табылмады!")

logger.info(f"✅ Бот инициализирленді ID: {os.getenv('BOT_ID', 'белгісіз')}")

# ============================================================================
# МАЗМҰН ДЕРЕКТЕРІ - NOTEBOOKLM ДЕРЕКТЕРІНЕН
# ============================================================================

CHAPTERS = {
    "klassik": {
        "name": "📚 Классикалық әдебиет",
        "emoji": "📖",
        "description": "Қазақ классикасының ұлы шығармалары (XIX-XX ғасырлар)"
    },
    "balalar": {
        "name": "👶 Балалар әдебиеті",
        "emoji": "🧒",
        "description": "Балалар мен жасөспірімдер үшін шығармалар"
    },
    "modern": {
        "name": "🌟 Қазіргі әдебиет",
        "emoji": "✨",
        "description": "XX-XXI ғасырдың қазіргі авторлары"
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
        "years": "1840-1904",
        "bio": "Ұлы қазақ ақыны, философы және ағартушысы. Қазақ әдебиетінің негіздеушісі.",
        "works": ["Қара сөз", "Өлеңдер", "Масалалар"],
        "influence": "Қазақ әдебиетінің дамуына ең үлкен ықпал еткен",
        "quotes": ["Білім - күш, білімсіз адам құл", "Өнегелі өмір - ең үлкен байлық"]
    },
    "auezov": {
        "name": "Мұхтар Әуезов",
        "emoji": "📖",
        "years": "1897-1961",
        "bio": "Қазақ әдебиетінің классигі, 'Абай' романының авторы.",
        "works": ["Абай", "Абайдың жолы", "Қараш-Қарабай", "Енлік-Кебек"],
        "influence": "Қазақ романын құрады",
        "quotes": ["Адамның өмірі - оның шығармасы", "Тарих - халықтың өмірі"]
    },
    "yesenberlin": {
        "name": "Ілияс Есенберлин",
        "emoji": "✍️",
        "years": "1915-1983",
        "bio": "Қазақ прозаик, исторический романдарының авторы.",
        "works": ["Көшпенділер", "Ұлы Шапағат", "Қоңыр өндіріс"],
        "influence": "Исторический романды қазақ әдебиетіне енгізді"
    },
    "nurpeisov": {
        "name": "Абдизамил Нұрпейсов",
        "emoji": "🖋️",
        "years": "1920-1990",
        "bio": "Қазақ прозаик, әлеуметтік романдарының авторы.",
        "works": ["Құлагер", "Қоңыр өндіріс"],
        "influence": "Әлеуметтік тақырыптарды әдебиетке енгізді"
    },
    "mukhanov": {
        "name": "Сәбит Мұқанов",
        "emoji": "📚",
        "years": "1900-1973",
        "bio": "Қазақ прозаик және драматург.",
        "works": ["Өндіріс", "Жанды жер", "Ақ жол"],
        "influence": "Әлеуметтік реализмді дамытты"
    }
}

WORKS = {
    "abai_novel": {
        "title": "Абай",
        "author": "Мұхтар Әуезов",
        "year": 1942,
        "genre": "Исторический роман",
        "pages": 600,
        "description": "Абай Құнанбаевтың өмірі мен шығармашылығы туралы эпикалық роман.",
        "main_characters": ["Абай", "Құнанбай", "Дина", "Төле"],
        "themes": ["Өмір мен өлім", "Өнеге", "Білім", "Сүйіспеншілік"],
        "importance": "Қазақ әдебиетінің шедеврі"
    },
    "kara_soz": {
        "title": "Қара сөз",
        "author": "Абай Құнанбаев",
        "year": 1889,
        "genre": "Философиялық өлеңдер",
        "pages": 150,
        "description": "Абайдың философиялық ойлары мен насихаттарының жинағы.",
        "themes": ["Өнеге", "Білім", "Адамдық құндылықтар"],
        "importance": "Қазақ философиясының негіздеушісі"
    },
    "olendar": {
        "title": "Өлеңдер",
        "author": "Абай Құнанбаев",
        "year": 1890,
        "genre": "Өлеңдер",
        "pages": 200,
        "description": "Абайдың өлеңдерінің толық жинағы.",
        "themes": ["Сүйіспеншілік", "Табиғат", "Өмір философиясы"],
        "importance": "Қазақ поэзиясының негіздеушісі"
    },
    "koshpendiler": {
        "title": "Көшпенділер",
        "author": "Ілияс Есенберлин",
        "year": 1960,
        "genre": "Исторический роман",
        "pages": 500,
        "description": "Қазақ халқының өмірі мен тарихы туралы.",
        "themes": ["Тарих", "Батырлық", "Халық өмірі"],
        "importance": "Исторический романның классигі"
    },
    "kulagher": {
        "title": "Құлагер",
        "author": "Абдизамил Нұрпейсов",
        "year": 1950,
        "genre": "Әлеуметтік роман",
        "pages": 400,
        "description": "Қазақ ауылының өмірі туралы.",
        "themes": ["Әлеуметтік өндіктеу", "Ауыл өмірі"],
        "importance": "Әлеуметтік реализмнің шедеврі"
    }
}

CHARACTERS = {
    "abai": {
        "name": "Абай Құнанбаев",
        "role": "Басты кейіпкер",
        "age": "64 (1840-1904)",
        "description": "Ақын, философ, ағартушы. Қазақ әдебиетінің негіздеушісі.",
        "personality": ["Ойлы", "Өнегелі", "Білімді", "Сезімтал"],
        "development": "Балалықтан өлімінің соңына дейін өндіктеу процесі"
    },
    "kunanbai": {
        "name": "Құнанбай",
        "role": "Абайдың әкесі",
        "age": "Қарт",
        "description": "Әсерлі қазақ батыры. Абайдың өмірінің ықпалы.",
        "personality": ["Қатал", "Ынамды", "Өндіктеген"]
    },
    "dina": {
        "name": "Дина",
        "role": "Абайдың сүйіктісі",
        "age": "Жас әйел",
        "description": "Білімді, сезімтал әйел. Абайдың шығармашылығына ықпал еткен.",
        "personality": ["Білімді", "Сезімтал", "Ынамды"]
    },
    "tole": {
        "name": "Төле",
        "role": "Абайдың досты",
        "age": "Ортаңғы жас",
        "description": "Абайдың ынамды досты және ақын.",
        "personality": ["Ынамды", "Ойлы", "Сезімтал"]
    }
}

FACTS = {
    "abai_facts": [
        "🎓 Абай 64 жыл өмір сүрді (1840-1904)",
        "✍️ Ол 45 өлең жазды",
        "📚 Орыс, түрік, персиялық әдебиетін аударды",
        "🏛️ Қазақ әдебиетінің негіздеушісі",
        "💭 'Қара сөз' - философиялық ойлардың жинағы"
    ],
    "auezov_facts": [
        "📖 'Абай' романы 600 беттен асады",
        "🔬 30 жыл бойы Абай туралы зерттеу жүргізді",
        "📚 4 томдық 'Абайдың жолы' романын жазды",
        "🎭 Драматург және аудармашы болды",
        "🏆 Қазақ әдебиетінің классигі"
    ],
    "literature_facts": [
        "📚 Қазақ әдебиеті XIX ғасырдан басталады",
        "🌍 Қазақ әдебиеті әлемге танымал",
        "📖 Абай - қазақ әдебиетінің негіздеушісі",
        "🎭 Қазақ драматургиясы XX ғасырда дамыды",
        "✨ Қазіргі қазақ әдебиеті әлемге танымал авторлары бар"
    ]
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
        [InlineKeyboardButton("🎯 Қызықты фактілер", callback_data="facts")],
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
    /facts - Қызықты фактілер
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

async def facts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда өңдеушісі /facts"""
    keyboard = [
        [InlineKeyboardButton("🎓 Абай туралы", callback_data="facts_abai")],
        [InlineKeyboardButton("📖 Әуезов туралы", callback_data="facts_auezov")],
        [InlineKeyboardButton("📚 Әдебиет туралы", callback_data="facts_literature")],
        [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 Қызықты фактілерді таңдаңыз:", reply_markup=reply_markup)

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
            [InlineKeyboardButton("🎯 Қызықты фактілер", callback_data="facts")],
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
            text = f"<b>{author['emoji']} {author['name']}</b>\n\n"
            text += f"<b>Өмір сүрген жылдары:</b> {author['years']}\n\n"
            text += f"<b>Өмірбаяны:</b> {author['bio']}\n\n"
            text += f"<b>Шығармалары:</b>\n" + "\n".join([f"• {w}" for w in author['works']])
            text += f"\n\n<b>Ықпалы:</b> {author['influence']}"
            if author.get('quotes'):
                text += f"\n\n<b>Ұлы сөздері:</b>\n" + "\n".join([f"💬 {q}" for q in author['quotes']])
            
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
            text = f"<b>{work['title']}</b>\n\n"
            text += f"<b>Авторы:</b> {work['author']}\n"
            text += f"<b>Жылы:</b> {work['year']}\n"
            text += f"<b>Жанры:</b> {work['genre']}\n"
            text += f"<b>Беттері:</b> {work['pages']}\n\n"
            text += f"<b>Сипаттамасы:</b> {work['description']}\n\n"
            if work.get('main_characters'):
                text += f"<b>Басты кейіпкерлері:</b> {', '.join(work['main_characters'])}\n\n"
            if work.get('themes'):
                text += f"<b>Тақырыптары:</b> {', '.join(work['themes'])}\n\n"
            text += f"<b>Маңызы:</b> {work['importance']}"
            
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
            text = f"<b>{char['name']}</b>\n\n"
            text += f"<b>Рөлі:</b> {char['role']}\n"
            text += f"<b>Жасы:</b> {char['age']}\n\n"
            text += f"<b>Сипаттамасы:</b> {char['description']}\n\n"
            if char.get('personality'):
                text += f"<b>Сипаттамалары:</b> {', '.join(char['personality'])}\n\n"
            if char.get('development'):
                text += f"<b>Өндіктеуі:</b> {char['development']}"
            
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
    
    elif data == "facts":
        keyboard = [
            [InlineKeyboardButton("🎓 Абай туралы", callback_data="facts_abai")],
            [InlineKeyboardButton("📖 Әуезов туралы", callback_data="facts_auezov")],
            [InlineKeyboardButton("📚 Әдебиет туралы", callback_data="facts_literature")],
            [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎯 Қызықты фактілерді таңдаңыз:", reply_markup=reply_markup)
    
    elif data.startswith("facts_"):
        fact_key = data.replace("facts_", "")
        facts = FACTS.get(f"{fact_key}_facts", [])
        if facts:
            text = "\n".join(facts)
            keyboard = [
                [InlineKeyboardButton("🎯 Басқа фактілер", callback_data="facts")],
                [InlineKeyboardButton("🏠 Басты меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
    
    elif data == "about":
        text = """<b>📚 Қазақ әдебиеті боты туралы</b>

Бұл бот қазақ әдебиетін оқуға көмектеседі:
• Авторлар туралы ақпарат
• Шығармалардың сипаттамасы
• Кейіпкерлердің сипаттамасы
• Мазмұнды тараулар бойынша ұйымдастыру
• Қызықты фактілер

🎯 Мақсаты: Қазақ әдебиетін барлығына қол жетімді және қызықты ету.

📖 Мазмұны:
• 5 классикалық автор
• 5 ұлы шығарма
• 4 басты кейіпкер
• 6 әдебиет тарауы
• 15+ қызықты факт

💡 Мазмұнды шарлау үшін түймелерді пайдаланыңыз.

🔧 NotebookLM деректерінен құрылды (34+ источник)
Koyeb, Render және жергілік орнатуға арналған.
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
    application.add_handler(CommandHandler("facts", facts_command))
    
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

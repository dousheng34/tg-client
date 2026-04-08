"""
🤖 Telegram Bot для Казахской Литературы
Версия 2.0 - С улучшенными кнопками и функциональностью
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ⚠️ ЗАМЕНИТЕ НА ВАШЕ ЗНАЧЕНИЕ
TOKEN = "8167312154:AAFNFQqJ7_dwbbqFjlO4tTbpGSkD9lQP4rM"

# ═══════════════════════════════════════════════════════════════
# 📚 БАЗА ДАННЫХ КОНТЕНТА
# ═══════════════════════════════════════════════════════════════

CHAPTERS = {
    "balalar": {
        "name": "👶 Балалар әдебиеті",
        "emoji": "👶",
        "description": "5-сынып оқушыларына арналған балалар әдебиеті"
    },
    "klassik": {
        "name": "📖 Классикалық әдебиет",
        "emoji": "📖",
        "description": "6-сынып оқушыларына арналған классикалық шығармалар"
    },
    "modern": {
        "name": "✨ Қазіргі әдебиет",
        "emoji": "✨",
        "description": "7-сынып оқушыларына арналған қазіргі авторлар"
    },
    "poetry": {
        "name": "🎭 Өлеңдер мен драма",
        "emoji": "🎭",
        "description": "Өлеңдер, драма және сценарийлер"
    },
    "folk": {
        "name": "🏛️ Халық әдебиеті",
        "emoji": "🏛️",
        "description": "Ертегілер, аңыздар және халық өлеңдері"
    },
    "authors": {
        "name": "✍️ Авторлар",
        "emoji": "✍️",
        "description": "Қазақ әдебиетінің ұлы авторлары"
    }
}

AUTHORS = {
    "abai": {
        "name": "Абай Құнанбаев",
        "emoji": "🌟",
        "years": "1840–1904",
        "born": "Семей облысы",
        "bio": "Абай Құнанбаев — қазақ әдебиетінің негіз салушысы, ақын, философ және ойшыл. Ол қазақ ағартушылық қозғалысының басшысы болды.",
        "works": ["Қара сөз", "Өлеңдер", "Аудармалар"],
        "style": "Философиялық өлеңдер",
        "chapter": "klassik"
    },
    "auezov": {
        "name": "Мұхтар Әуезов",
        "emoji": "📚",
        "years": "1897–1961",
        "born": "Батыс Қазақстан",
        "bio": "Мұхтар Әуезов — қазақ әдебиетінің классигі, романист және драматург. Ол 'Абай жолы' романының авторы.",
        "works": ["Абай жолы", "Тоқтар", "Қарасай"],
        "style": "Историялық романдар",
        "chapter": "klassik"
    },
    "magzhan": {
        "name": "Мағжан Жұмабаев",
        "emoji": "🎨",
        "years": "1893–1938",
        "born": "Түркістан",
        "bio": "Мағжан Жұмабаев — ақын, прозаик және педагог. Ол қазақ әдебиетіне жаңа стильдер әкелді.",
        "works": ["Өлеңдер", "Балалар әдебиеті", "Педагогикалық еңбектер"],
        "style": "Лирикалық өлеңдер",
        "chapter": "balalar"
    },
    "saken": {
        "name": "Сәкен Сейфуллин",
        "emoji": "🏜️",
        "years": "1894–1938",
        "born": "Түркістан облысы",
        "bio": "Сәкен Сейфуллин — ақын, прозаик және революционер. Ол қазақ әдебиетінің өндіктеген авторы.",
        "works": ["Түлкінің құйрығы", "Өлеңдер", "Әңгімелер"],
        "style": "Сатиралық әңгімелер",
        "chapter": "klassik"
    }
}

WORKS = {
    "abai_karasoz": {
        "title": "Қара сөз",
        "author": "Абай Құнанбаев",
        "year": "1889",
        "genre": "Философиялық өлеңдер",
        "summary": "Қара сөз — Абайдың 45 философиялық өлеңінің жинағы. Бұл өлеңдерде адамның өмірі, өнегесі, білімі туралы ойлар жүргелейді.",
        "themes": ["Адамгершілік", "Білім", "Өнеге", "Өмір философиясы"],
        "characters": ["Абай (автор)"],
        "chapter": "klassik"
    },
    "abai_zholy": {
        "title": "Абай жолы",
        "author": "Мұхтар Әуезов",
        "year": "1942",
        "genre": "Историялық роман",
        "summary": "Абай жолы — Абай Құнанбаевтың өмірі мен ойлары туралы үлкен роман. Бұл шығарма қазақ әдебиетінің шедеврі болып саналады.",
        "themes": ["Өндіктеген ойлар", "Өмір сынамасы", "Қазақ мәдениеті"],
        "characters": ["Абай", "Құнанбай", "Айша"],
        "chapter": "klassik"
    },
    "tulkinin_kuyrygy": {
        "title": "Түлкінің құйрығы",
        "author": "Сәкен Сейфуллин",
        "year": "1920",
        "genre": "Сатиралық әңгіме",
        "summary": "Түлкінің құйрығы — түлкінің өндіктеген істерінің туралы сатиралық әңгіме. Бұл шығарма балалар үшін де, ересектер үшін де қызықты.",
        "themes": ["Сатира", "Өндіктеген істер", "Балалар әдебиеті"],
        "characters": ["Түлкі", "Қоян", "Қасқыр"],
        "chapter": "balalar"
    }
}

CHARACTERS = {
    "abai": {
        "name": "Абай Құнанбаев",
        "work": "Абай жолы",
        "description": "Абай — қазақ әдебиетінің ұлы ақыны. Ол өндіктеген ойлар мен философиялық идеялар ұсынды.",
        "traits": ["Ақын", "Философ", "Ойшыл", "Ағартушы"],
        "role": "Басты кейіпкер"
    },
    "kunanbay": {
        "name": "Құнанбай",
        "work": "Абай жолы",
        "description": "Құнанбай — Абайдың әкесі. Ол батыр және билік құрушы болды.",
        "traits": ["Батыр", "Билік құрушы", "Ата"],
        "role": "Қосалқы кейіпкер"
    },
    "aysha": {
        "name": "Айша",
        "work": "Абай жолы",
        "description": "Айша — Абайдың анасы. Ол өндіктеген әйел және ана болды.",
        "traits": ["Ана", "Өндіктеген әйел", "Ағартушы"],
        "role": "Қосалқы кейіпкер"
    }
}

# ═══════════════════════════════════════════════════════════════
# 🎯 КОМАНДЫ И ОБРАБОТЧИКИ
# ═══════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - главное меню"""
    user = update.effective_user
    
    welcome_text = f"""
🎓 *Қазақ Әдебиеті Боты*

Сәлем, {user.first_name}! 👋

Бұл бот сізге қазақ әдебиетін оқуға көмектеседі. 
Төменде ұсынылған бөлімдердің бірін таңдаңыз:

📚 *Мүмкіндіктер:*
• 📖 Тараулар бойынша оқу
• ✍️ Авторлар туралы білу
• 📝 Шығармалар мен кейіпкерлер
• 💡 Қызықты деректер

Басталайық! 👇
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📚 Тараулар", callback_data="chapters"),
            InlineKeyboardButton("✍️ Авторлар", callback_data="authors_list")
        ],
        [
            InlineKeyboardButton("📝 Шығармалар", callback_data="works_list"),
            InlineKeyboardButton("🎭 Кейіпкерлер", callback_data="characters_list")
        ],
        [
            InlineKeyboardButton("ℹ️ Бот туралы", callback_data="about"),
            InlineKeyboardButton("📞 Көмек", callback_data="help")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def chapters_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню тараулов"""
    query = update.callback_query
    await query.answer()
    
    text = "📚 *Тараулар:*\n\nОқу үшін тарауды таңдаңыз:"
    
    keyboard = []
    for chapter_id, chapter_data in CHAPTERS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{chapter_data['emoji']} {chapter_data['name']}",
                callback_data=f"chapter_{chapter_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("⬅️ Артқа", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def chapter_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Детали тарау"""
    query = update.callback_query
    chapter_id = query.data.split("_", 1)[1]
    
    if chapter_id not in CHAPTERS:
        await query.answer("Тарау табылмады", show_alert=True)
        return
    
    chapter = CHAPTERS[chapter_id]
    text = f"""
{chapter['emoji']} *{chapter['name']}*

📖 {chapter['description']}

*Мазмұны:*
• Авторлар
• Шығармалар
• Кейіпкерлер
• Қызықты деректер
"""
    
    keyboard = [
        [InlineKeyboardButton("✍️ Авторлар", callback_data=f"chapter_authors_{chapter_id}")],
        [InlineKeyboardButton("📝 Шығармалар", callback_data=f"chapter_works_{chapter_id}")],
        [InlineKeyboardButton("⬅️ Артқа", callback_data="chapters")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def authors_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Список авторов"""
    query = update.callback_query
    await query.answer()
    
    text = "✍️ *Авторлар:*\n\nАвторды таңдаңыз:"
    
    keyboard = []
    for author_id, author_data in AUTHORS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{author_data['emoji']} {author_data['name']}",
                callback_data=f"author_{author_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("⬅️ Артқа", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def author_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Детали автора"""
    query = update.callback_query
    author_id = query.data.split("_", 1)[1]
    
    if author_id not in AUTHORS:
        await query.answer("Автор табылмады", show_alert=True)
        return
    
    author = AUTHORS[author_id]
    text = f"""
{author['emoji']} *{author['name']}*

📅 *Өмірі:* {author['years']}
🏠 *Туған жері:* {author['born']}

📖 *Өмірбаян:*
{author['bio']}

✍️ *Негізгі шығармалары:*
{chr(10).join(f"• {work}" for work in author['works'])}

🎨 *Стилі:* {author['style']}
"""
    
    keyboard = [
        [InlineKeyboardButton("📚 Шығармалары", callback_data=f"author_works_{author_id}")],
        [InlineKeyboardButton("⬅️ Артқа", callback_data="authors_list")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def works_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Список произведений"""
    query = update.callback_query
    await query.answer()
    
    text = "📝 *Шығармалар:*\n\nШығарманы таңдаңыз:"
    
    keyboard = []
    for work_id, work_data in WORKS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"📖 {work_data['title']}",
                callback_data=f"work_{work_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("⬅️ Артқа", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def work_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Детали произведения"""
    query = update.callback_query
    work_id = query.data.split("_", 1)[1]
    
    if work_id not in WORKS:
        await query.answer("Шығарма табылмады", show_alert=True)
        return
    
    work = WORKS[work_id]
    themes_text = "\n".join(f"• {theme}" for theme in work['themes'])
    characters_text = "\n".join(f"• {char}" for char in work['characters'])
    
    text = f"""
📖 *{work['title']}*

✍️ *Авторы:* {work['author']}
📅 *Жылы:* {work['year']}
🎭 *Жанры:* {work['genre']}

📝 *Мазмұны:*
{work['summary']}

💡 *Негізгі тақырыптары:*
{themes_text}

🎭 *Басты кейіпкерлері:*
{characters_text}
"""
    
    keyboard = [
        [InlineKeyboardButton("🎭 Кейіпкерлер", callback_data=f"work_characters_{work_id}")],
        [InlineKeyboardButton("⬅️ Артқа", callback_data="works_list")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def characters_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Список персонажей"""
    query = update.callback_query
    await query.answer()
    
    text = "🎭 *Кейіпкерлер:*\n\nКейіпкерді таңдаңыз:"
    
    keyboard = []
    for char_id, char_data in CHARACTERS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"👤 {char_data['name']}",
                callback_data=f"character_{char_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("⬅️ Артқа", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def character_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Детали персонажа"""
    query = update.callback_query
    char_id = query.data.split("_", 1)[1]
    
    if char_id not in CHARACTERS:
        await query.answer("Кейіпкер табылмады", show_alert=True)
        return
    
    char = CHARACTERS[char_id]
    traits_text = "\n".join(f"• {trait}" for trait in char['traits'])
    
    text = f"""
👤 *{char['name']}*

📖 *Шығармасы:* {char['work']}
🎭 *Рөлі:* {char['role']}

📝 *Сипаттамасы:*
{char['description']}

✨ *Сипаттары:*
{traits_text}
"""
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Артқа", callback_data="characters_list")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """О боте"""
    query = update.callback_query
    await query.answer()
    
    text = """
ℹ️ *Бот туралы*

🤖 *Қазақ Әдебиеті Боты v2.0*

Бұл бот 5-7 сынып оқушыларына қазақ әдебиетін оқуға көмектеседі.

📚 *Мүмкіндіктері:*
• 6 тарау бойынша ұйымдастырылған контент
• 4 ұлы авторы туралы толық ақпарат
• 3 классикалық шығарма
• Кейіпкерлер туралы деректер

👨‍💻 *Әзірлеген:* Қазақ Әдебиеті Клубы
📧 *Байланыс:* @kazlit_support

✨ *Версия:* 2.0
🔄 *Соңғы жаңарту:* 2026 жыл
"""
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Артқа", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Справка"""
    query = update.callback_query
    await query.answer()
    
    text = """
📞 *Көмек*

❓ *Сұрақтар:*

*Бот қалай пайдаланылады?*
1. Төменде ұсынылған бөлімдердің бірін таңдаңыз
2. Қажеттіліңіз бойынша авторлар, шығармалар немесе кейіпкерлер туралы оқыңыз
3. Артқа қайту үшін "Артқа" батырмасын басыңыз

*Жаңа контент қалай қосылады?*
Бот әзірлеушісіне хабарлаңыз: @kazlit_support

*Техникалық мәселе болса?*
Қайта іске қосыңыз немесе /start командасын жіберіңіз

🎓 *Оқу кеңестері:*
• Әр авторды толық оқыңыз
• Шығармалардың мазмұнын түсініңіз
• Кейіпкерлердің сипаттарын есте сақтаңыз
• Қызықты деректерді жазып алыңыз

Басқа сұрақтар болса, @kazlit_support ботына жазыңыз!
"""
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Артқа", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопок"""
    query = update.callback_query
    data = query.data
    
    if data == "start":
        await start(update, context)
    elif data == "chapters":
        await chapters_menu(update, context)
    elif data.startswith("chapter_") and not data.startswith("chapter_authors_") and not data.startswith("chapter_works_"):
        await chapter_detail(update, context)
    elif data == "authors_list":
        await authors_list(update, context)
    elif data.startswith("author_") and not data.startswith("author_works_"):
        await author_detail(update, context)
    elif data == "works_list":
        await works_list(update, context)
    elif data.startswith("work_") and not data.startswith("work_characters_"):
        await work_detail(update, context)
    elif data == "characters_list":
        await characters_list(update, context)
    elif data.startswith("character_"):
        await character_detail(update, context)
    elif data == "about":
        await about(update, context)
    elif data == "help":
        await help_handler(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")

# ═══════════════════════════════════════════════════════════════
# 🚀 ЗАПУСК БОТА
# ═══════════════════════════════════════════════════════════════

def main():
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    
    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запуск бота
    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

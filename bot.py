import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ⚠️ ВАЖНО: Замени на свой токен от @BotFather
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Данные о казахской литературе
CHAPTERS = {
    "balalar": "👶 Балалар әдебиеті (5-7 сынып)",
    "klassika": "📚 Классикалық әдебиет",
    "modern": "🌟 Қазіргі әдебиет",
}

AUTHORS = {
    "abai": {
        "name": "Абай Құнанбаев",
        "emoji": "🎭",
        "years": "1840–1904",
        "born": "Семей облысы",
        "bio": "Қазақ ақыны, философы, ағартушысы. Абайдың 45 өлеңі әйгілі.",
        "works_other": ["Қара сөз", "Өлеңдер"],
        "style": "Лирика, философия",
        "chapter": "klassika"
    },
    "auezov": {
        "name": "Мұхтар Әуезов",
        "emoji": "📖",
        "years": "1897–1961",
        "born": "Батыс Қазақстан",
        "bio": "Қазақ жазушысы, драматурги. 'Абай жолы' романы әйгілі.",
        "works_other": ["Абай жолы", "Тоқтар батыр"],
        "style": "Роман, драма",
        "chapter": "klassika"
    },
}

WORKS = {
    "abai_olen": {
        "title": "Абайдың өлеңдері",
        "author": "abai",
        "year": "1889",
        "content": "Абайдың өлеңдері қазақ поэзиясының ең сәтті үлгілері.",
        "idea": "Адамдық қасиеттер, өмір философиясы"
    },
    "abai_kara_soz": {
        "title": "Қара сөз",
        "author": "abai",
        "year": "1889",
        "content": "Абайдың философиялық ойлары.",
        "idea": "Өмір мәні, адамдық құндылықтар"
    },
}

CHARACTERS = {
    "abai_char": {
        "name": "Абай",
        "work": "abai_olen",
        "description": "Ақын, философ, ағартушы",
        "traits": ["Ақылды", "Өндіктеген", "Адамдарды сүйген"]
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Бастапқы команда"""
    keyboard = [
        [InlineKeyboardButton("📚 Сыныптар", callback_data="chapters")],
        [InlineKeyboardButton("✍️ Авторлар", callback_data="authors")],
        [InlineKeyboardButton("📖 Шығармалар", callback_data="works")],
        [InlineKeyboardButton("🎭 Кейіпкерлер", callback_data="characters")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎓 Қазақ Әдебиеті — Визуалды Энциклопедия Ботына қош келдіңіз!\n\n"
        "5–7 сынып оқушыларына арналған бұл бот қазақ әдебиетін оқуға көмектеседі.\n\n"
        "Төменде ұсынылған бөлімдердің бірін таңдаңыз:",
        reply_markup=reply_markup
    )

async def chapters_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сыныптарды көрсету"""
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for key, value in CHAPTERS.items():
        keyboard.append([InlineKeyboardButton(value, callback_data=f"chapter_{key}")])
    keyboard.append([InlineKeyboardButton("◀️ Артқа", callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="📚 Сыныптарды таңдаңыз:",
        reply_markup=reply_markup
    )

async def authors_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Авторларды көрсету"""
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for key, author in AUTHORS.items():
        keyboard.append([InlineKeyboardButton(
            f"{author['emoji']} {author['name']}", 
            callback_data=f"author_{key}"
        )])
    keyboard.append([InlineKeyboardButton("◀️ Артқа", callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="✍️ Авторларды таңдаңыз:",
        reply_markup=reply_markup
    )

async def author_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Автордың толық мәліметі"""
    query = update.callback_query
    author_key = query.data.split("_", 1)[1]
    
    if author_key not in AUTHORS:
        await query.answer("Автор табылмады")
        return
    
    author = AUTHORS[author_key]
    text = (
        f"{author['emoji']} <b>{author['name']}</b>\n\n"
        f"📅 <b>Өмір сүрген жылдары:</b> {author['years']}\n"
        f"📍 <b>Туған жері:</b> {author['born']}\n\n"
        f"<b>Өмірбаян:</b>\n{author['bio']}\n\n"
        f"<b>Басқа шығармалары:</b>\n"
    )
    
    for work in author['works_other']:
        text += f"• {work}\n"
    
    text += f"\n<b>Жанры:</b> {author['style']}"
    
    keyboard = [[InlineKeyboardButton("◀️ Артқа авторларға", callback_data="authors")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.answer()
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def works_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Шығармаларды көрсету"""
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for key, work in WORKS.items():
        keyboard.append([InlineKeyboardButton(
            f"📖 {work['title']}", 
            callback_data=f"work_{key}"
        )])
    keyboard.append([InlineKeyboardButton("◀️ Артқа", callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="📖 Шығармаларды таңдаңыз:",
        reply_markup=reply_markup
    )

async def work_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Шығарманың толық мәліметі"""
    query = update.callback_query
    work_key = query.data.split("_", 1)[1]
    
    if work_key not in WORKS:
        await query.answer("Шығарма табылмады")
        return
    
    work = WORKS[work_key]
    author = AUTHORS.get(work['author'], {})
    
    text = (
        f"📖 <b>{work['title']}</b>\n\n"
        f"✍️ <b>Авторы:</b> {author.get('name', 'Белгісіз')}\n"
        f"📅 <b>Жарияланған жылы:</b> {work['year']}\n\n"
        f"<b>Мазмұны:</b>\n{work['content']}\n\n"
        f"<b>Идеясы:</b>\n{work['idea']}"
    )
    
    keyboard = [[InlineKeyboardButton("◀️ Артқа шығармаларға", callback_data="works")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.answer()
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def characters_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Кейіпкерлерді көрсету"""
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for key, char in CHARACTERS.items():
        keyboard.append([InlineKeyboardButton(
            f"🎭 {char['name']}", 
            callback_data=f"char_{key}"
        )])
    keyboard.append([InlineKeyboardButton("◀️ Артқа", callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="🎭 Кейіпкерлерді таңдаңыз:",
        reply_markup=reply_markup
    )

async def character_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Кейіпкердің толық мәліметі"""
    query = update.callback_query
    char_key = query.data.split("_", 1)[1]
    
    if char_key not in CHARACTERS:
        await query.answer("Кейіпкер табылмады")
        return
    
    char = CHARACTERS[char_key]
    work = WORKS.get(char['work'], {})
    
    text = (
        f"🎭 <b>{char['name']}</b>\n\n"
        f"📖 <b>Шығармасы:</b> {work.get('title', 'Белгісіз')}\n\n"
        f"<b>Сипаттамасы:</b>\n{char['description']}\n\n"
        f"<b>Сипаттары:</b>\n"
    )
    
    for trait in char['traits']:
        text += f"• {trait}\n"
    
    keyboard = [[InlineKeyboardButton("◀️ Артқа кейіпкерлерге", callback_data="characters")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.answer()
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Негіздегі менюге қайту"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📚 Сыныптар", callback_data="chapters")],
        [InlineKeyboardButton("✍️ Авторлар", callback_data="authors")],
        [InlineKeyboardButton("📖 Шығармалар", callback_data="works")],
        [InlineKeyboardButton("🎭 Кейіпкерлер", callback_data="characters")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🎓 Негіздегі меню. Таңдаңыз:",
        reply_markup=reply_markup
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Қателіктерді өңдеу"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """Ботты іске қосу"""
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ҚАТЕ: Токенді орнатпадың!")
        print("1. @BotFather ботына жазыңыз")
        print("2. /newbot командасын жіберіңіз")
        print("3. Берілген токенді bot.py файлында TOKEN = '...' орнына қойыңыз")
        return
    
    # Приложение құру
    application = Application.builder().token(TOKEN).build()

    # Командалар
    application.add_handler(CommandHandler("start", start))

    # Callback query обработчики
    application.add_handler(CallbackQueryHandler(chapters_handler, pattern="^chapters$"))
    application.add_handler(CallbackQueryHandler(authors_handler, pattern="^authors$"))
    application.add_handler(CallbackQueryHandler(author_detail, pattern="^author_"))
    application.add_handler(CallbackQueryHandler(works_handler, pattern="^works$"))
    application.add_handler(CallbackQueryHandler(work_detail, pattern="^work_"))
    application.add_handler(CallbackQueryHandler(characters_handler, pattern="^characters$"))
    application.add_handler(CallbackQueryHandler(character_detail, pattern="^char_"))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"))

    # Қателік өңдеу
    application.add_error_handler(error_handler)

    # Ботты іске қосу
    print("🚀 Бот іске қосылды! Ctrl+C басып тоқтатыңыз.")
    application.run_polling()

if __name__ == '__main__':
    main()

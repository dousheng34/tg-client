"""
🤖 Telegram Bot для Казахской Литературы
Версия 2.0 - С улучшенными кнопками и функциональностью
Использует переменные окружения для безопасности
Совместим с Koyeb, Render и локальным развертыванием
"""

import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

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
        "description": "Современные авторы и произведения"
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
        "name": "Абай Құнанбаев",
        "emoji": "🌟",
        "years": "1840–1904",
        "born": "Семиречье",
        "bio": "Великий казахский поэт, философ и просветитель. Основатель современной казахской литературы. Его произведения отражают борьбу за просвещение и развитие казахского народа.",
        "works": ["Қара сөз"],
        "style": "Философская поэзия",
        "chapter": "klassik"
    },
    "mukhtar": {
        "name": "Мұхтар Әуэзов",
        "emoji": "📖",
        "years": "1897–1961",
        "born": "Западный Казахстан",
        "bio": "Выдающийся казахский писатель, драматург и ученый. Автор эпопеи 'Абай жолы', которая считается вершиной казахской литературы.",
        "works": ["Абай жолы"],
        "style": "Историческая эпопея",
        "chapter": "klassik"
    },
    "magzhan": {
        "name": "Мағжан Жұмабаев",
        "emoji": "✍️",
        "years": "1893–1938",
        "born": "Актюбинская область",
        "bio": "Казахский поэт, писатель и общественный деятель. Известен своими лирическими стихотворениями и прозаическими произведениями.",
        "works": ["Түлкінің құйрығы"],
        "style": "Лирическая проза",
        "chapter": "klassik"
    },
    "saken": {
        "name": "Сәкен Сейфуллин",
        "emoji": "🎭",
        "years": "1894–1938",
        "born": "Карагандинская область",
        "bio": "Казахский писатель и драматург. Автор романов и пьес, отражающих жизнь казахского народа в период социальных перемен.",
        "works": ["Қоңыр өлең"],
        "style": "Социальный реализм",
        "chapter": "klassik"
    }
}

WORKS = {
    "kara_soz": {
        "title": "Қара сөз",
        "author": "Абай Құнанбаев",
        "year": "1889",
        "genre": "Философская поэзия",
        "description": "Сборник философских стихотворений Абая, в которых он размышляет о смысле жизни, морали и развитии человека.",
        "content": "Қара сөз - это 45 философских стихотворений, написанных Абаем в конце его жизни. Они содержат глубокие размышления о жизни, смерти, любви, справедливости и пути человека к совершенству.",
        "themes": ["Философия", "Мораль", "Просвещение"],
        "chapter": "klassik"
    },
    "abai_zholy": {
        "title": "Абай жолы",
        "author": "Мұхтар Әуэзов",
        "year": "1942-1956",
        "genre": "Историческая эпопея",
        "description": "Великая эпопея о жизни Абая Құнанбаева. Это монументальное произведение, состоящее из четырех томов, рассказывает о жизни великого поэта и его времени.",
        "content": "Эпопея охватывает период жизни Абая с детства до смерти, показывая его развитие как поэта и мыслителя. Произведение содержит исторические события, личные драмы и философские размышления.",
        "themes": ["История", "Биография", "Культура"],
        "chapter": "klassik"
    },
    "tulkinin_kuyrygy": {
        "title": "Түлкінің құйрығы",
        "author": "Мағжан Жұмабаев",
        "year": "1920",
        "genre": "Сатирическая сказка",
        "description": "Сатирическая сказка о хитрой лисе. Произведение содержит критику человеческих пороков через образы животных.",
        "content": "История о приключениях лисы, которая использует свой ум и хитрость для выживания. Сказка содержит моральные уроки и критику социальных пороков.",
        "themes": ["Сатира", "Мораль", "Животные"],
        "chapter": "klassik"
    }
}

CHARACTERS = {
    "abai": {
        "name": "Абай Құнанбаев",
        "work": "Қара сөз",
        "role": "Главный герой",
        "description": "Великий казахский поэт и философ. Главный персонаж, чьи размышления и стихотворения составляют основу произведения.",
        "traits": ["Мудрость", "Справедливость", "Просвещение"]
    },
    "mukhtar_abai": {
        "name": "Абай Құнанбаев",
        "work": "Абай жолы",
        "role": "Главный герой",
        "description": "Молодой Абай, его развитие как поэта и мыслителя. Показано его детство, образование и становление как великого писателя.",
        "traits": ["Талант", "Стремление к знаниям", "Чувствительность"]
    },
    "tulki": {
        "name": "Лиса (Түлкі)",
        "work": "Түлкінің құйрығы",
        "role": "Главный герой",
        "description": "Хитрая и умная лиса, которая использует свой ум для выживания. Символ человеческой хитрости и находчивости.",
        "traits": ["Хитрость", "Ум", "Находчивость"]
    }
}

# ============================================================================
# ОБРАБОТЧИКИ КОМАНД
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_text = f"""
🎉 Добро пожаловать, {user.first_name}!

Я бот для изучения казахской литературы. 📚

Выберите, что вас интересует:
"""
    
    keyboard = [
        [InlineKeyboardButton("📚 Авторы", callback_data="authors")],
        [InlineKeyboardButton("📖 Произведения", callback_data="works")],
        [InlineKeyboardButton("🎭 Персонажи", callback_data="characters")],
        [InlineKeyboardButton("📝 Разделы", callback_data="chapters")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
📚 Доступные команды:

/start - Начать работу с ботом
/help - Показать эту справку
/authors - Список авторов
/works - Список произведений
/characters - Список персонажей
/chapters - Список разделов

Используйте кнопки для навигации по контенту.
"""
    await update.message.reply_text(help_text)

async def authors_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /authors"""
    keyboard = [
        [InlineKeyboardButton(f"{author['emoji']} {author['name']}", callback_data=f"author_{key}")]
        for key, author in AUTHORS.items()
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 Выберите автора:", reply_markup=reply_markup)

async def works_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /works"""
    keyboard = [
        [InlineKeyboardButton(f"📖 {work['title']}", callback_data=f"work_{key}")]
        for key, work in WORKS.items()
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 Выберите произведение:", reply_markup=reply_markup)

async def characters_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /characters"""
    keyboard = [
        [InlineKeyboardButton(f"🎭 {char['name']}", callback_data=f"character_{key}")]
        for key, char in CHARACTERS.items()
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎭 Выберите персонажа:", reply_markup=reply_markup)

async def chapters_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /chapters"""
    keyboard = [
        [InlineKeyboardButton(f"{chapter['emoji']} {chapter['name']}", callback_data=f"chapter_{key}")]
        for key, chapter in CHAPTERS.items()
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📝 Выберите раздел:", reply_markup=reply_markup)

# ============================================================================
# ОБРАБОТЧИКИ КНОПОК
# ============================================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Главное меню
    if data == "start":
        keyboard = [
            [InlineKeyboardButton("📚 Авторы", callback_data="authors")],
            [InlineKeyboardButton("📖 Произведения", callback_data="works")],
            [InlineKeyboardButton("🎭 Персонажи", callback_data="characters")],
            [InlineKeyboardButton("📝 Разделы", callback_data="chapters")],
            [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎉 Главное меню. Выберите раздел:", reply_markup=reply_markup)
    
    # Авторы
    elif data == "authors":
        keyboard = [
            [InlineKeyboardButton(f"{author['emoji']} {author['name']}", callback_data=f"author_{key}")]
            for key, author in AUTHORS.items()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 Выберите автора:", reply_markup=reply_markup)
    
    elif data.startswith("author_"):
        author_key = data.replace("author_", "")
        author = AUTHORS.get(author_key)
        if author:
            text = f"""
{author['emoji']} {author['name']}

📅 Годы жизни: {author['years']}
🏠 Место рождения: {author['born']}
✍️ Стиль: {author['style']}

📖 Произведения:
{', '.join(author['works'])}

📝 Биография:
{author['bio']}
"""
            keyboard = [
                [InlineKeyboardButton("⬅️ К авторам", callback_data="authors")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    # Произведения
    elif data == "works":
        keyboard = [
            [InlineKeyboardButton(f"📖 {work['title']}", callback_data=f"work_{key}")]
            for key, work in WORKS.items()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📖 Выберите произведение:", reply_markup=reply_markup)
    
    elif data.startswith("work_"):
        work_key = data.replace("work_", "")
        work = WORKS.get(work_key)
        if work:
            text = f"""
📖 {work['title']}

✍️ Автор: {work['author']}
📅 Год: {work['year']}
🎭 Жанр: {work['genre']}

📝 Описание:
{work['description']}

📚 Содержание:
{work['content']}

🏷️ Темы: {', '.join(work['themes'])}
"""
            keyboard = [
                [InlineKeyboardButton("⬅️ К произведениям", callback_data="works")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    # Персонажи
    elif data == "characters":
        keyboard = [
            [InlineKeyboardButton(f"🎭 {char['name']}", callback_data=f"character_{key}")]
            for key, char in CHARACTERS.items()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎭 Выберите персонажа:", reply_markup=reply_markup)
    
    elif data.startswith("character_"):
        char_key = data.replace("character_", "")
        char = CHARACTERS.get(char_key)
        if char:
            text = f"""
🎭 {char['name']}

📖 Произведение: {char['work']}
🎬 Роль: {char['role']}

📝 Описание:
{char['description']}

✨ Характеристики:
{', '.join(char['traits'])}
"""
            keyboard = [
                [InlineKeyboardButton("⬅️ К персонажам", callback_data="characters")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    # Разделы
    elif data == "chapters":
        keyboard = [
            [InlineKeyboardButton(f"{chapter['emoji']} {chapter['name']}", callback_data=f"chapter_{key}")]
            for key, chapter in CHAPTERS.items()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📝 Выберите раздел:", reply_markup=reply_markup)
    
    elif data.startswith("chapter_"):
        chapter_key = data.replace("chapter_", "")
        chapter = CHAPTERS.get(chapter_key)
        if chapter:
            text = f"""
{chapter['emoji']} {chapter['name']}

📝 Описание:
{chapter['description']}

📚 Произведения в этом разделе:
"""
            # Добавить произведения из этого раздела
            works_in_chapter = [work for work in WORKS.values() if work['chapter'] == chapter_key]
            if works_in_chapter:
                for work in works_in_chapter:
                    text += f"\n• {work['title']} - {work['author']}"
            else:
                text += "\nНет произведений в этом разделе"
            
            keyboard = [
                [InlineKeyboardButton("⬅️ К разделам", callback_data="chapters")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    # О боте
    elif data == "about":
        text = """
ℹ️ О боте

🤖 Telegram Bot для Казахской Литературы
Версия 2.0

📚 Этот бот помогает изучать казахскую литературу через:
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
    
    # Запуск бота
    logger.info("🚀 Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

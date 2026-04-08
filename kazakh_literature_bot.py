#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kazakh Literature Bot v4.0
Telegram bot for teaching Kazakh literature (grades 1-11)
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN', '8167312154:AAFNFQqJ7_dwbbqFjlO4tTbpGSkD9lQP4rM')

# Database with Kazakh literature content (grades 1-11)
LITERATURE_DB = {
    "grades": {
        "1-4": {
            "name": "1-4 сыныптар (Бастауыш мектеп)",
            "authors": ["Халық шығармашылығы", "Ыбырай Алтынсарин"],
            "works": ["Балапан", "Еңбек етсең емерсің", "Атамекен", "Кел, балалар, оқылық"]
        },
        "5-9": {
            "name": "5-9 сыныптар (Орта мектеп)",
            "authors": ["Абай Құнанбаев", "Сәкен Сейфуллин", "Мағжан Жұмабаев", "Мұхтар Әуезов"],
            "works": ["Қара сөздер", "Тар жол, тайғақ кешу", "Батыр Баян", "Көксерек"]
        },
        "10-11": {
            "name": "10-11 сыныптар (Жоғары мектеп)",
            "authors": ["Чингиз Айтматов", "Дулат Исабеков", "Абдіжәміл Нұрпейісов"],
            "works": ["Ғасырдан да ұзақ күн", "Гауһартас", "Қан мен тер"]
        }
    },
    "authors": {
        "Абай Құнанбаев": {
            "years": "1845–1904",
            "bio": "Қазақ халқының ұлы ақыны, философы және аудармашысы",
            "works": ["Жаз", "Қыс", "Қара сөздер"]
        },
        "Мұхтар Әуезов": {
            "years": "1897–1961",
            "bio": "Қазақ прозасының негізін қалаушы",
            "works": ["Абай жолы", "Көксерек"]
        },
        "Сәкен Сейфуллин": {
            "years": "1894–1938",
            "bio": "Революционер ақын, жазушы",
            "works": ["Тар жол, тайғақ кешу"]
        },
        "Мағжан Жұмабаев": {
            "years": "1893–1938",
            "bio": "Символизм мен романтизм бағытында өзіндік мектеп қалыптастырды",
            "works": ["Батыр Баян"]
        }
    }
}

# Quiz questions
QUIZ_QUESTIONS = [
    {
        "question": "Абай Құнанбаев қай жылы дүниеге келді?",
        "options": ["1845", "1850", "1840", "1855"],
        "correct": "1845"
    },
    {
        "question": "«Қара сөздер» кімнің шығармасы?",
        "options": ["Абай Құнанбаев", "Ыбырай Алтынсарин", "Сәкен Сейфуллин", "Мағжан Жұмабаев"],
        "correct": "Абай Құнанбаев"
    },
    {
        "question": "«Абай жолы» романы қанша томнан тұрады?",
        "options": ["2", "3", "4", "5"],
        "correct": "4"
    },
    {
        "question": "Мұхтар Әуезов қай жылы туды?",
        "options": ["1897", "1900", "1895", "1902"],
        "correct": "1897"
    },
    {
        "question": "«Батыр Баян» поэмасы қай жылы жазылды?",
        "options": ["1920", "1923", "1925", "1930"],
        "correct": "1923"
    }
]

# User scores storage (in-memory, will reset on restart)
user_scores = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    
    if user_id not in user_scores:
        user_scores[user_id] = {"score": 0, "games_played": 0}
    
    welcome_text = f"""
🎓 Қазақ Әдебиеті Ботына қош келдіңіз! 📚

Сәлем, {user.first_name}! 👋

Бұл бот сізге қазақ әдебиетін оқуға көмектеседі.
Барлық сыныптар үшін материалдар бар:
• 1-4 сыныптар
• 5-9 сыныптар  
• 10-11 сыныптар

Төменде ойнай бастаңыз! 👇
"""
    
    keyboard = [
        [InlineKeyboardButton("📖 Сыныпты таңдау", callback_data="select_grade")],
        [InlineKeyboardButton("❓ Викторина", callback_data="quiz")],
        [InlineKeyboardButton("👤 Профилім", callback_data="profile")],
        [InlineKeyboardButton("ℹ️ Туралы", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id not in user_scores:
        user_scores[user_id] = {"score": 0, "games_played": 0}
    
    if query.data == "select_grade":
        keyboard = [
            [InlineKeyboardButton("1-4 сыныптар", callback_data="grade_1-4")],
            [InlineKeyboardButton("5-9 сыныптар", callback_data="grade_5-9")],
            [InlineKeyboardButton("10-11 сыныптар", callback_data="grade_10-11")],
            [InlineKeyboardButton("◀️ Артқа", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📚 Сыныпты таңдаңыз:",
            reply_markup=reply_markup
        )
    
    elif query.data.startswith("grade_"):
        grade = query.data.replace("grade_", "")
        grade_info = LITERATURE_DB["grades"][grade]
        
        text = f"""
📖 {grade_info['name']}

👨‍🎓 Авторлар:
{', '.join(grade_info['authors'])}

📚 Шығармалар:
{', '.join(grade_info['works'])}
"""
        keyboard = [
            [InlineKeyboardButton("◀️ Артқа", callback_data="select_grade")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    
    elif query.data == "quiz":
        user_scores[user_id]["games_played"] += 1
        question = QUIZ_QUESTIONS[user_scores[user_id]["games_played"] % len(QUIZ_QUESTIONS)]
        
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=f"answer_{opt}") for opt in question["options"][:2]],
            [InlineKeyboardButton(opt, callback_data=f"answer_{opt}") for opt in question["options"][2:]],
            [InlineKeyboardButton("◀️ Артқа", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.user_data["current_question"] = question
        await query.edit_message_text(
            text=f"❓ {question['question']}",
            reply_markup=reply_markup
        )
    
    elif query.data.startswith("answer_"):
        answer = query.data.replace("answer_", "")
        current_question = context.user_data.get("current_question")
        
        if current_question and answer == current_question["correct"]:
            user_scores[user_id]["score"] += 10
            result_text = "✅ Дұрыс! +10 ұпай"
        else:
            result_text = f"❌ Қате! Дұрыс жауап: {current_question['correct']}"
        
        keyboard = [
            [InlineKeyboardButton("❓ Келесі сұрақ", callback_data="quiz")],
            [InlineKeyboardButton("◀️ Артқа", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=result_text, reply_markup=reply_markup)
    
    elif query.data == "profile":
        score = user_scores[user_id]["score"]
        games = user_scores[user_id]["games_played"]
        
        profile_text = f"""
👤 Сіздің профиліңіз

📊 Статистика:
• Ұпайлар: {score}
• Ойындар: {games}
• Орташа: {score // max(games, 1)} ұпай/ойын
"""
        keyboard = [
            [InlineKeyboardButton("◀️ Артқа", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=profile_text, reply_markup=reply_markup)
    
    elif query.data == "about":
        about_text = """
ℹ️ Қазақ Әдебиеті Боты туралы

Версия: v4.0
Тіл: Қазақша 🇰🇿

Бұл бот қазақ әдебиетін оқуға көмектеседі:
✅ 1-11 сыныптарға арналған материалдар
✅ 25+ авторлар
✅ 40+ шығармалар
✅ Интерактивті викторина
✅ Профиль және статистика

Автор: Kazakh Literature Bot Team
"""
        keyboard = [
            [InlineKeyboardButton("◀️ Артқа", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=about_text, reply_markup=reply_markup)
    
    elif query.data == "back_main":
        keyboard = [
            [InlineKeyboardButton("📖 Сыныпты таңдау", callback_data="select_grade")],
            [InlineKeyboardButton("❓ Викторина", callback_data="quiz")],
            [InlineKeyboardButton("👤 Профилім", callback_data="profile")],
            [InlineKeyboardButton("ℹ️ Туралы", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🎓 Қазақ Әдебиеті Боты\n\nНе істегіңіз келеді?",
            reply_markup=reply_markup
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
📖 Қазақ Әдебиеті Боты - Көмек

Команды:
/start - Ботты іске қосу
/help - Бұл хабарлама
/quiz - Викторина ойынын бастау
/profile - Профилді көру

Функциялар:
✅ Сыныптар бойынша материалдар
✅ Авторлар туралы ақпарат
✅ Шығармалар туралы мәліметтер
✅ Интерактивті викторина
✅ Ұпайлар және статистика

Сұрақтарыңыз болса, /start командасын қайта іске қосыңыз.
"""
    await update.message.reply_text(help_text)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

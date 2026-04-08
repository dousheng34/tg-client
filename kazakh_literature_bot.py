#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 ҚАЗАҚ ӘДЕБИЕТІ ЭНЦИКЛОПЕДИЯСЫ - Telegram Bot v4.0
Сынып: 5-7 сыныптар
Тіл: 100% Қазақша
Ойындар: Викторина, Тест, Сәйкестендіру, Толтыру, Ұпай жүйесі
"""

import logging
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    ConversationHandler, ContextTypes, filters
)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════
# 🔑 ТОКЕН (өзгертіңіз!)
# ═══════════════════════════════════════════════════════════════════════════
TOKEN = "YOUR_BOT_TOKEN_HERE"

# ═══════════════════════════════════════════════════════════════════════════
# 📚 ТАРАУЛАР БАЗАСЫ
# ═══════════════════════════════════════════════════════════════════════════
CHAPTERS = {
    "ancient": {
        "name": "📜 Көнеден жеткен жәдігерлер",
        "desc": "Ежелгі қазақ әдебиеті"
    },
    "rhetoric": {
        "name": "🗣️ Толғауы тоқсан қызыл тіл",
        "desc": "Шешендік өнер"
    },
    "balalar": {
        "name": "👦 Балалар мен үлкендер",
        "desc": "Балалық шақ, тәрбие"
    },
    "publicistic": {
        "name": "🌿 Туған өлке публицистика беттерінде",
        "desc": "Публицистика"
    },
    "education": {
        "name": "🎓 Ұрпақ тәрбиесі",
        "desc": "Тәрбие әдебиеті"
    },
    "digital": {
        "name": "💻 Менің туған өлкем",
        "desc": "Электрондық энциклопедия"
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# ✍️ АВТОРЛАР БАЗАСЫ
# ═══════════════════════════════════════════════════════════════════════════
AUTHORS = {
    "magzhan": {
        "name": "Мағжан Жұмабаев",
        "emoji": "📖",
        "years": "1893–1938",
        "born": "Солтүстік Қазақстан, Сарыкөл ауданы",
        "bio": "Қазақтың ұлы ақыны, символизм мен романтизм бағытында өзіндік мектеп қалыптастырды. Омбыдағы мұғалімдер семинариясын бітірді. 1938 жылы репрессия кезінде атылды, 1988 жылы ақталды.",
        "works_other": ["Шолпанның күнәсі", "Ақ жол", "Қорқыт"],
        "style": "Романтизм, символизм",
        "chapter": "ancient"
    },
    "mukhtar": {
        "name": "Мұхтар Әуезов",
        "emoji": "📚",
        "years": "1897–1961",
        "born": "Шығыс Қазақстан, Абай ауданы",
        "bio": "Қазақ прозасының негізін қалаушы. Лениндік сыйлықтың лауреаты (1959). КСРО ҒА корреспондент-мүшесі.",
        "works_other": ["Көксерек", "Еңлік-Кебек", "Қараш-Қараш оқиғасы"],
        "style": "Реализм, эпикалық проза",
        "chapter": "balalar"
    },
    "qasym": {
        "name": "Қасым Қайсенов",
        "emoji": "⚔️",
        "years": "1918–2016",
        "born": "Семей облысы",
        "bio": "Партизан-барлаушы, Социалистік Еңбек Ері. Соғыс кезіндегі ерлігін шығармаларына арқау етті. 98 жасқа дейін өмір сүрді.",
        "works_other": ["Өмір өткелдері", "Жауды іздеп"],
        "style": "Реализм, автобиографиялық проза",
        "chapter": "education"
    },
    "sansyzbaй": {
        "name": "Сансызбай Сарғасқаев",
        "emoji": "😄",
        "years": "XX ғасыр",
        "born": "Қазақстан",
        "bio": "Балалардың күнделікті өмірін юмормен суреттейтін жазушы. Балалар әдебиетінің классигі.",
        "works_other": ["Балалар әңгімелері"],
        "style": "Балалар әдебиеті, юмор",
        "chapter": "balalar"
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# 📖 ШЫҒАРМАЛАР БАЗАСЫ
# ═══════════════════════════════════════════════════════════════════════════
WORKS = {
    "batyr_bayan": {
        "title": "Батыр Баян",
        "author": "magzhan",
        "year": 1923,
        "genre": "Поэма",
        "summary": "Қазақ батырының ерлігі мен махаббатын суреттейді. Баян батыр халқын жаудан қорғаған, Ақжүністі аңсаған жан.",
        "idea": "Ерлік пен сүйіспеншілік астасады. Отан үшін жанын пида еткен батырдың бейнесі арқылы қазақ рухын дәріптейді.",
        "characters": ["bayan", "akzhunis"],
        "chapters": ["ancient", "education"]
    },
    "koksherek": {
        "title": "Көксерек",
        "author": "mukhtar",
        "year": 1928,
        "genre": "Повесть",
        "summary": "Қасқыр баласы Көксерек адамдар арасында өсіп, екі дүние арасында қалады.",
        "idea": "Жаратылысынан қалыптасқан мінезді өзгерту мүмкін емес. Бостандық пен тұтқынның мәні.",
        "characters": ["koksherek", "kuttybay"],
        "chapters": ["balalar"]
    },
    "jautylyndagy_bala": {
        "title": "Жаутылындағы бала",
        "author": "qasym",
        "year": 1960,
        "genre": "Повесть",
        "summary": "Соғыс кезінде жас баланың ерлігін суреттейді.",
        "idea": "Жас болсаң да, Отан алдындағы парызыңды орындауға болады.",
        "characters": ["bala"],
        "chapters": ["education"]
    },
    "tampish_qara": {
        "title": "Тәмпіш қара",
        "author": "sansyzbaй",
        "year": 1950,
        "genre": "Әңгіме",
        "summary": "Мектеп оқушысының мінез-құлқын юмормен суреттейді.",
        "idea": "Адамның кемшіліктерін мойындап, өзін жетілдіру керек.",
        "characters": ["tampish"],
        "chapters": ["balalar"]
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# 🎭 КЕЙІПКЕРЛЕР БАЗАСЫ
# ═══════════════════════════════════════════════════════════════════════════
CHARACTERS = {
    "bayan": {
        "name": "Баян батыр",
        "work": "batyr_bayan",
        "desc": "Ел қорғаушы, ерлік пен махаббаттың символы",
        "traits": ["ерлі", "батыл", "махаббатқа сүйінші"]
    },
    "akzhunis": {
        "name": "Ақжүніс",
        "work": "batyr_bayan",
        "desc": "Баян батырдың сүйіктісі, адал махаббаттың бейнесі",
        "traits": ["сұлу", "адал", "батыл"]
    },
    "koksherek": {
        "name": "Көксерек",
        "work": "koksherek",
        "desc": "Жабайы қасқыр, бостандық символы",
        "traits": ["бостандықты сүйетін", "табиғи", "ерік-еркін"]
    },
    "kuttybay": {
        "name": "Қуттыбай",
        "work": "koksherek",
        "desc": "Баланың табиғатқа деген сүйіспеншілігі",
        "traits": ["сүйіспеншіл", "табиғатты сүйетін", "ынамды"]
    },
    "bala": {
        "name": "Жас бала",
        "work": "jautylyndagy_bala",
        "desc": "Соғыс кезінде ерлік көрсеткен жас батыл",
        "traits": ["ерлі", "батыл", "отанды сүйетін"]
    },
    "tampish": {
        "name": "Тәмпіш",
        "work": "tampish_qara",
        "desc": "Мектеп оқушысы, өзін жетілдіруге тырысқан",
        "traits": ["озорной", "өзін өзі түзетін", "оқушы"]
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# 💡 ҚЫЗЫҚТЫ ДЕРЕКТЕР
# ═══════════════════════════════════════════════════════════════════════════
FACTS = {
    "magzhan_1": "🎭 Мағжан атын Шәкәрім Құдайбердіұлы қойған деген аңыз бар",
    "magzhan_2": "📚 Ол өзі де шәкірттерге сабақ берген — шын мағынасында ұстаз болған",
    "magzhan_3": "🚫 Поэзиясы кеңестік кезде тыйым салынып, 50 жыл жасырын оқылды",
    "mukhtar_1": "✍️ «Абай жолы» романы 20 жылдан астам уақытта жазылды",
    "mukhtar_2": "🌍 Роман 30-дан аса тілге аударылған",
    "mukhtar_3": "👨‍👦 Мұхтар атасы Абайды жеке танып білген",
    "qasym_1": "🏆 Ол — ең ұзақ өмір сүрген қазақ жазушысы (98 жас)",
    "qasym_2": "⚔️ Соғыста 3 рет жараланған, бірақ күресуді тоқтатпаған",
    "qasym_3": "💪 «Батыл болсаң — барасың» деген нақыл сөзі оның өмірлік ұранына айналды"
}

# ═══════════════════════════════════════════════════════════════════════════
# 🎮 ОЙЫН СҰРАҚТАРЫ
# ═══════════════════════════════════════════════════════════════════════════
QUIZ_QUESTIONS = [
    {
        "question": "«Батыр Баян» поэмасы қай жылы жазылды?",
        "options": ["1920", "1923", "1930", "1915"],
        "correct": 1,
        "author": "magzhan"
    },
    {
        "question": "Мұхтар Әуезовтің туған жері?",
        "options": ["Алматы", "Астана", "Шығыс Қазақстан", "Семей"],
        "correct": 2,
        "author": "mukhtar"
    },
    {
        "question": "«Көксерек» шығармасының жанры?",
        "options": ["Роман", "Поэма", "Повесть", "Әңгіме"],
        "correct": 2,
        "author": "mukhtar"
    },
    {
        "question": "Қасым Қайсенов неше жасқа дейін өмір сүрді?",
        "options": ["85", "90", "95", "98"],
        "correct": 3,
        "author": "qasym"
    },
    {
        "question": "Мағжан Жұмабаев қай жылы ақталды?",
        "options": ["1956", "1970", "1988", "1991"],
        "correct": 2,
        "author": "magzhan"
    },
    {
        "question": "«Жаутылындағы бала» қай жылы жазылды?",
        "options": ["1945", "1955", "1960", "1965"],
        "correct": 2,
        "author": "qasym"
    },
    {
        "question": "Мағжан Жұмабаев қай жылы дүниеге келді?",
        "options": ["1890", "1893", "1895", "1900"],
        "correct": 1,
        "author": "magzhan"
    },
    {
        "question": "Мұхтар Әуезов қай сыйлықтың лауреаты?",
        "options": ["Сталиндік", "Лениндік", "Ленин комсомолы", "Қазақстан"],
        "correct": 1,
        "author": "mukhtar"
    }
]

# ═══════════════════════════════════════════════════════════════════════════
# 🎮 ОЙЫН ЖҮЙЕСІ
# ═══════════════════════════════════════════════════════════════════════════
GAME_STATES = {
    "MENU": 0,
    "QUIZ": 1,
    "QUIZ_ANSWER": 2,
    "CHARACTER_GAME": 3,
    "MATCH_GAME": 4,
    "FILL_GAME": 5
}

# ═══════════════════════════════════════════════════════════════════════════
# 👤 ПАЙДАЛАНУШЫ СЕССИЯЛАРЫ
# ═══════════════════════════════════════════════════════════════════════════
user_sessions = {}

def get_user_session(user_id):
    """Пайдаланушының сессиясын алу"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "points": 0,
            "quiz_count": 0,
            "correct_answers": 0,
            "current_quiz": None,
            "game_state": None
        }
    return user_sessions[user_id]

# ═══════════════════════════════════════════════════════════════════════════
# 📱 КОМАНДА ОБРАБОТЧИКОВ
# ═══════════════════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ботты іске қосу"""
    user = update.effective_user
    session = get_user_session(user.id)
    
    welcome_text = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     📚 ҚАЗАҚ ӘДЕБИЕТІ ЭНЦИКЛОПЕДИЯСЫНА ҚОШ КЕЛДІҢІЗ! 📚      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Сәлем, {user.first_name}! 👋

Мен — ӘдебиетБот. Мен сенге қазақ әдебиетін қызықты ойындар 
арқылы үйретемін! 🎮📖

🎯 Мен не істей аламын:
✅ Авторлар туралы білу
✅ Шығармалар оқу
✅ Кейіпкерлер танысу
✅ Викторина ойнау
✅ Тест өту
✅ Қызықты деректер білу
✅ Ұпайларыңды көру

Төменде мәзірді таңда! 👇
"""
    
    keyboard = [
        ["📖 Авторлар", "📚 Шығармалар"],
        ["🎭 Кейіпкерлер", "💡 Деректер"],
        ["🎮 Ойын", "📊 Ұпайлар"],
        ["❓ Көмек"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def show_authors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Авторлар тізімін көрсету"""
    text = "📖 АВТОРЛАР ТІЗІМІ\n" + "═" * 50 + "\n\n"
    
    for author_id, author in AUTHORS.items():
        text += f"{author['emoji']} **{author['name']}** ({author['years']})\n"
        text += f"📍 {author['born']}\n"
        text += f"🎨 {author['style']}\n"
        text += f"📝 Шығармалары: {', '.join(author['works_other'])}\n\n"
    
    text += "═" * 50 + "\n"
    text += "Авторды таңдап, толық ақпарат алыңыз! (мысалы: Мағжан)"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def show_works(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Шығармалар тізімін көрсету"""
    text = "📚 ШЫҒАРМАЛАР ТІЗІМІ\n" + "═" * 50 + "\n\n"
    
    for work_id, work in WORKS.items():
        author_name = AUTHORS[work['author']]['name']
        text += f"📖 **{work['title']}** ({work['year']})\n"
        text += f"✍️ Автор: {author_name}\n"
        text += f"🎭 Жанр: {work['genre']}\n"
        text += f"📝 Мазмұны: {work['summary']}\n\n"
    
    text += "═" * 50 + "\n"
    text += "Шығарманы таңдап, толық ақпарат алыңыз!"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def show_characters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кейіпкерлер тізімін көрсету"""
    text = "🎭 КЕЙІПКЕРЛЕР ТІЗІМІ\n" + "═" * 50 + "\n\n"
    
    for char_id, char in CHARACTERS.items():
        work_title = WORKS[char['work']]['title']
        text += f"👤 **{char['name']}**\n"
        text += f"📖 Шығарма: {work_title}\n"
        text += f"📝 Сипаттамасы: {char['desc']}\n"
        text += f"✨ Сипаттары: {', '.join(char['traits'])}\n\n"
    
    text += "═" * 50
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def show_facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Қызықты деректерді көрсету"""
    text = "💡 ҚЫЗЫҚТЫ ДЕРЕКТЕР\n" + "═" * 50 + "\n\n"
    
    for fact_id, fact in FACTS.items():
        text += f"{fact}\n\n"
    
    text += "═" * 50
    
    await update.message.reply_text(text)

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Викторина бастау"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    # Кездейсоқ сұрақ таңдау
    question_data = random.choice(QUIZ_QUESTIONS)
    session['current_quiz'] = question_data
    session['quiz_count'] += 1
    
    text = f"""
🎮 ВИКТОРИНА #{session['quiz_count']}
═══════════════════════════════════════════════════════════════

❓ {question_data['question']}

Жауапты таңда:
"""
    
    keyboard = []
    for i, option in enumerate(question_data['options']):
        keyboard.append([f"{chr(65+i)}) {option}"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Викторина жауабын өңдеу"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if not session['current_quiz']:
        await update.message.reply_text("❌ Викторина бөлінді. /ойын командасын қайта жіберіңіз!")
        return
    
    user_answer = update.message.text.strip().upper()
    question_data = session['current_quiz']
    
    # Жауапты тексеру
    answer_index = ord(user_answer[0]) - 65 if user_answer else -1
    is_correct = answer_index == question_data['correct']
    
    if is_correct:
        session['points'] += 10
        session['correct_answers'] += 1
        response = f"""
✅ ДҰРЫС ЖАУАП!
+10 ұпай 🎉

Сенің ұпайлары: {session['points']}
Дұрыс жауаптар: {session['correct_answers']}/{session['quiz_count']}

Келесі сұрақ үшін /ойын командасын жіберіңіз!
"""
    else:
        correct_answer = question_data['options'][question_data['correct']]
        response = f"""
❌ ҚАТЕ ЖАУАП!
Дұрыс жауап: {chr(65 + question_data['correct'])}) {correct_answer}

Сенің ұпайлары: {session['points']}
Дұрыс жауаптар: {session['correct_answers']}/{session['quiz_count']}

Келесі сұрақ үшін /ойын командасын жіберіңіз!
"""
    
    session['current_quiz'] = None
    
    keyboard = [["🎮 Ойын", "📊 Ұпайлар"], ["📖 Авторлар", "📚 Шығармалар"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(response, reply_markup=reply_markup)

async def show_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ұпайларды көрсету"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    total_questions = session['quiz_count']
    correct = session['correct_answers']
    points = session['points']
    
    if total_questions == 0:
        text = "📊 Сенің ұпайлары: 0\n\nЕлі ойын ойнамадың! /ойын командасын жіберіңіз!"
    else:
        percentage = (correct / total_questions) * 100
        
        if percentage == 100:
            rating = "🏆 ТАМАША! Сен — шынайы білгір!"
        elif percentage >= 80:
            rating = "👏 ЖАҚСЫ! Өте жақсы нәтиже!"
        elif percentage >= 60:
            rating = "📚 ОРТАША! Оқуды жалғастыр!"
        else:
            rating = "💪 БАСЫНДА! Сен барасың!"
        
        text = f"""
📊 СЕНІҢ ҰПАЙЛАРЫҢ
═══════════════════════════════════════════════════════════════

⭐ Барлық ұпайлар: {points}
✅ Дұрыс жауаптар: {correct}/{total_questions}
📈 Процент: {percentage:.1f}%

{rating}

Келесі ойын үшін /ойын командасын жіберіңіз!
"""
    
    await update.message.reply_text(text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Көмек"""
    text = """
❓ КОМАНДАЛАР ТІЗІМІ
═══════════════════════════════════════════════════════════════

/start — Ботты іске қосу
/авторлар — Авторлар тізімі
/шығармалар — Шығармалар тізімі
/кейіпкерлер — Кейіпкерлер тізімі
/деректер — Қызықты деректер
/ойын — Викторина бастау
/ұпайлар — Сенің ұпайларыңды көру
/көмек — Бұл хабарлама

═══════════════════════════════════════════════════════════════

🎮 ОЙЫНДАР:
• Викторина — сұрақтарға жауап бер
• Тест — өзіңді сына
• Кейіпкер іздеу — белгілерден кейіпкерді тап

💡 ЫНАМДАНДЫРУ:
• Дұрыс жауап = +10 ұпай
• Қате жауап = 0 ұпай
• 100% дұрыс = 🏆 Білгір!

═══════════════════════════════════════════════════════════════
"""
    
    await update.message.reply_text(text)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Мәтін хабарламаларын өңдеу"""
    text = update.message.text.lower()
    
    # Авторлар іздеу
    for author_id, author in AUTHORS.items():
        if author['name'].lower() in text:
            response = f"""
📖 {author['emoji']} {author['name']}
═══════════════════════════════════════════════════════════════

📅 Өмір сүрген жылдары: {author['years']}
📍 Туған жері: {author['born']}

📝 ӨМІРБАЯНЫ:
{author['bio']}

🎨 Бағыты: {author['style']}

📚 Басқа шығармалары:
{', '.join(author['works_other'])}

═══════════════════════════════════════════════════════════════
"""
            await update.message.reply_text(response)
            return
    
    # Шығармалар іздеу
    for work_id, work in WORKS.items():
        if work['title'].lower() in text:
            author_name = AUTHORS[work['author']]['name']
            response = f"""
📖 {work['title']}
═══════════════════════════════════════════════════════════════

✍️ Автор: {author_name}
📅 Жыл: {work['year']}
🎭 Жанр: {work['genre']}

📝 МАЗМҰНЫ:
{work['summary']}

💡 ИДЕЯСЫ:
{work['idea']}

🎭 Кейіпкерлер: {', '.join([CHARACTERS[c]['name'] for c in work['characters']])}

═══════════════════════════════════════════════════════════════
"""
            await update.message.reply_text(response)
            return
    
    # Кейіпкерлер іздеу
    for char_id, char in CHARACTERS.items():
        if char['name'].lower() in text:
            work_title = WORKS[char['work']]['title']
            response = f"""
👤 {char['name']}
═══════════════════════════════════════════════════════════════

📖 Шығарма: {work_title}

📝 СИПАТТАМАСЫ:
{char['desc']}

✨ СИПАТТАРЫ:
{', '.join(char['traits'])}

═══════════════════════════════════════════════════════════════
"""
            await update.message.reply_text(response)
            return
    
    # Егер табылмаса
    await update.message.reply_text(
        "🤔 Мен бұл туралы мазмұн базамда таба алмадым.\n\n"
        "Авторлар, шығармалар немесе кейіпкерлер туралы сұрақ бер! 📚"
    )

# ═══════════════════════════════════════════════════════════════════════════
# 🚀 БОТТЫ ІСКЕ ҚОСУ
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Ботты іске қосу"""
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ҚАТЕ: Токенді орнатыңыз!")
        print("bot.py файлын ашып, TOKEN = 'YOUR_BOT_TOKEN_HERE' жолын өзгертіңіз")
        return
    
    # Application құру
    application = Application.builder().token(TOKEN).build()
    
    # Командалар
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("авторлар", show_authors))
    application.add_handler(CommandHandler("шығармалар", show_works))
    application.add_handler(CommandHandler("кейіпкерлер", show_characters))
    application.add_handler(CommandHandler("деректер", show_facts))
    application.add_handler(CommandHandler("ойын", start_quiz))
    application.add_handler(CommandHandler("ұпайлар", show_points))
    application.add_handler(CommandHandler("көмек", help_command))
    
    # Мәтін хабарламалары
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Викторина жауаптары
    application.add_handler(MessageHandler(
        filters.Regex(r"^[A-D]\)"),
        handle_quiz_answer
    ))
    
    # Ботты іске қосу
    print("✅ Бот іске қосылды!")
    print("🎮 Викторина ойындарын ойнау үшін /ойын командасын жіберіңіз")
    print("📚 Авторлар туралы білу үшін /авторлар командасын жіберіңіз")
    
    application.run_polling()

if __name__ == '__main__':
    main()

"""handlers/menu.py — Бас мәзір обработчиктері"""
from telegram import Update
from telegram.ext import CallbackContext
from database import get_or_create_user, get_level_info
from utils.keyboards import main_menu_keyboard, MAIN_MENU_TEXT

DAILY_FACTS = [
    "💡 Абайдың шын есімі — Ибраһим. «Абай» атын әжесі Зере берген!",
    "💡 Жамбыл Жабаев 99 жыл өмір сүрді — ұзақ өмірлі ақын!",
    "💡 «Абай жолы» романы дүние жүзінің 100+ тіліне аударылды!",
    "💡 Ахмет Байтұрсынов 1912 жылы қазақ алфавитін жасады!",
    "💡 Сәкен Сейфуллин, Беймбет Майлин, Ілияс Жансүгіров — үшеуі де 1938 жылы репрессияға ұшырады!",
    "💡 Мұхтар Әуезов 50-ден астам пьеса жазды!",
    "💡 «Абай жолы» Лениндік сыйлықты 1959 жылы алды!",
    "💡 Ыбырай Алтынсарин Қазақстанда алғашқы 4 мектеп ашты!",
    "💡 Мағжан Жұмабаев 1960 жылы ғана посмертно ақталды!",
    "💡 Сұлтанмахмұт Торайғыров небәрі 27 жасында дүниеден өтті!",
    "💡 Бауыржан Момышұлы Москва шайқасының батыры болды!",
    "💡 «Қозы Көрпеш — Баян сұлу» — дүние жүзіндегі ең атақты сүйіспеншілік жырларының бірі!",
    "💡 Абай Пушкиннің «Евгений Онегинінен» «Татьянаның хатын» қазақшаға аударды!",
    "💡 Жамбыл домбырамен жырлап, айтыста ешкімге жеңіленбеген!",
    "💡 Алаш партиясы 1917 жылы Азамат соғысы кезінде құрылды!",
]

import random
import datetime


def start_command(update: Update, context: CallbackContext):
    """Бот іске қосылғанда немесе /start командасы"""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.full_name)
    level = db_user.get('level', 1)
    emoji, name = get_level_info(level)
    points = db_user.get('points', 0)

    welcome = (
        f"👋 Сәлем, <b>{user.first_name}</b>!\n\n"
        f"🎓 Деңгейің: {emoji} <b>{name}</b>\n"
        f"⭐ Ұпайлар: <b>{points}</b>\n\n"
        f"{MAIN_MENU_TEXT}"
    )
    update.message.reply_text(welcome, parse_mode='HTML', reply_markup=main_menu_keyboard())


def main_menu_callback(update: Update, context: CallbackContext):
    """Бас мәзірге оралу"""
    query = update.callback_query
    query.answer()
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.full_name)
    level = db_user.get('level', 1)
    emoji, name = get_level_info(level)
    points = db_user.get('points', 0)
    text = (
        f"🎓 Деңгейің: {emoji} <b>{name}</b>  ⭐ {points} ұпай\n\n"
        f"{MAIN_MENU_TEXT}"
    )
    query.edit_message_text(text, parse_mode='HTML', reply_markup=main_menu_keyboard())


def daily_fact_callback(update: Update, context: CallbackContext):
    """Күнделікті қызықты факт"""
    query = update.callback_query
    query.answer()
    fact = random.choice(DAILY_FACTS)
    # Күн бойынша бір факт
    day_idx = datetime.date.today().toordinal() % len(DAILY_FACTS)
    fact = DAILY_FACTS[day_idx]
    from utils.keyboards import back_to_main
    query.edit_message_text(
        f"📅 <b>БҮГІНГІ ФАКТ</b>\n\n{fact}\n\n"
        f"Ертең жаңа факт күтеді! 😊",
        parse_mode='HTML',
        reply_markup=back_to_main()
    )


def help_callback(update: Update, context: CallbackContext):
    """Анықтама"""
    query = update.callback_query
    query.answer()
    from utils.keyboards import back_to_main
    help_text = (
        "ℹ️ <b>АНЫҚТАМА</b>\n\n"
        "📖 <b>Сабақтар</b> — 1-11 класс материалдары\n"
        "🎮 <b>Ойындар</b> — 6 түрлі ойын:\n"
        "   • Викторина (4 нұсқа)\n"
        "   • Кім жазды?\n"
        "   • Шығарманы тап!\n"
        "   • Цитата жарысы\n"
        "   • Блиц-тур\n"
        "   • Кейіпкерлер\n\n"
        "👤 <b>Авторлар</b> — 18+ автор биографиясы\n"
        "📊 <b>Прогресс</b> — ұпайлар, деңгей, стрик\n"
        "🏆 <b>Рейтинг</b> — ең үздік оқушылар\n\n"
        "🎯 <b>Ұпай жүйесі:</b>\n"
        "• Дұрыс жауап: +10 ұпай\n"
        "• Тақырып аяқтау: +15 ұпай\n"
        "• Автор оқу: +5 ұпай\n"
        "• Мінсіз викторина: +50 ұпай бонус\n\n"
        "📈 <b>Деңгейлер:</b> 1-11 деңгей\n"
        "⭐ 100 ұпайдан 2-деңгей, 300-ден 3-деңгей..."
    )
    query.edit_message_text(help_text, parse_mode='HTML', reply_markup=back_to_main())

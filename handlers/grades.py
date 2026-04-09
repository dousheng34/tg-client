"""handlers/grades.py — Сыныптар бойынша оқу материалдары"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from content.grades import (
    get_grade_info, get_grade_topics, get_topic_content,
    list_all_grades, LITERARY_TERMS
)
from database import get_or_create_user, add_points, mark_topic_completed
from utils.keyboards import back_to_main


def _grades_keyboard():
    """5–11 сынып таңдау батырмалары"""
    buttons = []
    row = []
    emojis = {5:"🌟",6:"⚔️",7:"💎",8:"🦥",9:"✍️",10:"🔥",11:"🏆"}
    for grade, emoji, title in list_all_grades():
        if grade < 5:
            continue  # 1-4 сынып емес
        em = emojis.get(grade, "📖")
        short = f"{em}{grade}-сынып"
        row.append(InlineKeyboardButton(short, callback_data=f"grade_{grade}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🏠 Басты мәзір", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def _topics_keyboard(grade: int, topics: list):
    """Сынып тақырыптарының батырмалары"""
    buttons = [
        [InlineKeyboardButton(t["title"], callback_data=f"topic_{grade}_{t['key']}")]
        for t in topics
    ]
    buttons.append([
        InlineKeyboardButton("🔙 Сыныптарға", callback_data="menu_grades"),
        InlineKeyboardButton("🏠 Мәзір", callback_data="menu_main"),
    ])
    return InlineKeyboardMarkup(buttons)


def _topic_done_keyboard(grade: int):
    """Тақырып аяқтағаннан кейінгі батырмалар"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Аяқтадым! (+15 ұпай)", callback_data=f"topic_done_{grade}")],
        [
            InlineKeyboardButton("🔙 Тақырыптарға", callback_data=f"grade_{grade}"),
            InlineKeyboardButton("🏠 Мәзір", callback_data="menu_main"),
        ],
        [InlineKeyboardButton("📖 Сөздік", callback_data="menu_terms")],
    ])


# ─── ХЕНДЛЕРЛЕР ──────────────────────────────────────────────────────────────

def grades_menu_callback(update: Update, context: CallbackContext):
    """Сыныптар мәзірі"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "📚 <b>СЫНЫПТАР БОЙЫНША ОҚУ МАТЕРИАЛЫ</b>\n\n"
        "5-11 сынып бойынша барлық тақырыптар:\n"
        "• Авторлар өмірбаяны\n"
        "• Шығармалар мазмұны\n"
        "• Талдауы және идеясы\n"
        "• Цитаталар мен деректер\n\n"
        "👇 <b>Сыныбыңызды таңдаңыз:</b>",
        parse_mode='HTML',
        reply_markup=_grades_keyboard()
    )


def grade_select_callback(update: Update, context: CallbackContext):
    """Нақты сыныпты таңдағанда тақырыптар тізімі"""
    query = update.callback_query
    query.answer()
    grade = int(query.data.split('_')[1])
    data = get_grade_info(grade)
    topics = get_grade_topics(grade)

    if not data or not topics:
        query.edit_message_text(
            "⚠️ Тақырыптар табылмады.",
            reply_markup=_grades_keyboard()
        )
        return

    emoji = data.get("emoji", "📚")
    title = data.get("title", f"{grade}-сынып")
    desc  = data.get("description", "")
    count = len(topics)

    text = (
        f"{emoji} <b>{title}</b>\n\n"
        f"📝 {desc}\n\n"
        f"📖 <b>{count} тақырып қол жетімді:</b>\n"
    )
    for i, t in enumerate(topics, 1):
        text += f"{i}. {t['title']}\n"
    text += "\n👇 <b>Тақырыпты таңдаңыз:</b>"

    query.edit_message_text(
        text, parse_mode='HTML',
        reply_markup=_topics_keyboard(grade, topics)
    )


def topic_callback(update: Update, context: CallbackContext):
    """Тақырып мазмұнын көрсету"""
    query = update.callback_query
    query.answer()
    parts = query.data.split('_', 2)
    grade = int(parts[1])
    topic_key = parts[2]
    content = get_topic_content(grade, topic_key)
    context.user_data['last_topic_key'] = topic_key
    context.user_data['last_topic_grade'] = grade
    query.edit_message_text(
        content, parse_mode='HTML',
        reply_markup=_topic_done_keyboard(grade)
    )


def topic_done_callback(update: Update, context: CallbackContext):
    """Тақырып оқылды — ұпай беру"""
    query = update.callback_query
    query.answer()
    grade = int(query.data.split('_')[-1])
    user = update.effective_user
    topic_key = context.user_data.get('last_topic_key', f'grade{grade}_topic')
    mark_topic_completed(user.id, topic_key)
    updated = add_points(user.id, 15)
    points = updated.get('points', 0)
    level  = updated.get('level', 1)
    query.edit_message_text(
        f"✅ <b>Тақырып сәтті оқылды!</b>\n\n"
        f"🎉 <b>+15 ұпай</b> есептелді!\n"
        f"⭐ Жалпы ұпай: <b>{points}</b>\n"
        f"🎓 Деңгей: <b>{level}</b>\n\n"
        f"Оқуды жалғастыр, білім — күш! 💪",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🔙 {grade}-сынып тақырыптарына", callback_data=f"grade_{grade}")],
            [InlineKeyboardButton("📚 Барлық сыныптар", callback_data="menu_grades")],
            [InlineKeyboardButton("🏠 Басты мәзір", callback_data="menu_main")],
        ])
    )


def terms_callback(update: Update, context: CallbackContext):
    """Әдебиеттік терминдер анықтамасы"""
    query = update.callback_query
    query.answer()
    text = "📖 <b>ӘДЕБИЕТ ТЕРМИНДЕРІ СӨЗДІГІ</b>\n\n"
    for term, definition in LITERARY_TERMS.items():
        text += f"🔹 <b>{term.capitalize()}</b> — {definition}\n\n"
    query.edit_message_text(
        text, parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Басты мәзір", callback_data="menu_main")]
        ])
    )

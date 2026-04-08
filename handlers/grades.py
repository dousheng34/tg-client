"""handlers/grades.py — Сыныптар бойынша оқу материалдары"""
from telegram import Update
from telegram.ext import CallbackContext
from content.grades import get_grade_info, get_grade_topics, format_grade_menu, get_topic_content
from database import get_or_create_user, add_points, mark_topic_completed
from utils.keyboards import grades_keyboard, grade_topics_keyboard, topic_done_keyboard, back_to_main


def grades_menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "📚 <b>СЫНЫПТАР БОЙЫНША ОҚУЛЫҚ</b>\n\n"
        "Сыныбыңызды таңдаңыз:",
        parse_mode='HTML',
        reply_markup=grades_keyboard()
    )


def grade_select_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    grade = int(query.data.split('_')[1])
    text = format_grade_menu(grade)
    topics = get_grade_topics(grade)
    if not topics:
        query.edit_message_text("Тақырыптар табылмады.", reply_markup=grades_keyboard())
        return
    query.edit_message_text(
        text, parse_mode='HTML',
        reply_markup=grade_topics_keyboard(grade, topics)
    )


def topic_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # callback_data = "topic_{grade}_{key}"
    parts = query.data.split('_', 2)
    grade = int(parts[1])
    topic_key = parts[2]
    content = get_topic_content(grade, topic_key)
    context.user_data['last_topic_key'] = topic_key
    context.user_data['last_topic_grade'] = grade
    query.edit_message_text(
        content, parse_mode='HTML',
        reply_markup=topic_done_keyboard(grade)
    )


def topic_done_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    grade = int(query.data.split('_')[-1])
    user = update.effective_user
    topic_key = context.user_data.get('last_topic_key', f'grade{grade}_unknown')
    mark_topic_completed(user.id, topic_key)
    updated = add_points(user.id, 15)
    points = updated.get('points', 0)
    level = updated.get('level', 1)
    query.edit_message_text(
        f"✅ <b>Тақырып аяқталды!</b>\n\n"
        f"+15 ұпай қосылды!\n"
        f"⭐ Жалпы ұпай: <b>{points}</b>\n"
        f"🎓 Деңгей: <b>{level}</b>",
        parse_mode='HTML',
        reply_markup=back_to_main()
    )

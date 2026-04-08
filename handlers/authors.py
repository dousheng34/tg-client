"""handlers/authors.py — Авторлар обработчиктері"""
from telegram import Update
from telegram.ext import CallbackContext
from content.authors import AUTHORS, AUTHOR_KEYS, format_author_card, format_author_full, format_infographic
from database import get_or_create_user, add_points, mark_author_viewed, give_achievement
from utils.keyboards import authors_keyboard, author_detail_keyboard, back_to_authors, back_to_main


def authors_menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    authors_list = [(k, v['name'], v['emoji']) for k, v in AUTHORS.items()]
    query.edit_message_text(
        "👤 <b>АВТОРЛАР</b>\n\n"
        f"Жалпы {len(authors_list)} автор туралы мәліметтер бар.\n"
        "Авторды таңдаңыз:",
        parse_mode='HTML',
        reply_markup=authors_keyboard(authors_list)
    )


def author_card_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    key = query.data.replace('author_', '')
    # Авторды оқыды деп белгіле
    user = update.effective_user
    mark_author_viewed(user.id, key)
    updated = add_points(user.id, 5)

    # Жетістік тексеру
    from database import get_user_stats
    stats = get_user_stats(user.id)
    viewed = stats.get('authors_viewed', 0)
    if viewed >= 5:
        give_achievement(user.id, 'authors_5')
    if viewed >= 10:
        give_achievement(user.id, 'authors_10')
    if viewed >= len(AUTHORS):
        give_achievement(user.id, 'authors_all')

    card = format_author_card(key)
    query.edit_message_text(
        card + f"\n\n+5 ұпай қосылды! ⭐ {updated.get('points', 0)}",
        parse_mode='HTML',
        reply_markup=author_detail_keyboard(key)
    )


def author_full_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    key = query.data.replace('author_full_', '')
    text = format_author_full(key)
    query.edit_message_text(text, parse_mode='HTML', reply_markup=author_detail_keyboard(key))


def author_infographic_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    key = query.data.replace('author_info_', '')
    text = format_infographic(key)
    query.edit_message_text(text, parse_mode='HTML', reply_markup=author_detail_keyboard(key))


def author_works_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    key = query.data.replace('author_works_', '')
    a = AUTHORS.get(key, {})
    if not a:
        query.answer("Автор табылмады")
        return
    works_text = "\n".join(f"  📗 {w}" for w in a.get('works', []))
    query.edit_message_text(
        f"{a['emoji']} <b>{a['name']}</b>\n\n"
        f"📚 <b>Шығармалары:</b>\n{works_text}",
        parse_mode='HTML',
        reply_markup=author_detail_keyboard(key)
    )


def author_quotes_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    key = query.data.replace('author_quotes_', '')
    a = AUTHORS.get(key, {})
    if not a:
        query.answer("Автор табылмады")
        return
    quotes_text = "\n\n".join(f"  💬 {q}" for q in a.get('quotes', []))
    facts_text = "\n".join(a.get('facts', []))
    query.edit_message_text(
        f"{a['emoji']} <b>{a['name']}</b>\n\n"
        f"💬 <b>Цитаталары:</b>\n{quotes_text}\n\n"
        f"📌 <b>Бір қызық:</b>\n{facts_text}",
        parse_mode='HTML',
        reply_markup=author_detail_keyboard(key)
    )
